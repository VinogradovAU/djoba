from .users import users
from .jobs import jobs
from .base import metadata, engine

metadata.create_all(bind=engine)
print(f'запустился __init__.py с кодом созданиятаблиц postgresql')