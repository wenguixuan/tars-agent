
from langchain_openai import ChatOpenAI

from tasks.TaskBase import TaskBase


class TarsBase(object):
    def __init__(self, role: str = 'You are a highly intelligent and autonomous agent capable of performing complex tasks.', name: str = 'tars', output_parser=None, max_retry_times=2, llm_config=None) -> None:
        assert name is not None and isinstance(name, str) and len(name.replace(' ', '')) > 0, Exception('tars agnet must be given a specific name, which must be a non-empty string.')
        assert role is not None and isinstance(role, str) and len(name.replace(' ', '')) > 0, Exception('tars agnet must be given a specific role, which must be a non-empty string.')
        assert llm_config is not None and isinstance(role, dict), Exception('tars agnet must be given a llm config.')

        self.role = role
        self.name = name

        self.output_parser = output_parser
        self.answer_format_requirements = "No specific requirements."
        if self.output_parser is not None:
            self.answer_format_requirements = self.output_parser.get_format_instructions()

        self.max_retry_times = max_retry_times

        self.brain = self.init_brain()
        self.llm = ChatOpenAI(model=llm_config['model_name'], 
                       base_url=llm_config['base_url'], 
                       api_key=llm_config['api_key'])

        

    
    def init_brain(self):
        brain_str = f"<YOUR NAME>: {self.name}\n<YOUR ROLE>: {self.role}\n<ANSWER FORMAT REQUIREMENTS>: {self.answer_format_requirements}\n"
        return brain_str


    def answer(self, task):
        assert task is not None, Exception('tasks can not be must be None.')
        try_times = 0
        task_answer = None
        while try_times < self.max_retry_times:
            task_answer = self.invoke(task)
            if task_answer is not None:
                break
            else:
                try_times += 1



    def invoke(self, task: TaskBase):
        assert task is not None, Exception('tasks can not be must be empty.')


        self.context = context
        self.instruction = instruction
        self.task_description = task_description
        self.tools = tools
        self.examples = examples
        self.output_parser = output_parser
        self.childrens = childrens
        self.answer = None
        self.status = TaskStatus.NOT_STARTED

        
        examples = task.examples
        if len(examples) == 0:
            pass
        else:
            example_str = ''
            for example_idx in range(len(examples)):
                example_str = f"EXAMPLE {example_idx+1}: {examples[example_idx]} "
        
        human_message_content = f"***CONTEXT***: {task.context}\n***TASK DESCRIPTION***: {task.task_description}\n***REFERENCE EXAMPLES***: {example_str}\n"

        self.llm.invoke()

        answer = 

    def __str__(self):
        # 返回一个描述该对象的字符串
        return f"{self.init_brain}"