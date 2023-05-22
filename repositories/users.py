from pydantic import ValidationError
from fastapi import HTTPException, status
import datetime
from typing import List, Optional

from db.base import database, metadata
from models.user import User, UserIn, UserOut, EditUserProfilData, Users_rait, Users_stars
from db.users import users, users_rait, users_stars
from repositories.base import BaseRepository
from core.security import hashed_password
from sqlalchemy import select
import uuid


class UserRepository(BaseRepository):

    async def user_status_banned_off(self, u: str, status: bool = False) -> bool:
        print(f'user_status_banned_off function')
        query = users.update().where(users.c.uuid == u).values(status_banned=status)
        return await self.database.execute(query)

    async def user_status_banned_on(self, u: str, status: bool = True) -> bool:
        print(f'user_status_banned_on function')
        query = users.update().where(users.c.uuid == u).values(status_banned=status)
        return await self.database.execute(query)

    async def user_set_status(self, u: str, status_online: bool) -> bool:
        print(f'function user_set_status')
        query = users.update().where(users.c.uuid == u).values(status_online=status_online)
        return await self.database.execute(query)

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[UserOut]:

        try:
            query = select(users.c.id,
                           users.c.uuid,
                           users.c.name,
                           users.c.email,
                           users.c.is_company,
                           users.c.is_admin,
                           users.c.status_banned,
                           users.c.status_online,
                           users.c.created_at,
                           users.c.updated_at).limit(limit).offset(skip)

            res = await database.fetch_all(query=query)
        except ValidationError as e:
            return e.json()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Что-то пошло не так!!!")
        return res

    async def users_rait_get_by_id(self, user_id: int) -> Optional[Users_rait]:
        query = users_rait.select().where(users_rait.c.user_id == user_id)
        user_r = await database.fetch_one(query=query)
        if user_r is None:
            return None
        return Users_rait.parse_obj(user_r)

    async def users_rait_create_record(self, user_id: int, new_rating: int) -> Users_rait:
        new_data = Users_rait(
            id=1,
            user_id=user_id,
            rating=new_rating,
            rait_summ=new_rating,
            coutn_rait=1,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**new_data.dict()}
        values.pop("id", None)
        query = users_rait.insert().values(**values)
        new_rait = await self.database.execute(query)
        if new_rait is None:
            return None
        return new_rait

    async def users_rait_update(self, user_id: int, new_rating: int):
        record = await self.users_rait_get_by_id(user_id=user_id)
        if record is None:
            return False
        new_summ = record.rait_summ + new_rating
        new_count = record.coutn_rait + 1
        result_rating = round(float(new_summ / new_count), 1)

        query = users_rait.update().where(users_rait.c.user_id == user_id).values(
            rait_summ=new_summ,
            coutn_rait=new_count,
            rating=result_rating)

        try:
            await self.database.execute(query)
            return True
        except Exception as e:
            return False

    async def user_stars_create_record(self, job_id: int,
                                       user_id_who: int,
                                       user_id_to_whom: int,
                                       stars: int) -> Users_stars:
        new_data = Users_stars(
            id=1,
            job_id=job_id,
            user_id_who=user_id_who,
            user_id_to_who=user_id_to_whom,
            stars=stars,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**new_data.dict()}
        values.pop("id", None)
        query = users_stars.insert().values(**values)
        new_record = await self.database.execute(query)
        if new_record is None:
            return None
        return new_record

    async def update_user_raiting(self, user_id: int) -> bool:
        user_r = await self.users_rait_get_by_id(user_id=user_id)
        if user_r is None:
            return False
        query = users.update().where(users.c.id == user_id).values(rating=user_r.rating)
        try:
            await self.database.execute(query=query)
        except Exception as e:
            return False
        return True

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
            uuid=u.uuid,
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
        user = await self.database.execute(query)
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

    async def update_user_from_form_profil(self, id: int, u: EditUserProfilData) -> Optional[bool]:
        user_data = EditUserProfilData(
            name=u.name,
            email=u.email,
            phone=u.phone,
            is_company=u.is_company,
            updated_at=datetime.datetime.utcnow(),
        )
        values = {**user_data.dict()}
        query = users.update().where(users.c.id == id).values(**values)
        # создаем запись в таблице jobs
        try:
            await self.database.execute(query=query)
        except Exception as e:
            return False
        return True
