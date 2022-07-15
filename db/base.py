from databases import Database
from sqlalchemy import create_engine, MetaData
from core.config import DATABASES_URL

database = Database(DATABASES_URL) # объект для подключения к базе
metadata = MetaData() # объект для создания таблиц
engine = create_engine(
    DATABASES_URL,
)

