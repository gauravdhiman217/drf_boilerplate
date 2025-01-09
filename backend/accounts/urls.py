from .views import (
    SignupApiView,
    LoginApiView,
    LogOutView,
    TestingResponse,
    RoleView,
    CustomTokenRefreshView,
    ForgotPasswordRequestOtpView,
    ForgotPasswordVerifyOtpView
)

from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

admin.autodiscover()

router = DefaultRouter()
router.register("", SignupApiView)

app_name = "accounts"

urlpatterns = [
    ## Authentication
    path("signup/", include(router.urls), name="signup_api"),
    path("login/", LoginApiView.as_view(), name="login_api"),
    path("logout/", LogOutView.as_view(), name="logout_api"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("check/", TestingResponse.as_view(), name="testing"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    path("role/", RoleView.as_view(), name="RoleView"),
    path('forgot-password/request-otp/', ForgotPasswordRequestOtpView.as_view(), name='forgot_password_request_otp'),
    path('forgot-password/verify-otp/', ForgotPasswordVerifyOtpView.as_view(), name='forgot_password_verify_otp'),
]
