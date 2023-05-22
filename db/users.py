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

users_rait = sqlalchemy.Table(
    'users_rait',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("rating", sqlalchemy.DECIMAL(3, 1), default=0.0),  # рассчитаный рейтинг
    sqlalchemy.Column("rait_summ", sqlalchemy.Integer, default=0),  # общая сумма оценок - звезд
    sqlalchemy.Column("coutn_rait", sqlalchemy.Integer, default=0),  # количество проголосовавших
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)

users_stars = sqlalchemy.Table(
    'users_stars',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("job_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id"), nullable=False),
    sqlalchemy.Column("user_id_who", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("user_id_to_whom", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False),
    sqlalchemy.Column("stars", sqlalchemy.Integer, default=0),  # сколько звезд поставил
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
