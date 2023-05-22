import datetime
from typing import Optional, Union
from uuid import UUID
import phonenumbers

from pydantic import BaseModel, EmailStr, validator, constr, Field


class User(BaseModel):
    id: Optional[int] = None
    uuid: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    hashed_password: str
    is_company: bool = False
    status_banned: bool = False
    status_online: bool = False
    rating: Optional[float] = 0.0
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


class EditUserProfilData(BaseModel):
    name: str
    email: EmailStr
    phone: str
    is_company: Union[bool, None] = False

    @validator("phone")
    def phone_validation(cls, v):
        try:
            x = phonenumbers.parse(v, None)
        except Exception as e:
            raise ValueError("phonenumbers don't match")
        return v

class Users_rait(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    rating: float = 0.0
    rait_summ: float = 0.0
    coutn_rait: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

class Users_stars(BaseModel):
    id: Optional[int] = None
    job_id: int
    user_id_who: int
    user_id_to_who: int
    stars: int = Field(..., gt=0, le=5)
    created_at: datetime.datetime
    updated_at: datetime.datetime


@validator("password2")
async def password_match(cls, v, values, **kwargs):
    if "password" in values and v != values["password"]:
        raise ValueError("password don't match")
    return v
