from pydantic import ValidationError
from fastapi import HTTPException, status
import datetime
from typing import List, Optional

from db.base import database, metadata
from models.user import User, UserIn, UserOut
from db.users import users
from repositories.base import BaseRepository
from core.security import hashed_password
from sqlalchemy import select
import uuid


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[UserOut]:

        try:
            query = select(users.c.id, users.c.name, users.c.email, users.c.is_company, users.c.created_at,
                           users.c.updated_at).limit(limit).offset(skip)

            res = await database.fetch_all(query=query)
        except ValidationError as e:
            return e.json()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Что-то пошло не так!!!")
        return res

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id)
        user = await database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def get_by_uuid(self, uuid: str) -> Optional[User]:
        query = users.select().where(users.c.uuid == uuid)
        user = await database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserIn) -> Optional[User]:
        my_uuid = str(uuid.uuid4())
        user = User(
            uuid=my_uuid,
            name=u.name,
            email=u.email,
            hashed_password=hashed_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user = await self.database.execute(query)
        if user is None:
            return None
        return user

    async def update_user(self, id: int, u: UserIn) -> User:
        user = User(
            id=id,
            name=u.name,
            email=u.email,
            hashed_password=hashed_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = users.update().where(users.c.id == id).values(**values)
        await self.database.execute(query)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == email)
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create_user_from_formtemplate(self, u: UserIn) -> Optional[User]:
        user = User(
            name=u.name,
            uuid=u.uuid,
            email=u.email,
            hashed_password=hashed_password(u.hashed_password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        values = {**user.dict()}
        values.pop("id", None)
        query = users.insert().values(**values)
        user = await self.database.execute(query)
        if user is None:
            return None
        return user