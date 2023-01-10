from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from models.my_token import MyToken, Login
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from core.security import verify_password, create_access_token
from fastapi.templating import Jinja2Templates
from auth.forms import LoginForm
from fastapi.responses import RedirectResponse
from core.security import manager

templates = Jinja2Templates(directory="templates")
router = APIRouter()

router = APIRouter(include_in_schema=False)


@router.get("/registration")
async def registration(request: Request):
    print('this is get registration function')
    return templates.TemplateResponse("registration.html", {"request": request})


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
async def logout(request: Request):
    print('this is get logout function')
    manager.direction = 'logout'
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
async def login(request: Request, users: UserRepository = Depends(get_user_repository)):
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
