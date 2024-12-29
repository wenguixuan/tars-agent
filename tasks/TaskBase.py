from enum import Enum
from typing import Dict, List

from examples.ExampleBase import ExampleBase
from langchain_core.output_parsers import JsonOutputParser

class TaskStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'

class TaskBase(object):
    def __init__(self, context:Dict[str, str], instruction: str, precautions: List[str]=[], examples: List[ExampleBase] = [], output_parser: JsonOutputParser=None, identifier='***') -> None:
        self.identifier = identifier
        self.context = context
        if len(context) == 0:
            self.context_str = ''
        else:
            tmp_strs = []
            for key in context:
                upper_key = key.upper()
                tmp_strs.append(f"{self.identifier}{upper_key}{self.identifier}: {context[key]}")
            self.context_str = '\n'.join(tmp_strs)

        self.instruction = instruction
        self.precautions = precautions
        self.examples = examples

        if len(self.examples) == 0:
            self.examples_str  = "No reference examples yet."
        else:
            tmp_strs = []
            for example_idx, example in enumerate(self.examples):
                tmp_strs.append(f"EXAMPLE {example_idx+1}: INPUT: {example.input} OUTPUT: {example.output}")
            self.examples_str  = '\n'.join(tmp_strs)

        if len(self.precautions) == 0:
            self.precautions_str = 'No precautions.'
        else:
            self.precautions_str = '\n'.join([f"{idx+1}. {caution}" for idx, caution in enumerate(self.precautions)])

        self.output_parser = output_parser
        if output_parser is not None:
            self.format_instructions = output_parser.get_format_instructions()
        else:
            self.format_instructions = 'No specific output requirements.'

        self.raw_answer = None
        self.formatted_answer = None
        self.status = TaskStatus.NOT_STARTED

        self.task_description = f"{self.context_str}\n{self.identifier}INSTRUCTION{self.identifier}:\n{self.instruction}\n{self.identifier}REFERENCE EXAMPLES{self.identifier}: \n{self.examples_str}\n{self.identifier}OUTPUT FORMAT{self.identifier}\n{self.format_instructions}\n{self.identifier}PRECAUTIONS{self.identifier}:\n{self.precautions_str}\n"

    def set_answer(self, raw_answer: str):
        self.raw_answer = raw_answer
        if self.output_parser is not None:
            try:
                self.formatted_answer = self.output_parser.parse(raw_answer)
                self.status = TaskStatus.SUCCESS
            except Exception as e:
                raise Exception(f'Output format error, You can check the output format instructions!')
                
        else:
            self.formatted_answer = raw_answer
            self.status = TaskStatus.SUCCESS
            
