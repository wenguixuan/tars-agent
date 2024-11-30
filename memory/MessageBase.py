

from enum import Enum
from pydantic import BaseModel

class MessageType(Enum):
    SOLUTION = 'solution'
    INFORMATION = 'information'
    ACTION = 'action'
    WARNING = 'warning'
    ERROR = 'error'


class MessageBase(BaseModel):
    sender_id: str
    sender_name: str
    sender_role: str
    receiver_id: str
    receiver_name: str
    receiver_role: str
    content: str
    type: MessageType
