from typing import List
from endpoints.depends import get_job_repository, get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from repositories.jobs import JobRepositoryes
from models.jobs import jobs_model, jobIn_model
from models.user import User
from pydantic import PositiveInt

router = APIRouter()



@router.get("/api", response_model=List[jobs_model])
async def read_jobs(
        limit: PositiveInt = 100,
        skip: int = 0,
        jobs: JobRepositoryes = Depends(get_job_repository)):
    if skip < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="skip cat' be negative")
    res = await jobs.get_list_jobs(limit=limit, skip=skip)
    return res


@router.post("/api", response_model=jobs_model)
async def create_job(
        j: jobIn_model,
        jobs: JobRepositoryes = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)):
    return await jobs.create_job(user_id=current_user.id, j=j)


@router.put("/api", response_model=jobs_model)
async def update_job(
        id: int,
        j: jobIn_model,
        jobs: JobRepositoryes = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)):
    job = await jobs.get_job_by_id(id=id)
    if job is None or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return await jobs.update_job(id=id, user_id=current_user.id, j=j)


@router.delete("/api")
async def delete_job(id: int,
                     jobs: JobRepositoryes = Depends(get_job_repository),
                     current_user: User = Depends(get_current_user)):
    job = await jobs.get_job_by_id(id=id)
    exp = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job is None or job.user_id != current_user.id:
        raise exp
    await jobs.delete_job(id=id)
    return {'status': True}
