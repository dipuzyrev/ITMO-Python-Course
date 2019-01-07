from typing import Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    """ User model with base fields """
    id: int
    first_name: str
    last_name: str
    online: int
    deactivated: Optional[str]


class User(BaseUser):
    """ User model with optional field 'bdate' """
    bdate: Optional[str]


class Message(BaseModel):
    """ Message model """
    id: int
    text: Optional[str]
    user_id: Optional[str]
    date: float
    read_state: Optional[int]
    attachments: Optional[list]
