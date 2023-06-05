from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import  (TokenObtainPairView,CustomUserRegisterView,UserProfileView,
                             UserLoginView,LogoutView,ForgotPasswordView,ResetPasswordView)

urlpatterns = [
    path('custom_user/register/', CustomUserRegisterView.as_view(), name='user_register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path("token/create/",  TokenObtainPairView.as_view(), name='token_create'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('login/',  UserLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]