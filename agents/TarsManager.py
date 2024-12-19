

from agents.TarsBase import TarsBase

from pydantic import BaseModel, Field
from agents.TarsWorker import TarsWorker
from memory.MessageBase import MessageBase, MessageType
from tasks.TaskBase import TaskBase, TaskStatus
from tools.ToolBase import ToolBase
from langchain_core.output_parsers import JsonOutputParser

# Define your desired data structure.
class ManagerAnswer(BaseModel):
    tasks: dict[str, str] = Field(description="")
    is_finished: bool = Field(description="")
    response: str = Field(description="")



class TarsManager(TarsBase):

    default_max_retry_times = 2
    default_manager_name = 'TarsManager'
    default_manager_role = 'You are a manager of Tars worker agents.'

    default_instruction = {
        'plan': '',
        'review': '',
    }

    default_precaution = [
        'If there is no suitable API, you can return empty dictionary.',
        'The selected APIs and parameters must be correct and feasible.',
        'Strictly follow the request and do not make any assumptions.',
        'Strictly follow the output format.',
    ]


    def __init__(self, name: str=default_manager_name, role: str=default_manager_role, llm_config=None, max_retry_times=default_max_retry_times):
        super().__init__(role, name, llm_config, max_retry_times)

    

