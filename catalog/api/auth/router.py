from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.contrib.auth import (
    login as django_login,
)
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
from ninja import Router
from ninja.security import django_auth

from .schema import ErrorsOut, LoginIn, RegisterIn, UserOut

router = Router(tags=["Authentication"])
_LOGIN_BACKEND = "django.contrib.auth.backends.ModelBackend"


@router.post("/", response={200: UserOut, 403: None}, auth=None)
def login(request, data: LoginIn):
    user = authenticate(backend=_LOGIN_BACKEND, **data.dict())
    if user is not None and user.is_active:
        django_login(request, user, backend=_LOGIN_BACKEND)
        return user
    return 403, None


@router.post("/register/", response={201: UserOut, 400: ErrorsOut}, auth=None)
def register(request, data: RegisterIn):
    User = get_user_model()

    try:
        # Create user
        user = User.objects.create_user(
            username=data.username,
            email=data.email,
            password=data.password,
            # Add any additional fields here
        )

        # Authenticate and login the user
        django_login(request, user, backend=_LOGIN_BACKEND)
        return 201, user

    except ValidationError as e:
        # Handle model validation errors
        return 400, {"errors": e.message_dict}
    except Exception as e:
        # Handle other potential errors (e.g., duplicate username/email)
        return 400, {"errors": {"__all__": [str(e)]}}


@router.delete("/", response={204: None}, auth=django_auth)
def logout(request):
    django_logout(request)
    return 204, None


# Add this to your existing auth router
@router.get("/csrf/", auth=None)
def get_csrf_token(request):
    return {"csrfToken": get_token(request)}


@router.get("/me", response=UserOut, auth=django_auth)
def me(request):
    return request.user
