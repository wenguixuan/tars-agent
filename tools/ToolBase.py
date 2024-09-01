from abc import ABC, abstractmethod
class ToolBase(ABC):
    def __init__(self, tool_name:str, tool_description: str, tool_type: str) -> None:
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_type = None

    @abstractmethod
    def execute(**kwargs):
        pass


