from pydantic import BaseModel
import datetime


class BaseJob(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True


class jobs_model(BaseJob):
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class jobIn_model(BaseJob):
    pass
