


from typing import List
from agents.TarsBase import TarsBase
from config.ConfigLoader import ConfigLoader
from tasks.TaskBase import TaskBase
from utils.Log import Log

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI


# Define your desired data structure.
class Paper(BaseModel):
    title: str = Field(description="the title of your paper.")
    keyword: List[str] = Field(description="3 to 5 theme keywords of your paper.")
    paragraphs: List[str] = Field(description="the paragraphs of your paper.")


if __name__ == "__main__":
    config_loader = ConfigLoader(base_url='config/yaml')
    llm_config = config_loader.read_yaml("llm.yaml")
    logger = Log()

    logger.info(llm_config)
    name = 'tars'
    role = "You are a Chinese language teacher."

    context = {
        "topic": "长久以来，人们只能看到月球固定朝向地球的一面，“嫦娥四号”探月任务揭开了月背的神秘面纱；随着“天问一号”飞离地球，航天人的目光又投向遥远的深空……正如人类的太空之旅，我们每个人也都在不断抵达未知之境。",
        "precaution": "要求：选准角度，确定立意，明确文体，自拟标题；不要套作，不得抄袭；不得泄露个人信息；800字左右。"
        }
    
    instruction = "这引发了你怎样的联想与思考？请写一篇文章。"

    output_parser = JsonOutputParser(pydantic_object=Paper)

    task = TaskBase(context=context, instruction=instruction, output_parser=output_parser)
    tars = TarsBase(name=name, role=role, llm_config=llm_config['default_model'])
    task_with_answer = tars.answer(task)

    logger.info(task_with_answer.status)
    logger.info(task_with_answer.formatted_answer)

    
    # response = model.invoke([HumanMessage(content="Hi! I'm Bob")])

    # logger.info(response.content)
    