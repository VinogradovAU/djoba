from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from repositories.jobs import JobRepositoryes
from endpoints.depends import get_job_repository

templates = Jinja2Templates(directory="templates")
from core.security import manager

# router = APIRouter()

router = APIRouter(include_in_schema=False)


@router.get("/profile")
async def profil(
        request: Request,
        users: UserRepository = Depends(get_user_repository),
        jobs: JobRepositoryes = Depends(get_job_repository)):
    print('this is get profile function')

    # user = await users.get_by_uuid(uuid)
    if not request.state.user_is_authenticated:
        print(f'authenticated = Fals ---> редирект на login')
        return RedirectResponse("/auth/login", status_code=302)

    context = {
        "request": request,
        "user_object": request.state.user,
        "user_name": request.state.user.name,
        "user_uuid": request.state.user.uuid,
    }

    if request.state.user.is_admin:
        all_users = await users.get_all(limit=100, skip=0)
        for k in all_users:
            print(f'uuid: {k.uuid}')
        if all_users:
            context['all_users'] = all_users
        response = templates.TemplateResponse("admin_profile.html", context=context)
    else:
        my_jobs = await jobs.get_job_by_user_id(request.state.user.id)
        context['jobs'] = my_jobs
        response = templates.TemplateResponse("user_profile.html", context=context)

    return response