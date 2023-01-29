from fastapi import APIRouter, Request
from core.security import manager
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.jobs import CreateJobIn
from pydantic import ValidationError

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
async def create_job(request: Request):
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
            else:
                print(f'СОХРАНИТЬ КАК ЧЕРНОВИК')

            return RedirectResponse("/profile", status_code=302)
    manager.direction = 'create_job'
    return RedirectResponse("/auth/login", status_code=302)
