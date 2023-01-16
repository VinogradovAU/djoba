from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from models.my_token import MyToken, Login
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from core.security import verify_password, create_access_token, hashed_password
from fastapi.templating import Jinja2Templates
from auth.forms import LoginForm, RegisterForm
from fastapi.responses import RedirectResponse
from core.security import manager
from models.user import User
import datetime
import uuid

templates = Jinja2Templates(directory="templates")
# router = APIRouter()

router = APIRouter(include_in_schema=False)


@router.get("/registration")
async def registration(request: Request):
    print('this is get registration function')
    return templates.TemplateResponse("registration.html", {"request": request})


@router.post("/registration")
async def registration_post(request: Request, users: UserRepository = Depends(get_user_repository)):
    print('this is POST registration function')
    form = RegisterForm(request)
    await form.load_data()
    if await form.is_valid():
        print("form is valid - ok")
        try:
            # проверяем есть юзер с таким мылом в системе или нет. если нет, то генерим под новое мыло токен
            access_token = await verify_register_new_user(form, users)
            if access_token:
                print(f'сгенерирован access_token: {access_token}')
                # тут надо завести нового юзера в бд и залогинить его
                my_uuid = str(uuid.uuid4())
                UserA = User(
                    name=form.email.split('@')[0],
                    uuid=my_uuid,
                    email=form.email,
                    hashed_password=form.password,
                    is_company=False,
                    status_online=True,
                    is_admin=False,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                )
                new_user = await users.create_user_from_formtemplate(u=UserA)
                # настраиваем менеджер для залогиненного юзера
                manager.access_token = access_token
                manager.direction = 'login'
                if new_user:
                    manager.user = await users.get_by_email(form.email)
                return RedirectResponse("/", status_code=302)
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            form.__dict__.update(authenticated=False)
            response = templates.TemplateResponse("registration.html", form.__dict__)
            return response

        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("registration.html", form.__dict__)
    form.__dict__.update(msg="")
    form.__dict__.get("errors").append("Incorrect Email or Password")
    return templates.TemplateResponse("registration.html", form.__dict__)


@router.post("/", response_model=MyToken)
async def api_login(mylogin: Login, users: UserRepository = Depends(get_user_repository)):
    log_user = await users.get_by_email(mylogin.email)
    if log_user is None or not verify_password(mylogin.password, log_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return MyToken(
        access_token=create_access_token({"sub": log_user.email}),
        token_type="Bearer"
    )


@router.get("/logout")
async def logout(request: Request, users: UserRepository = Depends(get_user_repository)):
    print('this is get logout function')
    manager.direction = 'logout'
    await users.user_set_status(manager.user, False)
    return RedirectResponse(url="/", status_code=302)


@router.get("/login")
async def login(request: Request):
    print('this is get login function')
    return templates.TemplateResponse("login.html", {"request": request})


async def verify_login(form: Form, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(form.email)
    if not user:
        return False
    if verify_password(form.password, user.hashed_password):
        access_token = create_access_token({"sub": user.email})
        # return Token_for_login(access_token=access_token)
        return access_token
    return False


@router.post("/login")
async def login_post(request: Request, users: UserRepository = Depends(get_user_repository)):
    print('this is POST login function')
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        print("form is valid - ok")
        try:
            access_token = await verify_login(form, users)
            if access_token:
                print(f'сгенерирован access_token: {access_token}')
                manager.access_token = access_token
                manager.direction = 'login'
                manager.user = await users.get_by_email(form.email)
                manager.autorization = True
                if manager.user.is_admin:
                    manager.is_admin = True
                await users.user_set_status(manager.user, True)
                print(f'manager.user.uuid:{manager.user.uuid}')
                return RedirectResponse("/", status_code=302)
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            form.__dict__.update(authenticated=False)
            response = templates.TemplateResponse("login.html", form.__dict__)
            return response

        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    form.__dict__.update(msg="")
    form.__dict__.get("errors").append("Incorrect Email or Password")
    return templates.TemplateResponse("login.html", form.__dict__)


async def verify_register_new_user(form: Form, users: UserRepository = Depends(get_user_repository)):
    user = await users.get_by_email(form.email)
    # если юзер есть то возвращем false
    if user:
        return False
    # если юзера нет то генерим для новго юзера токен
    access_token = create_access_token({"sub": form.email})
    return access_token
