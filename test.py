

import json
import sys

from langserve import RemoteRunnable
from agents.TarsApiWorker import TarsApiWorker
from agents.TarsManager import ActionType, ManagerAnswer, TarsManager
from tools.ApiBase import ApiMethod
from tools.ParamBase import Params, ParamsType
from tools.RapidApi import RapidApi
from tools.ToolBase import ToolBase
from utils.Log import Log
from utils.format_dataframe import df_format
from config.ConfigLoader import ConfigLoader


if __name__ == '__main__':

    # user_request = sys.argv[1]

    # base_path = 'config/yaml/'
    # tool_yaml_path = 'RapidApiTool.yaml'

    # config_loader = ConfigLoader(base_url=base_path)
    # llm_config = config_loader.read_yaml("llm.yaml")
    # logger = Log()
    
    # tools = ToolBase.import_tools_from_yaml(base_path, tool_yaml_path)
    # workers = []
    # for idx, tool in enumerate(tools):

    #     worker = TarsApiWorker(name=f'worker_{idx}', tool=tool, llm_config=llm_config['manager'])
    #     workers.append(worker)

    # manager = TarsManager(name='manager', workers=workers, llm_config=llm_config['manager'])
    # manager.answer(user_request)



    joke_chain = RemoteRunnable("http://localhost:8100/joker/")

    joke_chain.invoke({"topic": "parrots"})

    
    
