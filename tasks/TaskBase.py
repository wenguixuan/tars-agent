from enum import Enum
from typing import Dict, List

from examples.ExampleBase import ExampleBase

class TaskStatus(Enum):
    NOT_STARTED = 'NOT_STARTED'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'

class TaskBase(object):
    def __init__(self, context:Dict[str, str], instruction: str, examples: List[ExampleBase] = [], output_parser=None, identifier='***') -> None:
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

        self.examples = examples

        if len(examples) == 0:
            self.examples_str  = "No reference examples yet."
        else:
            tmp_strs = []
            for example_idx, example in enumerate(examples):
                tmp_strs.append(f"EXAMPLE {example_idx+1}: INPUT: {example.input} OUTPUT: {example.output}")
            self.examples_str  = '\n'.join(tmp_strs)

        self.output_parser = output_parser
        if output_parser is not None:
            self.format_instructions = output_parser.get_format_instructions()
        else:
            self.format_instructions = 'No specific output requirements.'

        self.answer = None
        self.status = TaskStatus.NOT_STARTED


        self.task_description = f"{self.identifier}REFERENCE EXAMPLES{self.identifier}: \n{self.examples_str}\n{self.context_str}\n{self.identifier}INSTRUCTION{self.identifier}:\n{self.instruction}\n***OUTPUT FORMAT***\n{self.format_instructions}\n"



