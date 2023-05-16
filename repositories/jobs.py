from repositories.base import BaseRepository
from models.jobs import Jobs_model, JobIn_model, JobOut_model, CreateJobIn, Active_job, Booking_job_model
from models.user import User
from db.jobs import jobs, active_jobs, booking_job
from db.users import users
from typing import List, Optional
import datetime
from fastapi import HTTPException, status
from pydantic import ValidationError
import uuid
from sqlalchemy import select, func, nullslast


class JobRepositoryes(BaseRepository):

    async def get_userinfo_by_uuid_job(self, uuid_job: str) -> str:
        query = jobs.select().where(jobs.c.uuid == uuid_job)
        job = await self.database.fetch_one(query=query)
        if job is None:
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="phone not found")
            return False
        query = users.select().where(users.c.id == job.user_id)
        user = await self.database.fetch_one(query=query)
        if user is None:
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="phone not found")
            return False
        return User.parse_obj(user)

    async def get_phone_by_jobuuid(self, uuid: str) -> str:
        query = jobs.select().where(jobs.c.uuid == uuid)
        job = await self.database.fetch_one(query=query)
        if job is None:
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="phone not found")
            return False
        print(f'job---> {job}')
        return job.phone

    async def job_id_publish_change(self, uuid: str, new_publish: bool = False) -> bool:
        print(f'job_is_publish_change function')
        query = jobs.update().where(jobs.c.uuid == uuid).values(is_publish=new_publish)
        try:
            await self.database.execute(query)
            return True
        except Exception as e:
            return False

    async def update_job_from_html(self,
                                   joba: Jobs_model,
                                   j: CreateJobIn, is_publish: bool) -> Jobs_model:

        job = Jobs_model(
            uuid=joba.uuid,
            id=joba.id,
            user_id=joba.user_id,
            title=j.title,
            description=j.description,
            price=j.price,
            address=j.address,
            city=j.city,
            phone=j.phone,
            metrostation=j.metrostation,
            is_active=joba.is_active,
            is_publish=is_publish,
            is_expired_time=False,
            is_booking=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**job.dict()}
        values.pop("id", None)
        query = jobs.update().where(jobs.c.id == joba.id).values(**values)
        # создаем запись в таблице jobs
        await self.database.execute(query=query)

        # вычисляем время когда объявление(запрос) должен быть снят с публикации - типа вышло время
        new_expired_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=j.expired_day * 24 * 60)
        activ_job = Active_job(
            job_uuid=job.uuid,
            disactivate_date=new_expired_time.strftime("%Y-%m-%d %H:%M")
        )
        # создаем запись в таблице active_jobs
        query = active_jobs.update().where(active_jobs.c.job_uuid == job.uuid).values(**{**activ_job.dict()})
        await self.database.execute(query=query)
        return job

    async def create_job_from_html(self, user_id: int,
                                   j: CreateJobIn, is_publish: bool) -> Jobs_model:
        job_uuid = str(uuid.uuid4())
        job = Jobs_model(
            uuid=job_uuid,
            id=0,
            user_id=user_id,
            title=j.title,
            description=j.description,
            price=j.price,
            address=j.address,
            city=j.city,
            phone=j.phone,
            metrostation=j.metrostation,
            is_active=True,
            is_publish=is_publish,
            is_expired_time=False,
            is_booking=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**job.dict()}
        values.pop("id", None)
        query = jobs.insert().values(**values)
        # создаем запись в таблице jobs
        job.id = await self.database.execute(query=query)

        # вычисляем время когда объявление(запрос) должен быть снят с публикации - типа вышло время
        new_expired_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=j.expired_day * 24 * 60)
        activ_job = Active_job(
            job_uuid=job.uuid,
            disactivate_date=new_expired_time.strftime("%Y-%m-%d %H:%M")
        )
        # создаем запись в таблице active_jobs
        query = active_jobs.insert().values(**{**activ_job.dict()})
        await self.database.execute(query=query)
        return job

    async def create_job(self, user_id: int, j: JobIn_model) -> Jobs_model:
        my_uuid = str(uuid.uuid4())
        # print(f'my_uuid: {my_uuid}')
        job = Jobs_model(
            uuid=my_uuid,
            id=0,
            user_id=user_id,
            title=j.title,
            description=j.description,
            price=j.price,
            address=j.address,
            city=j.city,
            phone=j.city,
            metrostation=j.metrostation,
            is_active=True,
            is_publish=True,
            is_expired_time=j.is_expired_time,
            is_booking=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow())
        values = {**job.dict()}
        values.pop("id", None)
        query = jobs.insert().values(**values)
        job.id = await self.database.execute(query=query)
        return job

    async def get_list_jobs(self, limit: int = 100, skip: int = 0) -> List[Jobs_model]:

        query = f'''SELECT jobs.id as "jobs_id",
                jobs.uuid as "jobs_uuid",
                jobs.user_id as "jobs_user_id",
                jobs.title as "jobs_title",
                jobs.description as "jobs_description",
                jobs.address as "jobs_address",
                jobs.city as "jobs_city",
                jobs.phone as "jobs_phone",
                jobs.metrostation as "jobs_metrostation",
                jobs.price as "jobs_price",
                jobs.is_active as "jobs_is_active",
                jobs.is_publish as "jobs_is_publish",
                jobs.is_expired_time as "jobs_is_expired_time",
                jobs.is_booking as "jobs_is_booking",
                jobs.created_at as "jobs_created_at",
                jobs.updated_at as "jobs_updated_at",
                active_jobs.id as active_jobs_id,
                active_jobs.job_uuid as active_jobs_job_uuid,
                active_jobs.performer_confirmed as active_jobs_performer_confirmed,
                active_jobs.disactivate_date as active_jobs_disactivate_date,
                users.id as users_id,
                users.uuid as users_uuid,
                users.name as users_name,
                users.phone as users_phon,
                users.status_banned as users_status_banned,
                users.rating as users_rating,
        (SELECT count(*) from booking_job where booking_job.job_uuid=jobs.uuid) AS booking_b_count 
        from jobs 
        JOIN active_jobs ON jobs.uuid = active_jobs.job_uuid 
        JOIN users ON jobs.user_id = users.id 
        ORDER BY jobs.updated_at DESC LIMIT {limit} OFFSET {skip};'''

        result = {"erorr": False, 'list_jobs': ''}
        try:
            # res = await self.database.fetch_all(query=test_query)
            res = await self.database.fetch_all(query=query)
        except ValidationError as e:
            result['list_jobs'] = None
            result['erorr'] = (e.json())
            return result
        result['list_jobs'] = res
        return result

    async def get_list_jobs_without_id(self, limit: int = 100, skip: int = 0) -> List[JobOut_model]:
        # query = jobs.select().limit(limit).offset(skip)
        query = f"SELECT uuid, user_id, title, description, salary_from, salary_to, created_at, updated_at FROM jobs LIMIT {limit} OFFSET {skip}"
        try:
            res = await self.database.fetch_all(query=query)
        except ValidationError as e:
            return (e.json())
        return res

    async def update_job(self, id: int, user_id: int, j: JobIn_model) -> Jobs_model:

        # вычисляем время когда объявление(запрос) должен быть снят с публикации - типа вышло время
        new_expired_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=j.expired_day * 24 * 60)
        activ_job = Active_job(
            job_id=id,
            disactivate_date=new_expired_time
        )
        # создаем запись в таблице active_jobs
        query = active_jobs.update().where(jobs.c.id == id).values(**{**activ_job.dict()})
        await self.database.execute(query=query)

        job = Jobs_model(
            id=id,
            user_id=user_id,
            title=j.title,
            description=j.description,
            price=j.price,
            address=j.address,
            city=j.city,
            phone=j.phone,
            metrostation=j.metrostation,
            is_expired_time=False,
            is_booking=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow())

        values = {**job.dict()}
        values.pop("created_at", None)
        query = jobs.update().where(jobs.c.id == id).values(**values)
        await self.database.execute(query=query)
        return job

    async def delete_job(self, id: int):
        query = jobs.delete().where(jobs.c.id == id)
        return await self.database.execute(query=query)

    async def get_job_by_id(self, id: int) -> Optional[Jobs_model]:
        query = jobs.select().where(jobs.c.id == id)
        job = await self.database.fetch_one(query=query)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
        return Jobs_model.parse_obj(job)

    async def get_job_by_uuid(self, uuid: str) -> Optional[Jobs_model]:
        query = jobs.select().where(jobs.c.uuid == uuid)
        job = await self.database.fetch_one(query=query)
        if job is None:
            # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
            return False
        return Jobs_model.parse_obj(job)

    async def get_job_by_user_id(self, user_id: int) -> Optional[Jobs_model]:

        # query = select(jobs, active_jobs).where(jobs.c.user_id == user_id).join(active_jobs)
        query = f'''SELECT *, 
(SELECT count(*) from booking_job where booking_job.job_uuid=jobs.uuid) AS b_count 
from jobs 
JOIN active_jobs ON jobs.uuid = active_jobs.job_uuid WHERE jobs.user_id={user_id};'''

        # print(f'query={query}')
        res = await self.database.fetch_all(query=query)
        if res is None:
            return False
        return res

    async def set_is_booking(self, job_uuid: str, booking: bool) -> bool:
        query = jobs.update().where(jobs.c.uuid == job_uuid).values(is_booking=booking)
        try:
            await self.database.execute(query)
        except Exception as e:
            print(e)
            return False
        return True

    async def set_booking_job(self, job_uuid: str, user_id: int):
        query = booking_job.select().where(booking_job.c.job_uuid == job_uuid, booking_job.c.user_id == user_id)
        res = await self.database.fetch_one(query=query)
        print(f'res: {res}')
        if res is not None:
            # есть такое бронирование. ничего не меняем возвращаем False
            status = False
            code = 'E001'
            text = 'Заявка на выполение уже подана'
            return {'status': status, 'text': text, 'code': code}

        b_job = Booking_job_model(
            id=0,
            job_uuid=job_uuid,
            user_id=user_id,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow())
        values = {**b_job.dict()}
        values.pop("id", None)
        query = booking_job.insert().values(**values)
        try:
            await self.database.execute(query=query)
        except Exception as e:
            print(e)
            status = False
            code = 'E002'
            text = 'Ошибка записи заявки в БД'
            return {'status': status, 'text': text, 'code': code}
        status = True
        code = 'E003'
        text = 'Заявка создана'
        return {'status': status, 'text': text, 'code': code}

    async def get_users_from_booking_tab(self, job_uuid: str) -> Optional[User]:
        query = select(booking_job.c.user_id, users, active_jobs).join(users,
                                                                       booking_job.c.user_id == users.c.id).where(
            booking_job.c.job_uuid == job_uuid).join(active_jobs,
                                                     booking_job.c.job_uuid == active_jobs.c.job_uuid).order_by(
            nullslast(active_jobs.c.performer_confirmed.asc()))

        print(f'get user list query--->{query}')
        res = await self.database.fetch_all(query=query)
        if res is None:
            return False
        return res

    async def set_booking_job_approved_performer(self, job_uuid: str, user_id: int):
        # редактируем запись в таблице active_jobs
        # добавляем исполнителя в конкретной джобе

        query = active_jobs.update().where(active_jobs.c.job_uuid == job_uuid).values(performer_confirmed=user_id)
        try:
            await self.database.execute(query=query)
        except Exception as e:
            return False
        return True

    async def booking_job_cancel_performer(self, job_uuid: str, user_id: int):

        query = active_jobs.update().where(active_jobs.c.job_uuid == job_uuid,
                                           active_jobs.c.performer_confirmed == user_id).values(
            performer_confirmed=None)
        try:
            await self.database.execute(query=query)
        except Exception as e:
            return False
        return True

    async def delete_from_booking(self, job_uuid: str, user_id: int):
        query = booking_job.delete().where(booking_job.c.job_uuid == job_uuid, booking_job.c.user_id == user_id)
        try:
            await self.database.execute(query=query)
        except Exception as e:
            return False
        return True

    async def get_my_response_job_list(self, user_id: int):
        # получаю id юзера и ищу в booking таблице
        # надо полуичть список объявлений на которые юзер откликнулся
        query = select(booking_job.c.user_id, jobs, active_jobs, users).join(jobs,
                                                                             booking_job.c.job_uuid == jobs.c.uuid).join(
            active_jobs, active_jobs.c.job_uuid == booking_job.c.job_uuid).where(
            booking_job.c.user_id == user_id).join(users, users.c.id == jobs.c.user_id)
        print(f'get_my_response_job_list query--->{query}')
        res = await self.database.fetch_all(query=query)
        if res is None:
            return False
        return res

    async def false_is_booking(self, job_uuid: str, new_value: bool = False) -> bool:
        print(f'job_is_publish_change function')
        query = jobs.update().where(jobs.c.uuid == job_uuid).values(is_booking=new_value)
        try:
            await self.database.execute(query)
            return True
        except Exception as e:
            return False
