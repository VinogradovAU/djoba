from models.jobs import jobs_model
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends, Response, Cookie
from repositories.jobs import JobRepositoryes
from endpoints.depends import get_job_repository
from fastapi.templating import Jinja2Templates
from core.security import decode_access_token
from starlette.datastructures import MutableHeaders
from core.security import manager

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def main_page(
        request: Request,
        jobs: JobRepositoryes = Depends(get_job_repository),
):

    authenticated = False

    jobs_items = await jobs.get_list_jobs(limit=100, skip=0)
    jobs_items_list = list(map(jobs_model.parse_obj, jobs_items))
    context = {
        "request": request,
        "jobs_items": jobs_items_list,
        "authenticated": authenticated,
        # "jobs_items": jobs_items,
    }

    # просто зашли на главную
    if manager.direction == '/' or manager.direction == 'create_job':
        if manager.direction == 'create_job':
            manager.direction = '/'
        print(f'main_page-->main_page')
        if manager.autorization:
            context['authenticated'] = True
            # проверка на то что токен не протух. если протух делаем return сразу при этом authenticated false
            try:
                access_token = request.cookies.get("access_token")
                print(f'test token: {access_token}')
                decode_token = decode_access_token(access_token)
                print(f'decode_token: {decode_token}')
                if decode_token:
                    print(f'token не протух')
                    context['authenticated'] = True
                    if manager.user:
                        context['user_name'] = manager.user.name
                        context['user_uuid'] = manager.user.uuid
                else:
                    context['authenticated'] = False
            except Exception as e:
                print(f'ошибка проверки token')
                context['authenticated'] = False

        response = templates.TemplateResponse("index.html", context=context)
        return response

    # редирект на главную после нажатия login
    if manager.direction == 'login' or manager.direction == 'create_job_ok':
        print(f'main_page-->login')
        manager.autorization = True
        manager.set_cookie = True
        manager.user_status = 'online'
        context['authenticated'] = True
        if manager.user:
            context['user_name'] = manager.user.name
            context['user_uuid'] = manager.user.uuid
        # if manager.user.is_admin:
        #     return RedirectResponse(f"/profile/{manager.user.uuid}", status_code=302)
        if manager.direction == 'create_job_ok':
            #если логинились для создания нового объявления
            response = templates.TemplateResponse("create_job_form.html", context=context)
        else:
            response = templates.TemplateResponse("index.html", context=context)
        response.set_cookie(key="access_token", value=manager.access_token, httponly=True)
        manager.direction = '/'

        return response


    if manager.direction == 'logout':
        print(f'main_page-->logout')
        manager.autorization = False
        manager.set_cookie = False
        manager.user_status = 'offline'
        manager.access_token = ''
        context['authenticated'] = False
        response = templates.TemplateResponse("index.html", context=context)
        # response.delete_cookie("access_token")
        response.set_cookie(key="access_token", value=manager.access_token, httponly=True)
        manager.direction = '/'
        return response


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
