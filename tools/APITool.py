from typing import List

from examples.ExampleBase import ExampleBase
from tools.ParamBase import Params
from tools.RapidApi import RapidApi
from tools.ToolBase import ToolBase, ToolType
import pandas as pd


                
        

class ApiTool(ToolBase):

    def __init__(self, tool_name: str, tool_description: str, day_delay: int=0, apis: List[RapidApi]=[], examples: List[ExampleBase]=[]) -> None:
        super().__init__(tool_name, tool_description, ToolType.API, day_delay, examples)
        self.apis = apis

    def execute(self, selected_api_and_params: dict[str, dict[str, str]]) -> pd.DataFrame:
        results = []
        for selected_api, selected_params in selected_api_and_params.items():
            for api in self.apis:
                if api.api_name == selected_api:
                    api_signature, result = api.execute(selected_params)
                    results.append((api_signature, result))

        return results
    
    def factory(tool_config: dict) -> List:
        tool_name = tool_config.get('tool_name', '')
        tool_description = tool_config.get('tool_description', '')
        day_delay = tool_config.get('day_delay', 0)
        examples = tool_config.get('examples', [])
        
        apis_config = tool_config.get('apis', {})
        apis = []
        for api_name, api_config in apis_config.items():
            params_config = api_config.get('api_params', {})
            api_params = [Params(**param) for param in params_config.values()]
            api = RapidApi(api_name, api_config.get('api_description', ''), api_config.get('api_url', ''), api_config.get('api_method', 'GET'), api_config.get('default_headers', {}),  api_config.get('is_restful', True), api_params)
            apis.append(api)

        return ApiTool(tool_name, tool_description, day_delay, apis, examples)
    def __str__(self) -> str:
        strs = []
        strs.append(f'TOOL_NAME: {self.tool_name}')
        strs.append(f'TOOL_DESCRIPTION: {self.tool_description}')
        strs.append(f'TOOL_TYPE: {self.tool_type}')
        strs.append(f'TOOL_SYSTEM_DATE: {self.tool_system_date}')
        strs.append(f'EXAMPLES:')
        for example in self.examples:
            strs.append(str(example))
        strs.append(f'APIS:')
        for api in self.apis:
            strs.append(str(api))
        return '\n'.join(strs)
