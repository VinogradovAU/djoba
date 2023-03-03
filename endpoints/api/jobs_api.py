from typing import List
from endpoints.depends import get_job_repository, get_current_user
from fastapi import APIRouter, Depends, HTTPException, status, Request
from repositories.jobs import JobRepositoryes
from models.jobs import Jobs_model, JobIn_model, JobOut_model
from models.user import User
from pydantic import PositiveInt

router = APIRouter()



@router.get("/api/job/{uuid}", response_model=Jobs_model)
async def read_job_api(
        uuid: str,
        jobs: JobRepositoryes = Depends(get_job_repository)):
    res = await jobs.get_job_by_uuid(uuid=uuid)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return res


@router.get("/api/job/{id}", response_model=Jobs_model)
async def read_job_api(
        id: int,
        jobs: JobRepositoryes = Depends(get_job_repository)):
    res = await jobs.get_job_by_id(id=id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return res


@router.get("/api", response_model=List[JobOut_model])
async def read_jobs_api(
        limit: PositiveInt = 100,
        skip: int = 0,
        jobs: JobRepositoryes = Depends(get_job_repository)):
    if skip < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="skip cat' be negative")
    # res = await jobs.get_list_jobs(limit=limit, skip=skip)
    res = await jobs.get_list_jobs_without_id(limit=limit, skip=skip)
    return res


@router.post("/api", response_model=Jobs_model, response_model_exclude={"is_active"})
async def create_job_api(
        j: JobIn_model,
        jobs: JobRepositoryes = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)):
    return await jobs.create_job(user_id=current_user.id, j=j)


@router.put("/api", response_model=Jobs_model)
async def update_job_api(
        id: int,
        j: JobIn_model,
        jobs: JobRepositoryes = Depends(get_job_repository),
        current_user: User = Depends(get_current_user)):
    job = await jobs.get_job_by_id(id=id)
    if job is None or job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return await jobs.update_job(id=id, user_id=current_user.id, j=j)


@router.delete("/api")
async def delete_job_api(id: int,
                         jobs: JobRepositoryes = Depends(get_job_repository),
                         current_user: User = Depends(get_current_user)):
    job = await jobs.get_job_by_id(id=id)
    exp = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job is None or job.user_id != current_user.id:
        raise exp
    await jobs.delete_job(id=id)
    return {'status': True}
