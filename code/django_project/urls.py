"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from accounts.views import LogoutView, RegisterView, CustomTokenObtainPairView
from accounts.views import UserListView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Authentication
    path("api/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/login/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/signup/", RegisterView.as_view(), name="signup"),
    # User Management
    path("api/v1/users/", UserListView.as_view(), name="user_list"),
    # Friends & Friend Request Management
    path("api/v1/friend/", include("friends.urls")),
]
