from pydantic import BaseModel
from decouple import config
from typing import Union

CSRF_SECRET_KEY = config('CSRF_SECRET_KEY')


class CsrfSettings(BaseModel):
    secret_key: str = CSRF_SECRET_KEY


class TodoBody(BaseModel):
    title: str
    description: str


class Todo(TodoBody):
    id: str


class SuccessMsg(BaseModel):
    message: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBody(BaseModel):
    username: str
    email: str
    password: str


class User(UserBody):
    id: str


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
