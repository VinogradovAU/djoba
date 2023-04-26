from typing import Optional

from pydantic import BaseModel
import datetime


class Comment_base(BaseModel):
    id: int
    job_uuid: str
    comment: Optional[str] = None
    author_id: int
    performer_id: int
    is_publish: bool = True
    is_author_read: bool = False
    is_performer_read: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime


class Comment_out(Comment_base):
    user_id: int


class Comment_model_in(BaseModel):
    job_uuid: str
    comment: str
    performer_id: int
    author_id: int
