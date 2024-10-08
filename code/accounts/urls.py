from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import LogoutView, RegisterView, CustomTokenObtainPairView

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", RegisterView.as_view(), name="signup"),
]
