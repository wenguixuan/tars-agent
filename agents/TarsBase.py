
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tasks.TaskBase import TaskBase, TaskStatus
from utils.Log import Log


class TarsBase(object):
    def __init__(self, role: str, name: str, llm_config=None, max_retry_times=2) -> None:
        assert name is not None and isinstance(name, str) and len(name.replace(' ', '')) > 0, Exception('tars agnet must be given a specific name, which must be a non-empty string.')
        assert role is not None and isinstance(role, str) and len(name.replace(' ', '')) > 0, Exception('tars agnet must be given a specific role, which must be a non-empty string.')
        assert llm_config is not None and isinstance(llm_config, dict), Exception('tars agnet must be given a llm config.')

        self.role = role
        self.name = name
        self.id = uuid.uuid4().hex

        self.max_retry_times = max_retry_times

        self.brain = self.init_brain()

        self.logger = Log()

        assert all(key in llm_config for key in ['model_name', 'base_url', 'api_key']), "LLM config must contain 'model_name', 'base_url', and 'api_key'"

        self.llm = ChatOpenAI(model=llm_config['model_name'], 
                       base_url=llm_config['base_url'], 
                       api_key=llm_config['api_key'],
                       temperature=llm_config.get('temperature', 0.2))
        
    def init_brain(self):
        brain_str = f"<YOUR NAME>: {self.name}\n<YOUR ROLE>: {self.role}\n"
        return brain_str


    def answer(self, task: TaskBase):
        assert task is not None, Exception('task can not be must be None.')
        try_times = 0
        while try_times < self.max_retry_times:
            task_raw_answer = self.invoke(task)
            if task_raw_answer is not None:
                try:
                    task.set_answer(task_raw_answer.content)
                    break
                except Exception as e:
                    if 'chat_history' in task.context:
                        task.context['chat_history'] += f"\nSystem Error: {e}"
                    else:
                        task.context['chat_history'] = f"\nSystem Error: {e}"
                    try_times += 1
            else:
                try_times += 1
        
        if try_times >= self.max_retry_times:
            task.status = TaskStatus.FAILED
        return task
        


    def invoke(self, task: TaskBase):
        assert task is not None, Exception('task can not be must be None.')


        log_messages = f"\nAgent ID: {self.id}\nAgent Brain: \n{self.brain}\nAgent Task: \n{task.task_description}\n"
        messages = [
            SystemMessage(content=self.brain),
            HumanMessage(content=task.task_description),
        ]
        try:
            
            llm_answer_raw = self.llm.invoke(messages)
            log_messages += f"Agent Answer: {llm_answer_raw.content}\n"
            self.logger.info(log_messages)
            return llm_answer_raw
        except Exception as e:
            log_messages += f"Agent Answer: None\n"
            log_messages += f"Agent Error: {e}\n"
            self.logger.error(log_messages)
            return None


    def __str__(self):
        # 返回一个描述该对象的字符串
        return f"{self.init_brain}"