from fastapi import APIRouter, Request
from core.security import manager
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from auth.forms import CreateJobForm

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

            form = CreateJobForm(request)

            if await form.load_and_valid_data():
                print("form is valid - ok")
                print(form.__dict__)
            else:
                print("form is NOT valid")
                print(form.__dict__)
                context["errors"] = errors
                context["form"] = form.__dict__

            return templates.TemplateResponse("create_job_form.html", context=context)
    manager.direction = 'create_job'
    return RedirectResponse("/auth/login", status_code=302)
