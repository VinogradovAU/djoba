from pydantic import BaseModel
import datetime

class Comment_base(BaseModel):
    id: int
    job_uuid: str
    comment: str
    performer_id: int
    is_publish: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Comment_out(Comment_base):
    user_id: int


class Comment_model_in(BaseModel):
    job_uuid: str
    comment: str
    performer_id: int
