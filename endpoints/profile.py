from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
templates = Jinja2Templates(directory="templates")
from core.security import manager
# router = APIRouter()

router = APIRouter(include_in_schema=False)


@router.get("/profile/{uuid}")
async def profil(
        request: Request,
        uuid: str,
        users: UserRepository = Depends(get_user_repository)):
    print('this is get profile function')
    print(f'get user id: {uuid}')

    user = await users.get_by_uuid(uuid)
    if user:
        context = {
            "request": request,
            "user_object": user,
            "user_name": user.name,
            "user_uuid": user.uuid,
        }
        if manager.autorization:
            context['authenticated'] = True
        else:
            return RedirectResponse("/auth/login", status_code=302)

        if user.is_admin:
            response = templates.TemplateResponse("admin_profile.html", context=context)
        else:
            response = templates.TemplateResponse("user_profile.html", context=context)


    return response