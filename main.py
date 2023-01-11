import datetime

from fastapi.staticfiles import StaticFiles
import fastapi
from models.user import User
from core.config import ADMIN_USERMANE, ADMIN_PASSWORD, ADMIN_EMAIL
from core.security import hashed_password
from db.base import database
import uvicorn
from endpoints import users, auth, jobs, main_page, profile
from fastapi.middleware.cors import CORSMiddleware
from db.users import users as db_users
import uuid

app = fastapi.FastAPI(title="Djoba Project")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://192.168.1.10:8000",
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
app.include_router(main_page.router, prefix="", tags=["mainpage"])
app.include_router(profile.router, prefix="", tags=["profile"])
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    await database.connect()
    query = db_users.select().where(db_users.c.email == ADMIN_EMAIL)
    user = await database.fetch_one(query=query)
    if user is None:
        #----------------------------------
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
        #----------------------------------

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
