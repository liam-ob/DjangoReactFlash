import jwt
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed('Unauthorized')

        user = User.objects.filter(id=payload['id']).first()

        return (user, None)


def create_payload(user_id: int) -> dict:
    return dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),  # token expires in 24 hours
        iat=datetime.datetime.utcnow(),
    )


def create_token(user_id: int) -> dict:
    return jwt.encode(create_payload(user_id=user_id), settings.JWT_SECRET, algorithm="HS256")
