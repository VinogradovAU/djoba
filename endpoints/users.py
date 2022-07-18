from fastapi import APIRouter, Depends, HTTPException, status
from repositories.users import UserRepository
from depends import get_user_repository, get_current_user
from typing import List
from models.user import User, UserIn, UserOut
from pydantic import PositiveInt

router = APIRouter()


@router.get("/api", response_model=List[UserOut])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: PositiveInt = 100,
        skip: int = 0
):
    if skip < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="skip cat' be negative")
    res = await users.get_all(limit=limit, skip=skip)
    return res


@router.post("/api", response_model=User)
async def create_user(
        user: UserIn,
        users: UserRepository = Depends(get_user_repository),
):
    return await users.create(u=user)


@router.put("/api", response_model=User)
async def update_user(
        id: int,
        user: UserIn,
        users: UserRepository = Depends(get_user_repository),
        current_user: User = Depends(get_current_user)):
    old_user = await users.get_by_id(id=id)
    if old_user is None or old_user.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found user")
    us = await users.update_user(id=id, u=user)
    us.hashed_password = "hidden"
    return us
