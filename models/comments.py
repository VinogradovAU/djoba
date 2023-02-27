from pydantic import BaseModel, condecimal, Field, conint
from typing import Union, Optional, List
import datetime
from uuid import UUID
from models.user import User
from models.jobs import Jobs_model

class Comment_model(BaseModel):
    id: int
    job_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class comment_out(Comment_model):
    user_id: int