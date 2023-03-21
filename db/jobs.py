from enum import unique
import sqlalchemy
from .base import metadata
import datetime
from sqlalchemy_utils import UUIDType
import uuid
from sqlalchemy.dialects.postgresql import UUID

jobs = sqlalchemy.Table(
    'jobs',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("uuid", sqlalchemy.String, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("address", sqlalchemy.String),
    sqlalchemy.Column("city", sqlalchemy.String),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("metrostation", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Float),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean),
    sqlalchemy.Column("is_publish", sqlalchemy.Boolean),
    sqlalchemy.Column("is_expired_time", sqlalchemy.Boolean),
    sqlalchemy.Column("is_booking", sqlalchemy.Boolean), # забронирована или нет
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)

active_jobs = sqlalchemy.Table(
    'active_jobs',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("job_uuid", sqlalchemy.String, sqlalchemy.ForeignKey("jobs.uuid"), nullable=False),
    sqlalchemy.Column("performer_confirmed", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True,
                      default=None), #юзер взявший работу в резуьтате. создатель услуги жмет на кнопку
    sqlalchemy.Column("disactivate_date", sqlalchemy.DateTime),
)

# performer_id - исполнитель работы. появится когда юзер желающий исполнить работу нажмет кнопку бронирования
# performer_confirmed - хозяин джобы подтверждает отдать работу юзеру-исполнителю

booking_job = sqlalchemy.Table(
    'booking_job',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("job_uuid", sqlalchemy.String, sqlalchemy.ForeignKey("jobs.uuid"), nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True,
                      default=None), #юзер который хочет выполнить работу - кандидат
)
