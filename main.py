import datetime
from fastapi import Request, Depends
from fastapi.staticfiles import StaticFiles
import fastapi
from models.user import User
from core.config import ADMIN_USERMANE, ADMIN_PASSWORD, ADMIN_EMAIL
from core.security import hashed_password, decode_access_token, manager
from db.base import database
import uvicorn
from endpoints import users, auth, jobs, main_page, profile
from endpoints.api import jobs_api
from fastapi.middleware.cors import CORSMiddleware
from db.users import users as db_users
import uuid
from endpoints.depends import get_current_user

app = fastapi.FastAPI(title="Djoba Project")
app.mount("/static", StaticFiles(directory="static"), name="static")

pool_managed_object = {}  # словарь {token:manager} по токену мы достаем объект manager

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8001",
    "http://192.168.1.34:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(jobs_api.router, prefix="/jobs", tags=["jobs_api"])
app.include_router(main_page.router, prefix="", tags=["mainpage"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print(f'сработал middleware')
    # try:
    access_token = request.cookies.get('access_token')
    print(f'cookies содержат token: {access_token}')
    request.state.user_is_anonymous = True
    request.state.user_is_authenticated = False

    if access_token is None:
        # print(f'token протух')
        manager.autorization = False
        manager.set_cookie = False
        manager.user = None
        manager.user_status = "offline"
        manager.access_token = ''
    else:
        if access_token in manager.resp:
            # токен есть в словаре (он там появляется после логирования юзера)
            # проверяем токен
            decode_token = decode_access_token(access_token)
            print(f'decode_token: {decode_token}')
            if decode_token is None:
                # неверный токен или истек срок действия
                manager.autorization = False
                manager.set_cookie = False
                request.cookies.clear()
                print(f'token протух')
            else:

                print(f'decode_token: {decode_token["sub"]}')
                print(f'token НЕ протух')
                # достанем юзера из бд по емаил из токена
                user_email = decode_token["sub"]
                user = await get_current_user(access_token)
                manager.user = user
                manager.autorization = True
                manager.set_cookie = True
                manager.user_status = 'Online'
                request.state.user_is_anonymous = False
                request.state.user_is_authenticated = True
                request.state.user = user
                request.state.access_token = access_token

        else:
            # print(f'в куках пришел неверный токен')
            manager.autorization = False
            manager.set_cookie = False
            manager.user = None
            manager.user_status = "offline"
            manager.access_token = ''
            request.cookies.clear()


        # except Exception as e:
        #     print(f'middleware ошибка проверки token')
        #     manager.autorization = False
        #     manager.set_cookie = False
    response = await call_next(request)

    return response


@app.on_event("startup")
async def startup():
    await database.connect()
    query = db_users.select().where(db_users.c.email == ADMIN_EMAIL)
    user = await database.fetch_one(query=query)
    if user is None:
        # ----------------------------------
        my_uuid = str(uuid.uuid4())
        # print(my_uuid)
        user = User(
            name=ADMIN_USERMANE,
            uuid=my_uuid,
            email=ADMIN_EMAIL,
            hashed_password=hashed_password(ADMIN_PASSWORD),
            is_company=False,
            is_admin=True,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**user.dict()}
        values.pop("id", None)
        query = db_users.insert().values(**values)
        user.id = await database.execute(query)
        # ----------------------------------


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, host="0.0.0.0", reload=True)
