

from tools.ApiBase import ApiMethod
from tools.ParamBase import Params, ParamsType
from tools.RapidApi import RapidApi
from tools.ToolBase import ToolBase


if __name__ == '__main__':
    base_path = 'config/yaml/'
    yaml_path = 'RapidApiTool.yaml'
    tools = ToolBase.import_tools_from_yaml(base_path, yaml_path)
    for tool in tools:
        print(tool)

    selected_api_and_params = {
        'current_weather': {'city': 'beijing', 'lang': 'ZH'}
    }
    results = tools[1].execute(selected_api_and_params)
    print(results)
    
