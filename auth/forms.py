from typing import List
from typing import Optional

from fastapi import Request
from pydantic import condecimal, Field
from models.jobs import CreateJobIn
from models.user import EditUserPassworModel


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get(
            "email"
        )  # since outh works on email field we are considering email as email
        self.password = form.get("password")

    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


class RegisterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.password2: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get(
            "email"
        )  # since outh works on email field we are considering email as email
        self.password = form.get("password")
        self.password2 = form.get("password2")

    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4 or self.password != self.password2:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


class EditPassworForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.newpassword1: Optional[str] = None
        self.newpassword2: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.newpassword1 = form.get("newpassword1")
        self.newpassword2 = form.get("newpassword2")

    async def is_valid(self):
        if not self.newpassword1 or not len(self.newpassword1) >= 4 or self.newpassword1 != self.newpassword2:
            self.errors.append("A valid password is required")
        try:
            check_password = EditUserPassworModel(
                newpassword1=self.newpassword1,
                newpassword2=self.newpassword2,
            )
            if check_password and not self.errors:
                return True
        except Exception as e:
            print(e)
            return False
        return False
