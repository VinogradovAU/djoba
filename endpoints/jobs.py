from fastapi import APIRouter, Request, Depends
from core.security import manager
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from models.jobs import CreateJobIn, Close_job
from pydantic import ValidationError
from endpoints.depends import get_job_repository
from endpoints.depends import get_comment_repository
from repositories.jobs import JobRepositoryes
from repositories.comments import CommentRepositoryes
from models.comments import Comment_model_in
from repositories.users import UserRepository
from endpoints.depends import get_user_repository

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# срабатывает по кнопке завершить работу их профиля пользователя
@router.post("/close_job")
async def close_job(request: Request,
                    comment: CommentRepositoryes = Depends(get_comment_repository),
                    jobs: JobRepositoryes = Depends(get_job_repository),
                    users: UserRepository = Depends(get_user_repository)):
    close_job = await request.json()
    # print(f'close_job from post: {close_job["uuid_job"]}')
    # print(f'close_job from post: {close_job["user_id"]}')
    # print(f'close_job from post: {close_job["text_area_cancel"]}')
    # тут буду сохранять отзыв и отменять/завершать выполнение джобы, уведомлять автора джобы
    if len(str(close_job["text_area_cancel"])) == 0:
        close_job["text_area_cancel"] = None

    if str(close_job["text_area_cancel"]) == '':
        close_job["text_area_cancel"] = None

    author_id = await jobs.get_userinfo_by_uuid_job(uuid_job=close_job["uuid_job"])
    print(f'autor_id: {author_id}')

    if str(close_job["rait"]) != "-1":
        # есть новая оценка пользователя
        # требуется сделать перерасчет рейтинга и записать в БД
        print(f'Получена оценка работодателя по завершении работы ----> {close_job["rait"]}')
        get_rait_data = await users.users_rait_get_by_id(user_id=author_id.id)
        if get_rait_data is None:
            new_reit_record = await users.users_rait_create_record(user_id=author_id.id, new_rating=int(close_job["rait"]))
            if new_reit_record is None:
                print(f'Ошибка БД при создании записи в users_rait')
            else:
                await users.update_user_raiting(user_id=author_id.id)
                print(f'Райтинг изменен')
        else:
            if await users.users_rait_update(user_id=author_id.id, new_rating=int(close_job["rait"])):
                print(f'Райтинг изменен')
                await users.update_user_raiting(user_id=author_id.id)
            else:
                print(f'ошибка записи в БД - users_rait_update')

    item = Comment_model_in(
        job_uuid=close_job["uuid_job"],
        comment=close_job["text_area_cancel"],
        performer_id=close_job["user_id"],
        author_id=author_id.id,
    )

    new_comment = await comment.create_job_comment(item=item)
    result = await jobs.booking_job_cancel_performer(job_uuid=close_job["uuid_job"],
                                                     user_id=int(close_job["user_id"]))
    booking_job_cancel = await jobs.delete_from_booking(job_uuid=close_job["uuid_job"],
                                                        user_id=int(close_job["user_id"]))
    false_is_booking = await jobs.false_is_booking(job_uuid=close_job["uuid_job"], new_value=False)

    errors = []
    error = False
    if not booking_job_cancel:
        error = True
        errors.append('Ошибка при работе с БД (delete_from_booking)')
    if not result:
        error = True
        errors.append('Ошибка при работе с БД (booking_job_cancel_performer)')
    if not new_comment:
        error = True
        errors.append('Ошибка при записи комментария (БД - create_job_comment)')
    if not false_is_booking:
        error = True
        errors.append('Ошибка при работе с БД (изменение is_booking)')
    if error:
        # print(f'ошибка в методе jobs/close_job: {errors}')
        # можно возвращать массив ошибок errors вместо True, если будет кому их там разобрать
        return {'error': 'True', 'status_cancel': 'NO'}

    return {'error': 'None', 'status_cancel': 'ok'}


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
            new_job = await jobs.create_job_from_html(user_id=request.state.user.id, j=form_valid, is_publish=True)

        else:
            print(f'СОХРАНИТЬ КАК ЧЕРНОВИК')
            await jobs.create_job_from_html(user_id=request.state.user.id, j=form_valid, is_publish=False)

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
            "user_name": request.state.user.name,
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
    # manager.direction = 'create_job'
    return RedirectResponse("/auth/login", status_code=302)


@router.get("/booking/approved/{uuid_job}/{user_id}")
async def approved_performer(request: Request,
                             uuid_job: str,
                             user_id: int,
                             jobs: JobRepositoryes = Depends(get_job_repository)):
    if request.state.user_is_authenticated:
        code = 'E001'
        approved_performer_status = "OK"
        active_job = await jobs.set_booking_job_approved_performer(job_uuid=uuid_job, user_id=int(user_id))
        if active_job:
            return {'code': code, 'approved_performer_status': approved_performer_status}
        else:
            return {'code': 'error', 'approved_performer_status': 'Не удалось назначить исполнителя'}
    return RedirectResponse("/auth/login, status_code=302")


@router.get("/set_booking/{uuid_job}")
async def set_job_booking(request: Request,
                          uuid_job: str,
                          jobs: JobRepositoryes = Depends(get_job_repository)):
    print(f'set_job_booking function on jobs endpoint')
    if request.state.user_is_authenticated:
        # проверяем юзер свое объявление бронирует или чужое
        job = await jobs.get_job_by_uuid(uuid=uuid_job)
        if job and request.state.user.id != job.user_id:
            pass
        else:
            status = False
            code = 'E006'
            text = 'Нельзя откликнуться на свое объявление'
            return {'status': status, 'error': text, 'code': code}

        set_is_booking = await jobs.set_is_booking(job_uuid=uuid_job, booking=True)
        set_booking_job = await jobs.set_booking_job(job_uuid=uuid_job, user_id=int(request.state.user.id))
        # {'status': status, 'text': text, 'code': code}

        if set_is_booking:  # статус is_booking успешно изменен
            if set_booking_job['status']:
                # code='E003'
                print(f'Статуc бронирования джобы с {uuid_job} установлен в {True}')
                return {'error': 'None', 'booking_status': 'True', 'code': set_booking_job['code']}
            else:
                # code E001 и E002
                return {'error': set_booking_job['text'], 'booking_status': '', 'code': set_booking_job['code']}
        else:
            return {'error': 'Не верный uuid джобы', 'booking_status': '', 'code': 'E004'}

    return {'error': 'Пользователь не распознан', 'booking_status': '', 'code': 'E005'}
