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
    phone: Optional[str] = None
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
    phone: Optional[str] = None
    expired_day: conint(gt=0, lt=8)
    button: str
    resp: bool = False
    is_booking: Optional[bool] = False


class Booking_job_model(BaseModel):
    id: int
    job_uuid: str
    user_id: int


class Jobs_model_join(Jobs_model, Active_job, User, Booking_job_model):
    b_count: int


class Model_list_jobs_join(BaseModel):
    jobs_id: int
    jobs_uuid: str
    jobs_user_id: int
    jobs_title: str
    jobs_description: str
    jobs_address: str
    jobs_city: str
    jobs_phone: str
    jobs_metrostation: str
    jobs_price: condecimal(max_digits=17, decimal_places=2) = Field(default=0)
    jobs_is_active: bool
    jobs_is_publish: bool
    jobs_is_expired_time: bool
    jobs_is_booking: bool
    jobs_created_at: datetime.datetime
    jobs_updated_at: datetime.datetime
    active_jobs_id: int
    active_jobs_job_uuid: str
    active_jobs_performer_confirmed: Optional[int] = None
    active_jobs_disactivate_date: datetime.datetime
    users_id: int
    users_uuid: str
    users_name: str
    users_phone: Optional[str] = ''
    users_status_banned: bool
    users_rating: Optional[float] = 0.0
    booking_b_count: Optional[int] = None


class Close_job(BaseModel):
    uuid_job: str
    user_id: str
    text_area_cancel: Optional[str] = ''
