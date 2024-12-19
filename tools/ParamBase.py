from enum import Enum
from typing import List


class ParamsType(Enum):
    STRING = 'STRING'
    INTEGER = 'INTEGER'

class Params():
    def __init__(self, param_name: str, llm_param_name: str, param_zh_name: str, param_description: str, param_type: str, param_required: bool=False, is_enum: bool=False, enum_values: List[object]=[]) -> None:
        self.param_name = param_name
        self.llm_param_name = llm_param_name
        self.param_zh_name = param_zh_name
        self.param_description = param_description
        if param_type in [ParamsType.STRING.value, ParamsType.INTEGER.value]:   
            self.param_type = param_type
        else:
            raise ValueError(f'Invalid param type: {param_type}')
        self.param_type: ParamsType = ParamsType(param_type)
        self.param_required = param_required
        self.is_enum = is_enum
        self.enum_values = enum_values

    def __str__(self) -> str:
        return f'{self.llm_param_name}: {self.param_zh_name}, {self.param_description}'
    
    def param_signature(self) -> str:
        type_annotation = f'{self.param_type.value} Literal[{", ".join(self.enum_values)}]' if self.is_enum else self.param_type.value
        return f'{self.llm_param_name}: {"" if self.param_required else "Optional["}' \
               f'{type_annotation}' \
               f'{"]" if not self.param_required else ""}'
    

if __name__ == '__main__':
    param = Params('param_name', 'llm_param_name', 'param_zh_name', 'param_description', ParamsType.STRING, True, False, [])
    print(param)
    print(param.param_signature())