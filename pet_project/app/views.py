# import logging

from django.contrib.auth.models import Group, User

from django.contrib.auth import login, logout
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

# from rest_framework.exceptions import MethodNotAllowed
# from rest_framework.views import APIView

from .serializers import (
    GroupSerializer,
    UserInfoSerializer,
    UserSerializer,
    UserRegistrationSerilaizer,
    UserAuthenticationSerilaizer,
)


class UserFunctionsViewSet(viewsets.GenericViewSet):

    http_method_names = ["get", "patch", "delete"]

    # serializer_class = UserInfoSerializer

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ("patch", "get"):
            return UserInfoSerializer
        return super().get_serializer_class()

    @action(
        methods=["get"],
        detail=False,
        url_path="info",
        url_name="info",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def get(self, request):
        """Информация пользователя."""
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["delete"],
        detail=False,
        url_path="delete",
        url_name="delete",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def delete(self, request):
        """Удаление учетной записи."""
        request.user.is_active = False
        request.user.save()
        logout(request)
        return Response({"detail": "Account is deleted."})

    @action(
        methods=["patch"],
        detail=False,
        url_path="update",
        url_name="update",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def patch(self, request):
        """Обновление данных пользователя."""
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            request.user, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthenticationUserViewSet(viewsets.GenericViewSet):
    """
    API-представление для аутентификации/регистрации пользователя.
    """

    # serializer_class = UserAuthenticationSerilaizer

    def get_serializer_class(self):
        if self.action == "login":
            return UserAuthenticationSerilaizer
        elif self.action == "register":
            return UserRegistrationSerilaizer
        return super().get_serializer_class()

    @action(
        methods=["post"],
        detail=False,
        url_path="logout",
        url_name="logout",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def logout(self, request, pk=None):
        """
        Удаляет текущую сессию пользователя.
        """
        logout(request)
        return Response(
            # {"detail": "Session has closed."}, status=status.HTTP_200_OK
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=["post"],
        detail=False,
        url_path="login",
        url_name="login",
    )
    def login(self, request, pk=None):
        """
        Принимает учетные данные и создает сессию.
        """
        if request.user.is_authenticated:
            return Response({"detail": "Authenticated already."})

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.filter(email=serializer.data.get("email")).first()

            if not user:
                return Response(
                    {"detail": "Not found in database."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not user.is_active:
                    return Response(
                    {"detail": "Account has been deleted."},
                    status=status.HTTP_404_NOT_FOUND,
                )                

            password = serializer.data.get("password")
            if user is not None and user.check_password(password):
                login(request, user)  # создание сессии и установка куки
                return Response(
                    {"detail": "Authentication completed."}, status=status.HTTP_200_OK
                )
        return Response(
            {"detail": "Wrong credentials."}, status=status.HTTP_401_UNAUTHORIZED
        )

    @action(
        methods=["post"],
        detail=False,
        url_path="register",
        url_name="register",
        permission_classes=(permissions.AllowAny,),
    )
    def register(self, request, pk=None):
        """Регистрация нового польователя.
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "detail": f"User {serializer.validated_data.get('username')} created successfully!"
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API-представление для манипуляции (CRUD) пользователями.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class GroupsViewSet(viewsets.ModelViewSet):
    """
    API-представление для манипуляции (CRUD) группами.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
