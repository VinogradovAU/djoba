from fastapi import Depends, HTTPException, status
from db.base import database
from models.user import User
from core.security import JWTBearer, decode_access_token
from repositories.users import UserRepository
from repositories.jobs import JobRepositoryes


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_job_repository() -> JobRepositoryes:
    return JobRepositoryes(database)


async def get_current_user(mytoken: str = Depends(JWTBearer()),
                           users: UserRepository = Depends(get_user_repository)) -> User:
    cred_exeption = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(mytoken)
    if payload is None:
        raise cred_exeption
    email: str = payload.get("sub")
    if email is None:
        raise cred_exeption
    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exeption
    return user
