from fastapi import APIRouter, Request, Depends
from core.security import manager
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.jobs import CreateJobIn
from pydantic import ValidationError

from endpoints.depends import get_job_repository

from repositories.jobs import JobRepositoryes

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/get_phone/{uuid_job}")
async def get_phone_jobuuid(
        request: Request,
        uuid_job: str,
        jobs: JobRepositoryes = Depends(get_job_repository)
):
    print('this is get get_phone_jobuuid')

    if request.state.user_is_authenticated:
        phone = await jobs.get_phone_by_jobuuid(uuid=uuid_job)
        if phone:
            return {'error': 'None', 'phone': phone}
        else:
            return {'error': 'phone not found', 'phone': ''}

    return {'error': 401, 'phone': ''}


@router.get("/job_edit/{uuid_job}")
async def job_edit(
        request: Request,
        uuid_job: str,
        jobs: JobRepositoryes = Depends(get_job_repository)
):
    print('this is get job_edit function')

    if request.state.user_is_authenticated:
        errors = []
        context = {
            "request": request,
            "user_name": manager.user.name,
            "authenticated": True,
            "form": False,
            "errors": errors,
        }
        joba = await jobs.get_job_by_uuid(uuid_job)

        if joba:
            context["joba"] = joba
            print(f'joba.title: {joba.title}')
        else:
            context["joba"] = False
            print(f'joba: False')
        return templates.TemplateResponse("edit_job_form.html", context=context)

    return RedirectResponse("/auth/login", status_code=302)


@router.get("/publishon/{uuid_job}")
async def publishon(
        request: Request,
        uuid_job: str,
        jobs: JobRepositoryes = Depends(get_job_repository)):
    origin_url = dict(request.scope["headers"]).get(b"referer", b"").decode()
    # my_headers = request.scope["headers"]

    if request.state.user_is_authenticated:
        job = await jobs.job_id_publish_change(uuid=uuid_job, new_publish=True)
        if job:
            error = 'False'
            status_publishon = 'True'  # удалось опубликовать - True, не удалось - False
        else:
            error = 'True'
            status_publishon = 'False'
        return {
            'status_publishon': status_publishon,
            'uuid_job': uuid_job,
            'referrer_uri': origin_url,
            'error': error,
            # 'my_headers': my_headers,
        }
    return RedirectResponse("/auth/login", status_code=302)


@router.get("/publishoff/{uuid_job}")
async def publishoff(
        request: Request,
        uuid_job: str,
        jobs: JobRepositoryes = Depends(get_job_repository)):
    origin_url = dict(request.scope["headers"]).get(b"referer", b"").decode()
    # my_headers = request.scope["headers"]

    if request.state.user_is_authenticated:
        job = await jobs.job_id_publish_change(uuid=uuid_job, new_publish=False)
        if job:
            error = 'False'
            status_publishoff = 'True'  # удалось снять с публикации - True, не удалось - False
        else:
            error = 'True'
            status_publishoff = 'False'
        return {
            'status_publishoff': status_publishoff,
            'uuid_job': uuid_job,
            'referrer_uri': origin_url,
            'error': error,
            # 'my_headers': my_headers,
        }
    return RedirectResponse("/auth/login", status_code=302)


@router.get("/create_job")
async def create_job(request: Request):
    # проверяю залогинен ли пользователь если да то отправляю страницу с формой,
    # если нет, то редирект на login form
    print('this is get create_job function')

    if request.state.user_is_authenticated:
        context = {
            "request": request,
            "user_name": manager.user.name,
            "authenticated": True,
            "form": False,
        }
        return templates.TemplateResponse("create_job_form.html", context=context)
    manager.direction = 'create_job'
    return RedirectResponse("/auth/login", status_code=302)


@router.post("/create_job")
async def create_job(request: Request, jobs: JobRepositoryes = Depends(get_job_repository)):
    # проверяю залогинен ли пользователь если да то отправляю страницу с формой,
    # если нет, то редирект на login form
    print('this is POST create_job function')

    if request.state.user_is_authenticated:
        errors = []
        context = {
            "request": request,
            "user_name": manager.user.name,
            "authenticated": True,
        }
        form = await request.form()
        try:
            form_valid = CreateJobIn(
                errors=errors,
                title=form.get('title'),
                description=form.get('description'),
                price=form.get('price'),
                address=form.get('address'),
                city=form.get('city'),
                metrostation=form.get('metrostation'),
                phone=form.get('phone'),
                expired_day=form.get('expired_day'),
                button=form.get('button'),
                resp=True,
            )
        except ValidationError as e:
            print(e.json()[0])
            err = e.json()
            print(e.__dict__)

            print("form is NOT valid")
            print(form.__dict__)
            errors.append("form is NOT valid")
            errors.append(f"Ошибка ввода поля: {err}")
            context["errors"] = errors
            context["form"] = form
            return templates.TemplateResponse("create_job_form.html", context=context)
        # form = CreateJobForm(request)

        if form_valid.button == 'publish':
            print(f'СОХРАНИТЬ И ОПУБЛИКОВАТЬ')
            new_job = await jobs.create_job_from_html(user_id=manager.user.id, j=form_valid, is_publish=True)

        else:
            print(f'СОХРАНИТЬ КАК ЧЕРНОВИК')
            await jobs.create_job_from_html(user_id=manager.user.id, j=form_valid, is_publish=False)

        return RedirectResponse("/profile", status_code=302)
    print(f'пользователь не залогинен')
    manager.direction = 'create_job'
    return RedirectResponse("/auth/login", status_code=302)


@router.post("/job_edit/{uuid_job}")
async def job_edit(request: Request,
                   uuid_job: str,
                   jobs: JobRepositoryes = Depends(get_job_repository)):
    # проверяю залогинен ли пользователь если да то отправляю страницу с формой,
    # если нет, то редирект на login form
    print('this is POST job_edit function')

    if request.state.user_is_authenticated:
        errors = []
        context = {
            "request": request,
            "user_name": manager.user.name,
            "authenticated": True,
        }
        form = await request.form()
        try:
            form_valid = CreateJobIn(
                errors=errors,
                title=form.get('title'),
                description=form.get('description'),
                price=form.get('price'),
                address=form.get('address'),
                city=form.get('city'),
                metrostation=form.get('metrostation'),
                phone=form.get('phone'),
                expired_day=form.get('expired_day'),
                button=form.get('button'),
                resp=True,
            )
            joba = await jobs.get_job_by_uuid(uuid=uuid_job)
        except ValidationError as e:
            print(e.json()[0])
            err = e.json()
            print(e.__dict__)

            print("form is NOT valid")
            print(form.__dict__)
            errors.append("form is NOT valid")
            errors.append(f"Ошибка ввода поля: {err}")
            context["errors"] = errors
            context["form"] = form
            return templates.TemplateResponse("edit_job_form.html", context=context)
        # form = CreateJobForm(request)

        if form_valid.button == 'publish':
            print(f'СОХРАНИТЬ И ОПУБЛИКОВАТЬ')
            new_job = await jobs.update_job_from_html(joba=joba, j=form_valid, is_publish=True)

        else:
            print(f'СОХРАНИТЬ КАК ЧЕРНОВИК')
            await jobs.update_job_from_html(joba=joba, j=form_valid, is_publish=False)

        return RedirectResponse("/profile", status_code=302)
    print(f'пользователь не залогинен')
    manager.direction = 'create_job'
    return RedirectResponse("/auth/login", status_code=302)
