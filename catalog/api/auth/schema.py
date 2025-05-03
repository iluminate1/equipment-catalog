from django.contrib.auth import (
    get_user_model,
)
from ninja import Schema
from ninja.orm import create_schema

UsernameSchemaMixin = create_schema(
    get_user_model(),
    fields=[get_user_model().USERNAME_FIELD],
)

EmailSchemaMixin = create_schema(
    get_user_model(),
    fields=[get_user_model().EMAIL_FIELD],
)

UserOut = create_schema(
    get_user_model(),
    exclude=["password"],
)


class LoginIn(UsernameSchemaMixin):
    password: str


class RequestPasswordResetIn(EmailSchemaMixin):
    pass


class ErrorsOut(Schema):
    errors: dict[str, list[str]]


class RegisterIn(Schema):
    username: str
    email: str
    password: str
