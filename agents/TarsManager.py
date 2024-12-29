

from concurrent.futures import as_completed
from datetime import datetime
from enum import Enum
import json
from typing import Dict, List, Literal, Optional, Union
from agents.TarsAgentType import TarsAgentType
from agents.TarsBase import TarsBase

from pydantic import BaseModel, Field
from agents.TarsWorker import TarsWorker
from memory.MessageBase import MessageBase, MessageType
from tasks.TaskBase import TaskBase, TaskStatus
from tools.ToolBase import ToolBase
from langchain_core.output_parsers import JsonOutputParser
from utils.thread_pool import Pool

class ActionType(Enum):
    ASSIGN_TASK = 'ASSIGN_TASK'
    RESPONSE = 'RESPONSE'

# Define your desired data structure.
class ManagerAnswer(BaseModel):
    subtasks: Optional [List[Dict[str, str]]] = Field(
        description="When you need to assign subtasks, please use this field. `subtasks` is a list where each element is a subtask represented by a dictionary. The dictionary must contain two keys: 'name' and 'subtask'. The value for 'name' is the worker's name, indicating who is responsible for this subtask. The value for 'subtask' provides the subtask details. For example: {'name': 'xxx', 'subtask': 'xxx'}. Subtasks assigned to the same worker can be combined into one dictionary."
    )
    response: Optional[str] = Field(
        description="When you need to give user a response, please use this field. The response must be in the same language of the user request."
    )
    reference_workers: Optional[List[str]] = Field(
        description="The list of names of the worker from whom the data referenced in your response comes."
    )
    action_type: Literal['assign_task', 'response'] = Field(
        description="If you need to assign subtasks, please set it to `assign_task`. If you need to answer the user, please set it to `response`."
    )



class TarsManager(TarsBase):


    default_max_retry_times = 2
    default_max_rounds = 5
    default_manager_name = 'TarsManager'
#     default_manager_role = """You are the manager of a group of workers. \
# You will be given a user request and then the workers you manage will provide corresponding solutions or data information. \
# You have two main responsibilities: \
# first, review the workers'solutions and select one or more of them to assign their corresponding subtasks using the `task` field, \
# with the goal of helping complete the user request. \
# Second, review the data collected by workers to determine whether the information they collected can answer the user request. \
# If so, set the `is_finish` field to true, and use the `response` field to answer the user question in Chinese and at the same time you shuold use the `reference_workers` field to give the worker(s) name from whom the data referenced in your response comes, \
# otherwise set the `is_finish` field to false, and continue to use the `tasks` field to assign new subtasks to the workers."""

    default_manager_role = """You are the manager of a group of workers. """
    default_error_tips = "Sorry, something went wrong～"

    default_instruction = {
        "first": "Please review the worker solutions and select the appropriate worker to assign subtasks within its capabilities.",
        "intermediate": "Please review the data collected by workers to determine whether the information they collected can answer the user request. If so, set the `is_finish` field to true, and use the `response` field to answer the request, otherwise set the `is_finish` field to false, and continue to use the `subtasks` field to assign new subtasks to the workers.",            
        "finally": "The specified number of assigned subtask rounds has been exceeded. Please answer the user request based on the data or information collected by the worker."
    }

    default_precaution = [
        'Strictly follow the request and do not make any assumptions.',
        'Strictly follow the output format.',
    ]


    def __init__(self, name: str=default_manager_name, 
                 role: str=default_manager_role, 
                 llm_config=None, 
                 max_retry_times=default_max_retry_times,
                 max_rounds=default_max_rounds,
                 instructions: dict[str, str]=default_instruction,
                 precautions: list[str]=default_precaution,
                 workers: List[TarsWorker]=[],
                 system_date: str=datetime.now().strftime("%Y-%m-%d")):
        super().__init__(role, name, llm_config, max_retry_times, TarsAgentType.Manager)
        assert isinstance(instructions, dict), 'instructions must be a dictionary.'
        assert isinstance(precautions, list), 'precautions must be a list.'
        assert instructions.keys() == TarsManager.default_instruction.keys(), f'instructions must contain the keys: {TarsManager.default_instruction.keys()}'
        assert len(workers) > 0, 'workers must be a list and contain at least one worker.'
        self.max_rounds = max_rounds
        self.instructions = instructions
        self.precautions = precautions
        self.workers: List[TarsWorker] = workers
        self.chat_history : List[MessageBase] = []
        self.system_date = system_date


    def build_task(self, request: str, is_first: bool=False, is_intermediate: bool=False, is_finally: bool=False):
        chat_history_str = ''
        context = {}
        context['system date'] = self.system_date
        context['request'] = request
        if len(self.chat_history) > 0:
            chat_history_str = '\n'
            for message in self.chat_history:
                if message.sender_id == self.id:
                    chat_history_str += f'Your action: you assigned {message.receiver_name} a subtask: {message.content}\n'
                elif message.sender_id == -1:
                    chat_history_str += f'System: {message.content}\n'
                else:
                    chat_history_str += f'{message.sender_name}({message.type.value}): {message.content}\n'
            context['chat_history'] = chat_history_str
        
        if is_first :
            instruction = self.instructions['first']
        elif is_intermediate:
            instruction = self.instructions['intermediate']
        else:
            instruction = self.instructions['finally']
        output_parser = JsonOutputParser(pydantic_object=ManagerAnswer)
        task = TaskBase(context=context, instruction=instruction, precautions=self.precautions, examples=[], output_parser=output_parser)
        return task    

    def answer(self, request: str):
        retry_times = 0
        final_answer = None
        while retry_times < self.max_retry_times:
            try:
                is_plan_success = self.collect_plan(request)
                if not is_plan_success:

                    task = self.think(request, is_finally=True)
                else:
                    task = self.think(request, is_first=True)

                if task.status == TaskStatus.SUCCESS:
                    round_num = 1
                    action_type = task.formatted_answer.get('action_type', None)
                    assert action_type is not None, Exception('action_type is None in manager output')
                    
                    while round_num < self.max_rounds and action_type.lower() == ActionType.ASSIGN_TASK.value.lower():
                        worker_tasks = task.formatted_answer.get('subtasks', None)
                        assert worker_tasks is not None, Exception('subtasks is None in manager output')
                        assert len(worker_tasks) > 0, Exception('len(worker_tasks) = 0')

                        self.collect_data(worker_tasks, request)

                        task = self.think(request, is_intermediate=True)
                        round_num += 1
                        action_type = task.formatted_answer.get('action_type', None)
                        assert action_type is not None, Exception('action_type is None in manager output')
                        if action_type.lower() == ActionType.RESPONSE.value.lower():
                            final_answer = task.formatted_answer.get('response', TarsManager.default_error_tips)
                            reference_workers = task.formatted_answer.get('reference_workers', [])
                            references = []
                            for ref_worker in reference_workers:
                                for woker in self.workers:
                                    if ref_worker.lower() != woker.name:
                                        continue
                                    
                                    ref = f"[{woker.tool.tool_name}](https://rapidapi.com/)"
                                    references.append(ref)

                            final_answer += "\n参考资料: \n" + '\n'.join([f"{ref_idx+1}. {ref}"for ref_idx, ref in enumerate(references)])
                            break

                    if action_type.lower() == ActionType.RESPONSE.value.lower():
                        break
                    elif round_num >= self.max_rounds:
                        raise Exception(f"round_num {round_num} exceed max_rounds {self.max_rounds}")
                    elif action_type is None:
                        raise Exception('action_type is None in manager output')
                    else:
                        raise Exception(f"unsuport ActionType {action_type}")


                else:
                    raise Exception("think task failed")
                
            except Exception as e:
                self.logger.error(e)
                self.logger.error(f"retry_times: {retry_times}")
                self.chat_history = []
                retry_times += 1
                
        return final_answer

    def collect_plan(self, request: str):
        pool = Pool()
        threads = []
        plan_cnt = 0
        for worker in self.workers:
            thread = pool.submit(worker.answer, sender_id=self.id, sender_name=self.name, sender_role=self.agent_type, request=request, is_plan=True, is_review=False, is_execute=False)
            threads.append(thread)
        
        for future in as_completed(threads):
            result: MessageBase = future.result()
            if result is None:
                continue
            self.chat_history.append(result)
            plan_cnt += 1
        if plan_cnt == 0:
            system_message = MessageBase(
                sender_id='-1',
                sender_name=None,
                sender_role=None,
                content="There is no suitable tool to solve the problem at present. Please give feedback to users truthfully.",
                receiver_id=None,
                receiver_name=None,
                receiver_role=None,
                type=MessageType.ERROR
            )
            self.chat_history.append(system_message)
            return False
        return True

    def think(self, request:str, is_first: bool=False, is_intermediate: bool=False, is_finally: bool=False):
        task = self.build_task(request, is_first=is_first, is_intermediate=is_intermediate, is_finally=is_finally)
        TarsBase.answer(self, task)
        return task

    def collect_data(self, worker_tasks: List[dict[str, str]], request: str):
        for worker_task in worker_tasks:
            for worker in self.workers:
                if worker.name != worker_task.get('name', None):
                    continue
                subtask = worker_task.get('subtask', request)
                result = worker.answer(sender_id=self.id, sender_name=self.name, sender_role=self.agent_type, 
                                       request=subtask, is_plan=False, is_review=False, is_execute=True)
                
                action = MessageBase(sender_id=self.id, sender_name=self.name, sender_role=self.agent_type, 
                                                     receiver_id=worker.id, receiver_name=worker.name, receiver_role=TarsAgentType.Worker, 
                                                     content=str(subtask), type=MessageType.ACTION)
                self.chat_history.append(action)
                if result is None:
                    continue
                self.chat_history.append(result)
        return



    

