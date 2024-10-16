from .constants import *  # noqa
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


User = get_user_model()


class EmailLoginBackend(ModelBackend):
    def authenticate(
        self, request, username=None, password=None, role_id=None, **kwargs
    ) -> dict:
        """
        This method is used for authenticating user using email or mobile number.
        If username is email then it will try to find user by email otherwise it will try to find user by mobile number.

        Args:
            request (drf_request): django request
            username (str): email or mobile number
            password (str):  password
        Returns:
            dict: if user is authenticated then it will return user object, access token, refresh token
            else None

        """
        user = None
        try:
            user = User.objects.filter(Q(email=username) | Q(mobile_no=username)).last()
        except User.DoesNotExist:
            return None
        if user is None:
            return None
        if user.check_password(password):
            return user
        return None
