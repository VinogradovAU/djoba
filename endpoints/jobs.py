from fastapi import APIRouter, Request, Depends
from core.security import manager
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.jobs import CreateJobIn
from pydantic import ValidationError

from endpoints.depends import get_job_repository

from repositories.jobs import JobRepositoryes

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/create_job")
async def create_job(request: Request):
    # проверяю залогинен ли пользователь если да то отправляю страницу с формой,
    # если нет, то редирект на login form
    print('this is get create_job function')
    if manager.user:
        if manager.autorization:
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
    if manager.user:
        if manager.autorization:
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
                new_job = await jobs.create_job_from_html(user_id=manager.user.id, j=form_valid, id_publish=True)

            else:
                print(f'СОХРАНИТЬ КАК ЧЕРНОВИК')
                await jobs.create_job_from_html(user_id=manager.user.id, j=form_valid, id_publish=False)

            return RedirectResponse("/profile", status_code=302)
    print(f'пользователь не залогинен')
    manager.direction = 'create_job'
    return RedirectResponse("/auth/login", status_code=302)
