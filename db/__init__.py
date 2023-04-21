from .users import users
from .jobs import jobs
from .comments import comments
from .base import metadata, engine
# from core.config import ADMIN_USERMANE, ADMIN_PASSWORD
# from models.user import User, UserIn
# import datetime
# from core.security import hashed_password

# def create_admin_user(u: UserIn) -> User:
#     print(u)
#     print(u['name'])
#     user = User(
#         name=u['name'],
#         email=u['email'],
#         hashed_password=hashed_password(u['password']),
#         is_company=u['is_company'],
#         is_admin=u['is_admin'],
#         created_at=datetime.datetime.utcnow(),
#         updated_at=datetime.datetime.utcnow()
#     )
#
#     values = {**user.dict()}
#     values.pop("id", None)
#     query = users.insert().values(**values)
#     user.id = database.execute(query)
#     return user

metadata.create_all(bind=engine)
print(f'запустился __init__.py с кодом создания таблиц postgresql')
# database.connect()
# userA = {'name': ADMIN_USERMANE,
#              'email': 'admin@djoba.ru',
#              'password': ADMIN_PASSWORD,
#              'password2': ADMIN_PASSWORD,
#              'is_company': False,
#              'is_admin': True}
# create_admin_user(u=userA)
# database.disconnect()


