from enum import Enum
from typing import List

from tools.ToolBase import ToolBase
class TaskStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'

class TaskBase(object):
    def __init__(self, context:str, instruction: str, task_description: str, tools=List[ToolBase], examples=[], childrens=[], output_parser=None) -> None:
        self.context = context
        self.instruction = instruction
        self.task_description = task_description
        self.tools = tools
        self.examples = examples
        self.output_parser = output_parser
        self.childrens = childrens
        self.answer = None
        self.status = TaskStatus.NOT_STARTED

