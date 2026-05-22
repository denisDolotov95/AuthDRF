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
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenBlacklistView)

from pet_project.app import views

router = routers.DefaultRouter()
router.register("auth", views.AuthenticationUserViewSet, basename="auth")
router.register("user-func", views.UserFunctionsViewSet, basename="user-func")
router.register("users", views.UserViewSet, basename="user")
router.register("groups", views.GroupsViewSet)
router.register("element", views.BusinessElementViewSet, basename="element")
router.register("product", views.BusinessElementProductViewSet, basename="product")
router.register("order", views.BusinessElementOrderViewSet, basename="order")
router.register(
    "access-rule-element", views.AccessGroupRuleViewSet, basename="access-rule-element"
)
router.register(
    "order-item", views.BusinessElementOrderItemViewSet, basename="orderitem"
)
# router.register("my-info-edit", views.MyInfoEditViewSet, basename="my-info-edit")


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email=""),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    # path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
