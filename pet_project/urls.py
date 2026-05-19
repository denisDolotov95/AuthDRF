"""
URL configuration for pet_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from rest_framework import routers

from pet_project.app import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet, basename="user")
router.register("login", views.LoginUserViewSet, basename="login")
router.register("logout", views.LogoutUserViewSet, basename="logout")
router.register("groups", views.GroupsViewSet)
router.register("my-info", views.MyInfoViewSet, basename="my-info")
router.register("register", views.RegisterUserViewSet, basename="register")
router.register("delete-user", views.UserDeleteViewSet, basename="delete-user")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
]
