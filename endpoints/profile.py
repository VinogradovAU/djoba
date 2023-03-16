from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from repositories.jobs import JobRepositoryes
from endpoints.depends import get_job_repository
from models.user import EditUserProfilData

templates = Jinja2Templates(directory="templates")
from core.security import manager

# router = APIRouter()

router = APIRouter(include_in_schema=False)


@router.get("/")
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
        "authenticated": True,
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

@router.get('/edit/{uuid}')
async def edit_user_info(
        request: Request,
        uuid: str,
        users: UserRepository = Depends(get_user_repository)
):
    print(f'this is get edit_user_info function')

    if request.state.user_is_authenticated:
        errors = []
        context = {
            "errors": errors,
            "request": request,
            "user_object": request.state.user,
            "user_name": request.state.user.name,
            "user_uuid": request.state.user.uuid,
            "authenticated": True,
        }
    else:
        print(f'authenticated = Fals ---> редирект на login')
        return RedirectResponse("/auth/login", status_code=302)

    response = templates.TemplateResponse("edit_user_form.html", context=context)
    return response


@router.post('/edit/{uuid}')
async def edit_user_info(
        request: Request,
        uuid: str,
        users: UserRepository = Depends(get_user_repository)
):
    print(f'this is post edit_user_info function')
    if request.state.user_is_authenticated:
        errors = []
        context = {
            "errors": errors,
            "request": request,
            "user_object": request.state.user,
            "user_name": request.state.user.name,
            "user_uuid": request.state.user.uuid,
            "authenticated": True,
        }

        # надо доставть форму из запроса и валидировать пола
        form = await request.form()
        try:
            print(f'валидирую данные форму')
            is_company = True if form.get('is_company') == '1' else False
            form_valid = EditUserProfilData(
                name=form.get('user_name'),
                email=form.get('email'),
                phone=form.get('phone'),
                is_company=is_company,
            )
            print(dict(form_valid))
            if form_valid:
                # print(f'валидация формы пройдена. далее будем сохранять')
                user = await users.update_user_from_form_profil(id=manager.user.id, u=form_valid)
                if user:
                    manager.user = await users.get_by_uuid(uuid=manager.user.uuid)
                    return RedirectResponse("/profile", status_code=302)
                errors.append("Не удалось сохранить изменения")
                response = templates.TemplateResponse("edit_user_form.html", context=context)
                return response

        except Exception as e:
            # ошибка валидации формы
            print(e)
            errors.append('Ошибка валидации формы. Проверьти поля')
            errors.append(e)
            context['errors'] = errors
            response = templates.TemplateResponse("edit_user_form.html", context=context)
            return response
    else:
        print(f'authenticated = False ---> редирект на login')
        return RedirectResponse("/auth/login", status_code=302)