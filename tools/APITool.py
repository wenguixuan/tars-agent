from enum import Enum
import json
from typing import List

import requests
from examples.ExampleBase import ExampleBase
from tools.ToolBase import ToolBase, ToolType
import pandas as pd

class ParamsType(Enum):
    STRING = 'string'
    INTEGER = 'integer'

class Params():
    def __init__(self, param_name: str, llm_param_name: str, param_zh_name: str, param_description: str, param_type: str, param_required: bool=False, is_enum: bool=False, enum_values: List[object]=[]) -> None:
        self.param_name = param_name
        self.llm_param_name = llm_param_name
        self.param_zh_name = param_zh_name
        self.param_description = param_description
        self.param_type = param_type
        self.param_required = param_required
        self.is_enum = is_enum
        self.enum_values = enum_values

    def __str__(self) -> str:
        return f'{self.llm_param_name}: {self.param_zh_name}, {self.param_description}'
    
    def param_signature(self) -> str:
        type_annotation = f'{self.param_type} Literal[{", ".join(self.enum_values)}]' if self.is_enum else self.param_type
        return f'{self.llm_param_name}: {"" if self.param_required else "Optional["}' \
               f'{type_annotation}' \
               f'{"]" if not self.param_required else ""}'


class ApiMethod(Enum):
    GET = 'get'
    POST = 'post'


class Api():
    def __init__(self, api_name: str, api_description: str, api_url: str, api_method: ApiMethod, api_headers: dict, api_params: List[Params]) -> None:
        assert api_method in ApiMethod, f'{api_method} is not a valid API method'

        self.api_name = api_name
        self.api_description = api_description
        self.api_url = api_url
        self.api_method = api_method
        self.api_headers = api_headers
        self.api_params = api_params


    def __str__(self) -> str:
        return f'DEFINITION: {self.api_name}(' + ', '.join([param.param_signature() for param in self.api_params]) + ')' + f'   USAGE: {self.api_description}'
    

    def execute(self, selected_params: dict[str, str]) -> pd.DataFrame:

        api_signature = f"{self.api_name}(" + ", ".join([f"{param}: {selected_params[param]}" for param in selected_params]) + ")"

        result = None
        try:
            params = {

            }
            for selected_param in selected_params:
                for param in self.api_params:
                    if param.llm_param_name != selected_param:
                        continue
                    if param.is_enum:
                        assert selected_params[selected_param] in param.enum_values, f'{selected_params[selected_param]} is not in {param.enum_values}'

                    params[param.param_name] = selected_params[selected_param]

                


                if self.api_method == ApiMethod.GET:
                    response = requests.get(self.api_url, params=params, headers=self.api_headers)
                elif self.api_method == ApiMethod.POST:
                    response = requests.post(self.api_url, json=params, headers=self.api_headers)
                
                if response is response.status_code != 200:
                    result = pd.DataFrame({'Error': [f'API request failed with status code {response.status_code}, message: {response.text}']})

                else:
                    result = pd.DataFrame(json.loads(response.text))
                
        except Exception as e:
            result = pd.DataFrame({'Error': [f'API request failed with error: {e}']})

        return api_signature, result
                
        

class ApiTool(ToolBase):

    def __init__(self, tool_name: str, tool_description: str, day_delay: int=0, examples: List[ExampleBase]=[]) -> None:
        super().__init__(tool_name, tool_description, ToolType.API, day_delay, examples)

    def execute(self, selected_apis: List[Api], selected_params: dict[str, str]) -> pd.DataFrame:
        results = []
        for api in selected_apis:
            api_signature, result = api.execute(selected_params)
            results.append((api_signature, result))

        return results