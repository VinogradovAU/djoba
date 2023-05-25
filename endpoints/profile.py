import datetime

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from repositories.jobs import JobRepositoryes
from repositories.comments import CommentRepositoryes
from endpoints.depends import get_job_repository
from endpoints.depends import get_comment_repository
from models.user import EditUserProfilData
from core.security import manager
from dateutil.parser import parse
from core.filters import templates

# templates = Jinja2Templates(directory="templates")
#
# def ts_to_datetime(ts) -> str:
#     return ts.strftime('%Y-%m-%d %H:%M')
#
# templates.env.filters["ts_to_datetime"] = ts_to_datetime
# router = APIRouter()

router = APIRouter(include_in_schema=False)


@router.get("/")
async def profil(
        request: Request,
        users: UserRepository = Depends(get_user_repository),
        jobs: JobRepositoryes = Depends(get_job_repository),
        comments: CommentRepositoryes = Depends(get_comment_repository)):
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
    if request.state.notifications:
        #передаю уведомления на страницу профиля
        context["notifications"] = request.state.notifications

        #удаляю уведомления, чтобы больше не показывать
        request.state.notifications = None
        del manager.notifications[request.state.user.id]

    if request.state.user.is_admin:
        all_users = await users.get_all(limit=100, skip=0)
        for k in all_users:
            print(f'uuid: {k.uuid}')
        if all_users:
            context['all_users'] = all_users
        response = templates.TemplateResponse("admin_profile.html", context=context)
    else:
        my_comments_performer = await comments.get_comment_by_performer_id(request.state.user.id)

        if my_comments_performer:
            context['comments_performer'] = my_comments_performer
            for ii in my_comments_performer:
                if ii.is_performer_read:
                    await comments.set_is_performer_read(comment_id=ii.id)
                print(f'get comments_performer----> {dict(ii)}')

        my_comments_author = await comments.get_comment_by_author_id(request.state.user.id)

        if my_comments_author:
            context['comments_author'] = my_comments_author
            for ii in my_comments_author:
                if ii.is_author_read:
                    await comments.set_is_author_read(comment_id=ii.id)
                print(f'get comments_author----> {dict(ii)}')

        my_jobs = await jobs.get_job_by_user_id(request.state.user.id)
        context['jobs'] = my_jobs
        my_response_job_list = await jobs.get_my_response_job_list(request.state.user.id)
        context['my_response_job_list'] = my_response_job_list
        response_count = False #для правильного отображения списков работ
        response_confirmed = False # есть те что с откликами, а есть те которые уже одобрили
        count1 = 0
        count2 = 0
        if my_response_job_list:
            for k in my_response_job_list:
                if k.performer_confirmed == request.state.user.id:
                    response_confirmed = True
                    count2 = +1
                else:
                    count1 = count1 + 1
        if count1 != 0:
            response_count = True
        if count2 != 0:
            response_confirmed = True
        context['response_count'] = response_count
        context['response_confirmed'] = response_confirmed
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


@router.get('/responses/{job_uuid}')
async def response_booking(request: Request,
                           job_uuid: str,
                           users: UserRepository = Depends(get_user_repository),
                           jobs: JobRepositoryes = Depends(get_job_repository)
                           ):
    print(f'this is get /responses/uuid_job function')
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

    user_list = await jobs.get_users_from_booking_tab(job_uuid)

    context['user_list'] = user_list
    context['target_job_uuid'] = job_uuid
    response = templates.TemplateResponse("booking_userlist_profile.html", context=context)
    return response
