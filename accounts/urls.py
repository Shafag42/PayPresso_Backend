from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import  (PersonalUserProfileRetrieveUpdateView,
                             BusinessUserProfileRetrieveUpdateView,TokenObtainPairView,
                             UserLoginView,LogoutView,PersonalUserRegisterView,BusinessUserRegisterView,PersonalUserProfileView,BusinessUserProfileView)

urlpatterns = [
    path('personal_user/register/', PersonalUserRegisterView.as_view(), name='personal_user_register'),
    path('business_user/register/', BusinessUserRegisterView.as_view(), name='business_user_register'),
    path("token_create/", TokenObtainPairView.as_view(), name='token_create'),
    path("token_refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("personal_profile/create", PersonalUserProfileView.as_view(), name="personal_profile_create"),
    path("business_profile/create", BusinessUserProfileView.as_view(), name="business_profile_create"),
    path("personal_profile/update", PersonalUserProfileRetrieveUpdateView.as_view(), name="personal_profile_update"),
    path("business_profile/update", BusinessUserProfileRetrieveUpdateView.as_view(), name="business_profile_update"),
    path('login/', UserLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
]