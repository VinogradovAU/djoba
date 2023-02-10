from repositories.base import BaseRepository
from models.jobs import Jobs_model, JobIn_model, JobOut_model, CreateJobIn, Active_job
from db.jobs import jobs, active_jobs
from typing import List, Optional
import datetime
from fastapi import HTTPException, status
from pydantic import ValidationError
import uuid


class JobRepositoryes(BaseRepository):
    async def job_id_publish_change(self, uuid: str, new_publish: bool = False) -> bool:
        print(f'job_is_publish_change function')
        query = jobs.update().where(jobs.c.uuid == uuid).values(is_publish=new_publish)
        try:
            await self.database.execute(query)
            return True
        except Exception as e:
            return False

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
            metrostation=j.metrostation,
            is_active=True,
            is_publish=is_publish,
            is_expired_time=False,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**job.dict()}
        values.pop("id", None)
        query = jobs.insert().values(**values)
        #создаем запись в таблице jobs
        job.id = await self.database.execute(query=query)

        #вычисляем время когда объявление(запрос) должен быть снят с публикации - типа вышло время
        new_expired_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=j.expired_day * 24 * 60)
        activ_job = Active_job(
            job_id=job.id,
            disactivate_date=new_expired_time
        )
        #создаем запись в таблице active_jobs
        query = active_jobs.insert().values(**{**activ_job.dict()})
        await self.database.execute(query=query)
        return job

    async def create_job(self, user_id: int, j: JobIn_model) -> Jobs_model:
        my_uuid = str(uuid.uuid4())
        print(f'my_uuid: {my_uuid}')
        job = Jobs_model(
            uuid=my_uuid,
            id=0,
            user_id=user_id,
            title=j.title,
            description=j.description,
            price=j.price,
            address=j.address,
            city=j.city,
            metrostation=j.metrostation,
            is_active=True,
            is_publish=True,
            is_expired_time=j.is_expired_time,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow())
        values = {**job.dict()}
        values.pop("id", None)
        query = jobs.insert().values(**values)
        job.id = await self.database.execute(query=query)
        return job

    async def get_list_jobs(self, limit: int = 100, skip: int = 0) -> List[Jobs_model]:
        test_query = f"SELECT * from jobs JOIN active_jobs ON jobs.id = active_jobs.job_id LIMIT {limit} OFFSET {skip};"


        # for k in records:
        #     print(f'id:{k.id}, {k.title}, истекает: {k.disactivate_date}')

        query = jobs.select().limit(limit).offset(skip)
        try:
            res = await self.database.fetch_all(query=test_query)
        except ValidationError as e:
            return (e.json())
        return res

    async def get_list_jobs_without_id(self, limit: int = 100, skip: int = 0) -> List[JobOut_model]:
        # query = jobs.select().limit(limit).offset(skip)
        query = f"SELECT uuid, user_id, title, description, salary_from, salary_to, created_at, updated_at FROM jobs LIMIT {limit} OFFSET {skip}"
        try:
            res = await self.database.fetch_all(query=query)
        except ValidationError as e:
            return (e.json())
        return res

    async def update_job(self, id: int, user_id: int, j: JobIn_model) -> Jobs_model:
        job = Jobs_model(
            id=id,
            user_id=user_id,
            title=j.title,
            description=j.description,
            salary_from=j.salary_from,
            salary_to=j.salary_to,
            is_active=j.is_active,
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
        return Jobs_model.parse_obj(job)

    async def get_job_by_user_id(self, user_id: int) -> Optional[Jobs_model]:
        query = jobs.select().where(jobs.c.user_id == user_id)
        res = await self.database.fetch_all(query=query)
        if res is None:
            return False
        return res