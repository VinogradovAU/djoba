from typing import List
from typing import Optional

from fastapi import Request
from pydantic import condecimal, Field
from models.jobs import CreateJobIn


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


class CreateJobForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.title: CreateJobIn.title
        self.description: CreateJobIn.description
        self.price: CreateJobIn.price
        self.phone: CreateJobIn.phone
        self.city: CreateJobIn.city
        self.address: CreateJobIn.address
        self.metrostation: CreateJobIn.metrostation
        self.expired_day: CreateJobIn.expired_day

    async def load_and_valid_data(self):
        form = await self.request.form()
        try:
            self.title = form.get("title")
            self.description = form.get("description")
            self.price = form.get("price")
            self.phone = form.get("phone")
            self.city = form.get("city")
            self.address = form.get("address")
            self.metrostation = form.get("metrostation")
            self.expired_day = form.get("expired_day")

        except Exception as e:
            return False
        return True

    async def is_valid(self):
        print('this is is_valid function CreateJobForm')
        return True
