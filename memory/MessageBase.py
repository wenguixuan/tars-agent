

from enum import Enum
from typing import Union
from pydantic import BaseModel

class MessageType(Enum):
    SOLUTION = 'solution'
    INFORMATION = 'information'
    ACTION = 'action'
    WARNING = 'warning'
    ERROR = 'error'


class MessageBase(BaseModel):
    sender_id: Union[str, None]
    sender_name: Union[str, None]
    sender_role: Union[str, None]
    receiver_id: Union[str, None]
    receiver_name: Union[str, None]
    receiver_role: Union[str, None]
    content: Union[str, None]
    type: MessageType
