

from collections import abc
from enum import Enum
from typing import List

from tools.ParamBase import Params


class ApiMethod(Enum):
    GET = 'GET'
    POST = 'POST'

class ApiBase():
    def __init__(self, api_name: str, api_description: str, api_url: str, api_method: ApiMethod, api_params: List[Params]) -> None:
        self.api_name = api_name
        self.api_description = api_description
        if api_url.endswith('/'):
            api_url = api_url[:-1]
        self.api_url = api_url
        self.api_method: ApiMethod = api_method
        self.api_params: List[Params] = api_params


    def execute(self, **kwargs):
        raise NotImplementedError('ApiBase.execute is not implemented')

    
