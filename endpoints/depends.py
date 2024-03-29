from fastapi import Depends, HTTPException, status
from db.base import database
from models.user import User
from core.security import JWTBearer, decode_access_token
from repositories.users import UserRepository
from repositories.jobs import JobRepositoryes
from repositories.comments import CommentRepositoryes

from endpoints import depends

def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_job_repository() -> JobRepositoryes:
    return JobRepositoryes(database)

def get_comment_repository() -> CommentRepositoryes:
    return CommentRepositoryes(database)

async def get_current_user(mytoken: str = Depends(JWTBearer()),
                           users: UserRepository = Depends(get_user_repository)) -> User:
    cred_exeption = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(mytoken)
    if payload is None:
        raise cred_exeption
    email: str = payload.get("sub")
    if email is None:
        raise cred_exeption
    users = depends.get_user_repository()
    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exeption
    return user

async def get_comment_by_performer_id(user_id: int):
    comments = depends.get_comment_repository()
    return await comments.get_comment_by_performer_id(user_id)

async def get_comment_by_author_id(user_id: int):
    comments = depends.get_comment_repository()
    return await comments.get_comment_by_author_id(user_id)

async def set_is_author_read(comment_id: int):
    comments = depends.get_comment_repository()
    return await comments.set_is_author_read(comment_id=comment_id)

async def set_is_performer_read(comment_id: int):
    comments = depends.get_comment_repository()
    return await comments.set_is_performer_read(comment_id=comment_id)