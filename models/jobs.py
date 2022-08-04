from pydantic import BaseModel
from typing import Union
import datetime
from uuid import UUID


class BaseJob(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True


class jobs_model(BaseJob):
    uuid: str
    id: Union[UUID, int, str]
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class jobIn_model(BaseJob):
    pass

class jobOut_model(BaseJob):
    uuid: str
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime