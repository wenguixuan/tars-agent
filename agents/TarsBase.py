
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tasks.TaskBase import TaskBase, TaskStatus


class TarsBase(object):
    def __init__(self, role: str, name: str, max_retry_times=2, llm_config=None) -> None:
        assert name is not None and isinstance(name, str) and len(name.replace(' ', '')) > 0, Exception('tars agnet must be given a specific name, which must be a non-empty string.')
        assert role is not None and isinstance(role, str) and len(name.replace(' ', '')) > 0, Exception('tars agnet must be given a specific role, which must be a non-empty string.')
        assert llm_config is not None and isinstance(llm_config, dict), Exception('tars agnet must be given a llm config.')

        self.role = role
        self.name = name

        self.max_retry_times = max_retry_times

        self.brain = self.init_brain()
        self.llm = ChatOpenAI(model=llm_config['model_name'], 
                       base_url=llm_config['base_url'], 
                       api_key=llm_config['api_key'])

        
    def init_brain(self):
        brain_str = f"<YOUR NAME>: {self.name}\n<YOUR ROLE>: {self.role}\n"
        return brain_str


    def answer(self, task: TaskBase):
        assert task is not None, Exception('tasks can not be must be None.')
        try_times = 0
        task_answer = None
        while try_times < self.max_retry_times:
            task_answer = self.invoke(task)
            if task_answer is not None:
                task.answer = task_answer
                task.status = TaskStatus.SUCCESS
                break
            else:
                try_times += 1
        
        if try_times >= self.max_retry_times:
            task.status = TaskStatus.FAILED

        return task
        


    def invoke(self, task: TaskBase):
        assert task is not None, Exception('task can not be must be None.')

        messages = [
            SystemMessage(content=self.brain),
            HumanMessage(content=task.task_description),
        ]
        try:
            llm_answer_raw = self.llm.invoke(messages)
            llm_answer = task.output_parser.parse(llm_answer_raw.content)
            return llm_answer
        except Exception as e:
            return None


    def __str__(self):
        # 返回一个描述该对象的字符串
        return f"{self.init_brain}"