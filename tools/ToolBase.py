from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

from examples.ExampleBase import ExampleBase

class ToolType:
    API = 'api'
    FUNCTION = 'function'

class ToolBase(ABC):
    def __init__(self, tool_name:str, tool_description: str, tool_type: ToolType, day_delay: int=0, examples: List[ExampleBase]=[]) -> None:
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_type = tool_type
        self.tool_system_date = (datetime.now() - timedelta(days=day_delay)).strftime('%Y-%m-%d')
        self.examples : List[ExampleBase] = examples

    @abstractmethod
    def execute(**kwargs):
        pass


