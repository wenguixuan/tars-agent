#!/usr/bin/env python
import time
from typing import List, Union
from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel, Field
import uvicorn
from agents.TarsApiWorker import TarsApiWorker
from agents.TarsManager import TarsManager
from config.ConfigLoader import ConfigLoader
from langchain_core.runnables import RunnableLambda
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from tools.ToolBase import ToolBase
from utils.Log import Log

def chat(user_request):

    base_path = 'config/yaml/'
    tool_yaml_path = 'RapidApiTool.yaml'

    config_loader = ConfigLoader(base_url=base_path)
    llm_config = config_loader.read_yaml("llm.yaml")
    logger = Log()
    
    tools = ToolBase.import_tools_from_yaml(base_path, tool_yaml_path)
    workers = []
    for idx, tool in enumerate(tools):
        worker = TarsApiWorker(name=f'worker_{idx}', tool=tool, llm_config=llm_config['manager'])
        workers.append(worker)

    manager = TarsManager(name='manager', workers=workers, llm_config=llm_config['manager'])
    final_answer = manager.answer(user_request)
    return final_answer

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple api server using Langchain's Runnable interfaces",
)


def chat_service(chat_historys: dict):
    start_time = time.time()
    messages: List = chat_historys.get('undefined', [])
    user_request = messages[-1].get('content')
    final_answer = chat(user_request)
    end_time = time.time()

    elapsed_time = end_time - start_time

    final_answer = f"{final_answer}\n TimeUsed: {elapsed_time:.2f} seconds"
    return final_answer

chain = RunnableLambda(chat_service)

add_routes(
    app,
    chain,
    path="/tars",
    playground_type='chat',
    
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8100)
