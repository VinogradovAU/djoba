import sqlalchemy
from .base import metadata
import datetime

comments = sqlalchemy.Table(
    'comments',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("job_uuid", sqlalchemy.String, sqlalchemy.ForeignKey("jobs.uuid"), nullable=False),
    sqlalchemy.Column("comment", sqlalchemy.String),
    sqlalchemy.Column("author_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False, default=None),
    sqlalchemy.Column("performer_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False,
                      default=None),  # юзер пишет комент к чужому объявлению, может выполнял эту работу, а может и нет.
    sqlalchemy.Column("is_publish", sqlalchemy.Boolean),
    sqlalchemy.Column("is_author_read", sqlalchemy.Boolean),
    sqlalchemy.Column("is_performer_read", sqlalchemy.Boolean),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
