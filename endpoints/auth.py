from fastapi import APIRouter, Depends, HTTPException, status
from models.my_token import MyToken, Login
from repositories.users import UserRepository
from endpoints.depends import get_user_repository
from core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/", response_model=MyToken)
async def login(mylogin: Login, users: UserRepository = Depends(get_user_repository)):
    log_user = await users.get_by_email(mylogin.email)
    if log_user is None or not verify_password(mylogin.password, log_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return MyToken(
        access_token=create_access_token({"sub": log_user.email}),
        token_type="Bearer"
    )
