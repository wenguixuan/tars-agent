

from agents.TarsApiWorker import TarsApiWorker
from tools.ApiBase import ApiMethod
from tools.ParamBase import Params, ParamsType
from tools.RapidApi import RapidApi
from tools.ToolBase import ToolBase
from utils.Log import Log
from utils.format_dataframe import df_format
from config.ConfigLoader import ConfigLoader


if __name__ == '__main__':
    base_path = 'config/yaml/'
    tool_yaml_path = 'RapidApiTool.yaml'

    config_loader = ConfigLoader(base_url=base_path)
    llm_config = config_loader.read_yaml("llm.yaml")
    logger = Log()
    
    tools = ToolBase.import_tools_from_yaml(base_path, tool_yaml_path)
    workers = []
    for tool in tools:
        print(tool)

        worker = TarsApiWorker(tool=tool, llm_config=llm_config['default_model'])
        message = worker.answer(sender_id='-1', sender_name='TarsManager', sender_role='manager',
                      request='FGI指数是多少', is_plan=False, is_execute=True)
        print(message)
        print("="*10)
        break

    




    # selected_api_and_params = {
    #     'current_weather': {'city': 'shenzhen', 'lang': 'ZH'}
    # }
    # results = tools[1].execute(selected_api_and_params)
    # for result in results:
    #     df = df_format(result[1], max_column=result[1].shape[1])
    #     print(df)
    
