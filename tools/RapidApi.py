import json
import traceback
from typing import List, Tuple

import pandas as pd
import requests
from tools.ApiBase import ApiBase, ApiMethod
from tools.ParamBase import Params, ParamsType


class RapidApi(ApiBase):
    def __init__(self, api_name: str, api_description: str, api_url: str, api_method: str, default_headers: dict = {}, api_params: List[Params] = []) -> None:
        api_method = ApiMethod(api_method)
        super().__init__(api_name, api_description, api_url, api_method, api_params)
        self.default_headers = default_headers

    def __str__(self) -> str:
        return f'DEFINITION: {self.api_name}(' + ', '.join([param.param_signature() for param in self.api_params]) + ')' + f'   USAGE: {self.api_description}'
    

    def execute(self, selected_params: dict[str, str]) -> Tuple[str, pd.DataFrame]:
        print(f'selected_params: {selected_params}')
        api_signature = f"{self.api_name}(" + ", ".join([f"{param}={selected_params[param]}" for param in selected_params]) + ")"
        
        restful_url = self.api_url
        result = None
        try:
            for param in self.api_params:
                if param.llm_param_name not in selected_params:
                    assert False, f'{param.llm_param_name} is required'
                if param.is_enum:
                    assert selected_params[param.llm_param_name] in param.enum_values, f'{selected_params[param.llm_param_name]} is not in {param.enum_values}'

                restful_url += f"/{selected_params[param.llm_param_name]}" 

            if self.api_method == ApiMethod.GET:
                response = requests.get(restful_url, headers=self.default_headers)
                if response.status_code != 200:
                    raise Exception(f'response: {response.text}')
            else:
                raise NotImplementedError('RapidApi.execute only supports GET method')
            print("response.text: ", response.text)
            result = pd.DataFrame(json.loads(response.text))
        except Exception as e:
            traceback.print_exc()
            print(restful_url)
            result = pd.DataFrame({'Error': [f'API request failed with error: {e}']})

        return api_signature, result

    


