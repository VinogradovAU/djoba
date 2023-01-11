import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator, constr


class User(BaseModel):
    id: Optional[int] = None
    uuid: str
    name: str
    email: EmailStr
    hashed_password: str
    is_company: bool = False
    status_online: bool = False
    is_admin: bool = False
    created_at: Optional[datetime.datetime] = None
    updated_at: datetime.datetime


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False


class UserOut(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    is_company: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


@validator("password2")
async def password_match(cls, v, values, **kwargs):
    if "password" in values and v != values["password"]:
        raise ValueError("password don't match")
    return v
