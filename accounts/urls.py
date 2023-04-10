from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.views import  (MyUserCreateView, PersonalProfileRetrieveUpdateView,
                             BusinessProfileRetrieveUpdateView,MyTokenObtainPairView,
                             LoginView,LogoutView, PersonalProfileSerializer,BusinessProfileSerializer)

urlpatterns = [
    path("register/", MyUserCreateView.as_view(), name="register"),
    path('personal_user/register/', PersonalProfileSerializer.as_view(), name='personal_user_register'),
    path('business_user/register/', BusinessProfileSerializer.as_view(), name='business_user_register'),
    path("token_create", MyTokenObtainPairView.as_view(), name='token_create'),
    path("token_refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("personal_profile/update", PersonalProfileRetrieveUpdateView.as_view(), name="personal_profile_update"),
    path("business_profile/update", BusinessProfileRetrieveUpdateView.as_view(), name="business_profile_update"),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
]