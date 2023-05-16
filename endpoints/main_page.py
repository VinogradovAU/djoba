from models.jobs import Jobs_model, Jobs_model_join, Model_list_jobs_join
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends, Response, Cookie
from repositories.jobs import JobRepositoryes
from endpoints.depends import get_job_repository
from core.filters import templates
from core.security import decode_access_token
from starlette.datastructures import MutableHeaders
from core.security import manager

router = APIRouter()



@router.get("/", response_class=HTMLResponse)
async def main_page(
        request: Request,
        jobs: JobRepositoryes = Depends(get_job_repository),
):
    authenticated = False
    jobs_items = await jobs.get_list_jobs(limit=100, skip=0)
    # jobs_items_list = list(map(Jobs_model.parse_obj, jobs_items))
    if not jobs_items['erorr']:
        jobs_items_list = list(map(Model_list_jobs_join.parse_obj, jobs_items['list_jobs']))
        print(f'jobs_items_list-->>>{jobs_items_list}')
        for k in jobs_items_list:
            print(k.users_name)

    else:
        jobs_items_list = []
        print(f'ошибка при попытки вычитать список объявлений: {jobs_items["erorr"]}')
    context = {
        "request": request,
        "jobs_items": jobs_items_list,
        "authenticated": authenticated,
        # "jobs_items": jobs_items,
    }

    if request.state.user_is_authenticated:
        context['authenticated'] = True
        context['user_name'] = request.state.user.name
        context['user_uuid'] = request.state.user.uuid
        context['user'] = request.state.user
        context['new_message_status'] = False
        if request.state.new_message_status:
            context['new_message_status'] = True
    if request.state.user_is_anonymous:
        context['authenticated'] = False

    response = templates.TemplateResponse("index.html", context=context)
    return response

    # редирект на главную после создать запрос !!!!!!!!!!!придумать как!!!!!!!!!!!!!!!!


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


@router.get("/userinfo/{uuid_job}")
async def get_user_info(request: Request,
                        uuid_job: str,
                        jobs: JobRepositoryes = Depends(get_job_repository)):
    user_info = await jobs.get_userinfo_by_uuid_job(uuid_job=uuid_job)
    # status_banned
    print('this is get get_user_info function')

    if not user_info:
        return {"error": 'Ошибка получения данных'}
    else:
        rait = str(user_info.rating)
        return {"error": None,
                "user_name": user_info.name,
                "user_phone": user_info.phone,
                "user_email": user_info.email,
                "user_rait": rait,
                "user_banned": user_info.status_banned}
