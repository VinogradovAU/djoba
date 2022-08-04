from models.jobs import jobs_model
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends
from repositories.jobs import JobRepositoryes
from endpoints.depends import get_job_repository
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def main_page(
        request: Request,
        jobs: JobRepositoryes = Depends(get_job_repository)
):
    jobs_items = await jobs.get_list_jobs(limit=100, skip=0)
    jobs_items_list = list(map(jobs_model.parse_obj, jobs_items))
    context = {
        "request": request,
        "jobs_items": jobs_items_list,
        # "jobs_items": jobs_items,
    }
    # for i in jobs_items_list:
    #     print(i.title)
    return templates.TemplateResponse("index.html", context=context)


@router.get("/job/{id}", response_class=HTMLResponse)
async def job_page(request: Request,
                   id: int,
                   jobs: JobRepositoryes = Depends(get_job_repository)):
    res = await jobs.get_job_by_id(id=id)
    context = {"request": request,
               "id": id,
               "job_item": res}
    print(type(res))
    return templates.TemplateResponse("job.html", context=context)
