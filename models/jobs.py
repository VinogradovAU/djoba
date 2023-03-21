from pydantic import BaseModel, condecimal, Field, conint
from typing import Union, Optional, List
import datetime
from uuid import UUID
from models.user import User


class BaseJob(BaseModel):
    title: str
    description: str
    price: condecimal(max_digits=17, decimal_places=2) = Field(default=0)
    address: str
    city: str
    phone: str
    metrostation: Optional[str] = None
    is_active: bool = True  # объявление можно заблокировать, снять с публикации. эделает не Юзер
    is_publish: bool = False  # при создании объявление оно в режиме черновика. чтобы опубликовать надо True сделать,
    # при условии, что is_active = True.
    # если у опубликованного объявления истек срок, то is_puslish становтся False и объявление видно только в профиле
    is_expired_time: bool = False  # флаг истечения времени публикации


class Jobs_model(BaseJob):
    uuid: str
    id: Union[UUID, int, str]
    user_id: int
    is_booking: Optional[bool] = False
    created_at: datetime.datetime
    updated_at: datetime.datetime


class JobIn_model(BaseModel):
    title: str
    description: str
    price: condecimal(max_digits=17, decimal_places=2) = Field(default=0)
    address: str
    city: str
    phone: str
    metrostation: Optional[str] = None
    expired_day: conint(gt=0, lt=8)


class JobOut_model(BaseJob):
    uuid: str
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


# данне для таблицы которая хранит ID объявления и дату когда надо снять его с публикации
class Active_job(BaseModel):
    job_uuid: str
    disactivate_date: datetime.datetime
    # performer_id: int = None


class CreateJobIn(BaseModel):
    errors: List = []
    title: str
    description: str
    price: condecimal(max_digits=17, decimal_places=2) = Field(default=0)
    address: str
    city: str
    metrostation: Optional[str] = None
    phone: str
    expired_day: conint(gt=0, lt=8)
    button: str
    resp: bool = False
    is_booking: Optional[bool] = False

class Jobs_model_join(Jobs_model, Active_job, User):
    pass

class Booking_job_model(BaseModel):
    id: int
    job_uuid: str
    user_id: int