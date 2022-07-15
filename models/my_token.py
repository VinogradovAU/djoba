from pydantic import BaseModel, EmailStr


class MyToken(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    email: EmailStr
    password: str
