from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List
from enum import Enum
from config.ConfigLoader import ConfigLoader
from examples.ExampleBase import ExampleBase

class ToolType(Enum):
    API = 'API'
    FUNCTION = 'FUNCTION'

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

    def import_tools_from_yaml(base_path: str, yaml_path: str) -> List:
        from tools.ApiTool import ApiTool  # Move import here
        config_loader = ConfigLoader(base_path)
        tools_config = config_loader.read_yaml(yaml_path)
        tools = []

        for tool_name in tools_config:
            tool_type = tools_config[tool_name].get('tool_type', '').lower()
            
            if tool_type == ToolType.API.value.lower():
                tools.append(ApiTool.factory(tools_config[tool_name]))
            else:
                raise ValueError(f'Unsupported tool type: {tools_config[tool_name].get("tool_type", "")}')

        return tools


