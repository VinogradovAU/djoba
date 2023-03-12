import sqlalchemy
from db.base import metadata
import datetime

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("uuid", sqlalchemy.String, unique=True),
    sqlalchemy.Column("email", sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
    sqlalchemy.Column("is_company", sqlalchemy.Boolean),
    sqlalchemy.Column("is_admin", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("status_banned", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("status_online", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("rating", sqlalchemy.DECIMAL(3, 1), default=0.0),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)

# rating - рейтин юзера будет расчитываться когда другой юзер будет ставить оценку
# после выполения договоренностей (работа или предоставление работы) от 1 до 5 звезд
