import datetime
from typing import Optional, List, Any
from fastapi import Request, HTTPException, status, Form, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import jwt
from core.config import SECRET_KEY, ALGORITM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")


def hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITM)
    print(f'token: {token}')
    return token


def decode_access_token(token: str):
    try:
        encode_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITM])
    except jwt.JWTError:
        return None
    return encode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        exp = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid auth token")
        if credentials:
            token_1 = decode_access_token(credentials.credentials)
            if token_1 is None:
                raise exp
            return credentials.credentials
        else:
            raise exp


class Manager():

    def __init__(self, user_status: str = 'offline',
                 autorization: bool = False,
                 resp: Optional[List] = None,
                 response: Any = None,
                 set_cookie: bool = False,
                 access_token: str = '',
                 direction: str = '/',  # login или logout пришли на главную по 302 или просто на главную заход
                 user: Any = None,
                 ):
        self.user_status = user_status
        self.autorization = autorization
        self.resp = resp
        self.response = response
        self.set_cookie = set_cookie
        self.access_token = ''
        self.direction = direction
        self.user = user


manager = Manager()
