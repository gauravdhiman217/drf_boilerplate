from .models import User, Roles
from .serializers import UserSerializer, RoleSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, logout
from django.views.generic import TemplateView
from django.shortcuts import redirect
from rest_framework.generics import ListAPIView
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from django.utils import timezone
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Call the original refresh method
        response = super().post(request, *args, **kwargs)

        # Update last_login field
        try:
            access_token = response.data.get("access")
            if access_token:
                # Decode the token to get the user
                token = AccessToken(access_token)
                user_id = token["user_id"]

                # Get the user instance and update the last_login
                user_instance = User.objects.get(id=user_id)
                user_instance.last_login = timezone.now()
                user_instance.save(update_fields=["last_login"])
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return response


"""
Admin Login
"""


class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect("accounts:web_login")


"""
SignUp Api
"""


class SignupApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Define permissions based on action
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


class SignupApiView1(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            if not request.data.get("first_name"):
                return Response(
                    {
                        "message": "Please enter first name",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("last_name"):
                return Response(
                    {
                        "message": "Please enter last name",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("mobile_no"):
                return Response(
                    {
                        "message": "Please enter mobile number",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("email"):
                return Response(
                    {
                        "message": "Please enter email",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.data.get("password"):
                return Response(
                    {
                        "message": "Please enter password",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = User.objects.create(
                first_name=request.data.get("first_name"),
                last_name=request.data.get("last_name"),
                email=request.data.get("email"),
                mobile_no=request.data.get("mobile_no"),
                password=make_password(request.data.get("password")),
                role_id=request.data.get("role_id"),
                gender=request.data.get("gender"),
            )
            data = UserSerializer(user, context={"request": request}).data
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_201_CREATED,
                    "message": "User Registered Successfully",
                    "data": data,
                }
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "User not Registered Successfully",
                    "info": str(e),
                }
            )


class LoginApiView(APIView):
    """
    Login Api
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.data.get("email"):
            return Response(
                {"message": "Please enter email", "status": status.HTTP_400_BAD_REQUEST}
            )
        if not request.data.get("password"):
            return Response(
                {"message": "Please enter password"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=request.data.get("email"), password=request.data.get("password")
        )

        if not user:
            return Response(
                {
                    "message": "Invalid Login Credentials.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        if not user.is_active:
            return Response(
                {
                    "message": "Your account has been deactivated. Please contact admin to activate your account.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        data = UserSerializer(user, context={"request": request}).data
        data.update(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        )
        return Response(
            {
                "status": "success",
                "status_code": status.HTTP_200_OK,
                "message": "Logged In Successfully",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class LogOutView(APIView):
    """
    Logout Api
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # refresh_token = request.headers.get('Authorization').split()[1]
            user = request.user
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])
            refesh_token = request.data.get("refresh_token")
            token = RefreshToken(refesh_token)
            token.blacklist()
            logout(request)
            request.session.flush()
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_205_RESET_CONTENT,
                    "message": "Logged out Successfully",
                },
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "Bad request",
                    "error": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class TestingResponse(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello World"}, status=status.HTTP_200_OK)


class RoleView(ListAPIView):
    serializer_class = RoleSerializer
    queryset = Roles.objects.all()
