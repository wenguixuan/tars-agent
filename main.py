


from agents.TarsBase import TarsBase
from config.ConfigLoader import ConfigLoader
from utils.Log import Log
from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage


if __name__ == "__main__":
    config_loader = ConfigLoader(base_url='config/yaml')
    llm_config = config_loader.read_yaml("llm.yaml")
    logger = Log()

    tars = TarsBase()
    logger.info(tars)

    # model = ChatOpenAI(model=llm_config['default_model']['model_name'], 
    #                    base_url=llm_config['default_model']['base_url'], 
    #                    api_key=llm_config['default_model']['api_key'])
    
    # response = model.invoke([HumanMessage(content="Hi! I'm Bob")])

    # logger.info(response.content)
    