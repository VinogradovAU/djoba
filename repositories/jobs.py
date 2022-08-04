from repositories.base import BaseRepository
from models.jobs import jobs_model, jobIn_model, jobOut_model
from db.jobs import jobs
from typing import List, Optional
import datetime
from fastapi import HTTPException, status
from pydantic import ValidationError
import uuid

class JobRepositoryes(BaseRepository):

    async def create_job(self, user_id: int, j: jobIn_model) -> jobs_model:
        my_uuid = str(uuid.uuid4())
        print(f'my_uuid: {my_uuid}')
        job = jobs_model(
            uuid=my_uuid,
            id=0,
            user_id=user_id,
            title=j.title,
            description=j.description,
            salary_from=j.salary_from,
            salary_to=j.salary_to,
            is_active=j.is_active,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow())
        values = {**job.dict()}
        values.pop("id", None)
        query = jobs.insert().values(**values)
        job.id = await self.database.execute(query=query)
        return job

    async def get_list_jobs(self, limit: int = 100, skip: int = 0) -> List[jobs_model]:
        query = jobs.select().limit(limit).offset(skip)
        try:
            res = await self.database.fetch_all(query=query)
        except ValidationError as e:
            return (e.json())
        return res
    
    async def get_list_jobs_without_id(self, limit: int = 100, skip: int = 0) -> List[jobOut_model]:
        # query = jobs.select().limit(limit).offset(skip)
        query = f"SELECT uuid, user_id, title, description, salary_from, salary_to, created_at, updated_at FROM jobs LIMIT {limit} OFFSET {skip}"
        try:
            res = await self.database.fetch_all(query=query)
        except ValidationError as e:
            return (e.json())
        return res

    async def update_job(self, id: int, user_id: int, j: jobIn_model) -> jobs_model:
        job = jobs_model(
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

    async def get_job_by_id(self, id: int) -> Optional[jobs_model]:
        query = jobs.select().where(jobs.c.id==id)
        job = await self.database.fetch_one(query=query)
        if job is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="job not found")
        return jobs_model.parse_obj(job)





