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
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)

active_jobs = sqlalchemy.Table(
    'active_jobs',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("job_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id"), nullable=False),
    sqlalchemy.Column("disactivate_date", sqlalchemy.DateTime),
)