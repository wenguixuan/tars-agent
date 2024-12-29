

import json
from typing import List

from pydantic import BaseModel, Field
from agents.TarsAgentType import TarsAgentType
from agents.TarsBase import TarsBase
from agents.TarsWorker import TarsWorker
from memory.MessageBase import MessageBase, MessageType
from tasks.TaskBase import TaskBase, TaskStatus
from tools.ToolBase import ToolBase
from langchain_core.output_parsers import JsonOutputParser

from utils.format_dataframe import df_format


# Define your desired data structure.
class ApiAnswer(BaseModel):
    apis: dict[str, dict[str, str]] = Field(description="the APIs and parameters you selected. The key of the dictionary is the API name, and the value is a dictionary of parameters and their values. If there is no suitable API, you can return empty dictionary.")

    @classmethod
    def to_string(cls):
        class_dict = {}
        for name, field in cls.__annotations__.items():
            class_dict[name] = {
                "type": str(field),
                "description": cls.__fields__[name].description
            }
        return json.dumps(class_dict, indent=4)
    
class TarsApiWorker(TarsWorker):

    default_max_retry_times = 2
    default_worker_name = 'TarsApiWorker'
    default_worker_role = 'You are a helpful assistant. You manage a tool with APIs. Please understand the request carefully and select the most appropriate API and parameters. If there is no suitable API, you can return empty dictionary.'

    default_instruction = {
        'plan': 'According to the request, select the most appropriate API and fill in the appropriate parameters. If there is no suitable API, you can return empty dictionary.',
        'review': '',
    }

    default_precaution = [
        'If there is no suitable API, you can return empty dictionary.',
        'The selected APIs and parameters must be correct and feasible.',
        'Strictly follow the request and do not make any assumptions.',
        'Strictly follow the output format.',
    ]

    def __init__(self, 
                 name: str=default_worker_name, 
                 role: str=default_worker_role, 
                 instructions: dict[str, str]=default_instruction,
                 precautions: list[str]=default_precaution,
                 llm_config=None, 
                 tool: ToolBase=None,
                 max_retry_times=default_max_retry_times):
        assert isinstance(instructions, dict), 'instructions must be a dictionary.'
        assert isinstance(precautions, list), 'precautions must be a list.'
        assert instructions.keys() == TarsApiWorker.default_instruction.keys(), f'instructions must contain the keys: {TarsApiWorker.default_instruction.keys()}'
        assert isinstance(tool, ToolBase), 'tool must be a ToolBase instance.'
        super().__init__(role=role, name=name, llm_config=llm_config, max_retry_times=max_retry_times)
        self.instructions = instructions
        self.precautions = precautions
        self.tool = tool
        self.chat_history : List[MessageBase] = []

    def build_task(self, request: str, is_review: bool=False):
        chat_history_str = ''
        context = {}
        context['tool'] = f'\n{self.tool}'
        if len(self.chat_history) > 0:
            chat_history_str = ''
            for message in self.chat_history:
                if message.sender_id == self.id:
                    chat_history_str += f'Your Answer: {message.content}\n'
                else:
                    chat_history_str += f'{message.sender_role}: {message.content}\n'
            context['chat_history'] = chat_history_str
        context['request'] = request
        if is_review:
            instruction = self.instructions['review']
        else:
            instruction = self.instructions['plan']
        output_parser = JsonOutputParser(pydantic_object=ApiAnswer)
        task = TaskBase(context=context, instruction=instruction, precautions=self.precautions, examples=self.tool.examples, output_parser=output_parser)
        return task

    def answer(self, sender_id: str, sender_name: str, sender_role: str, request: str, is_plan: bool=True, is_review: bool=False, is_execute: bool=False):

        assert request is not None, Exception('request can not be must be None.')

        assert is_plan or is_review or is_execute, Exception('is_plan, is_review and is_execute can not be all False.')
        assert not (is_plan and is_review), Exception('is_plan and is_review can not be both True.')
        assert not (is_plan and is_execute), Exception('is_plan and is_execute can not be both True.')
        assert not (is_review and is_execute), Exception('is_review and is_execute can not be both True.')

        if is_plan:
            message = self.plan(sender_id, sender_name, sender_role, request)

        elif is_review:
            message = self.review(sender_id, sender_name, sender_role, request)
        else:
            message = self.execute(sender_id, sender_name, sender_role, request)
        return message
    

    def execute(self, sender_id: str, sener_name:str, sender_role: TarsAgentType, request: str):
        task = self.build_task(request, is_review=False)
        TarsBase.answer(self, task)

        if task.status == TaskStatus.SUCCESS:
            selected_apis = task.formatted_answer.get('apis', {})
            if len(selected_apis) == 0:
                return None
            

            results = self.tool.execute(selected_apis)

            answer = ""

            for result in results:
                api_signature = result[0]
                data_json = result[1]

                answer += f"call api: `{api_signature}`, got: \n{data_json}\n"
            
            message = MessageBase(sender_id=self.id, 
                               sender_name=self.name, 
                               sender_role=self.agent_type,
                               receiver_id=sender_id,
                               receiver_name=sener_name,
                               receiver_role=sender_role,
                               content=answer,
                               type=MessageType.INFORMATION)
            return message
        else:
            return None

        
    
    def review(self, sender_id: str, sener_name:str, sender_role: TarsAgentType, request: str):
        pass

    def plan(self, sender_id: str, sener_name:str, sender_role: TarsAgentType, request: str):
        task = self.build_task(request, is_review=False)
        TarsBase.answer(self, task)
        if task.status == TaskStatus.SUCCESS:
            selected_apis = task.formatted_answer.get('apis', {})
            if len(selected_apis) == 0:
                return None
            plan = "I can use the following APIs to query the relevant information you need:\n"
            for api in selected_apis:
                plan += f'{api}: {selected_apis[api]}\n'

            message = MessageBase(sender_id=self.id, 
                               sender_name=self.name, 
                               sender_role=self.agent_type,
                               receiver_id=sender_id,
                               receiver_name=sener_name,
                               receiver_role=sender_role,
                               content=plan,
                               type=MessageType.SOLUTION)
            return message
        else:
            return None
            


