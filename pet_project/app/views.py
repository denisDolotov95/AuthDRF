# import logging

from django.contrib.auth.models import Group, User

# from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, logout
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

# from rest_framework.exceptions import MethodNotAllowed
# from rest_framework.views import APIView

from .serializers import (
    GroupSerializer,
    MyInfoSerializer,
    MyInfoEditSerializer,
    UserSerializer,
    UserRegistrationSerilaizer,
    UserLoginSerilaizer,
    UserLogoutSerilaizer,
)


class UserDeleteViewSet(viewsets.ModelViewSet):

    http_method_names = ["get", "delete"]

    serializer_class = MyInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return User.objects.filter(id=self.request.user.id)

    def delete(self, request):

        if request.user.is_active:
            request.user.is_active = False
            request.user.save()
            logout(request)
            return Response({"detail": "Account is deleted"})


class LoginUserViewSet(viewsets.ModelViewSet):
    """
    API-представление для аутентификации пользователя.
    """

    queryset = User.objects.none()
    serializer_class = UserLoginSerilaizer

    def create(self, request):
        """
        Принимает учетные данные и создает сессию.
        """

        if request.user.is_authenticated:
            return Response({"detail": "Authenticated already."})

        serializer = UserLoginSerilaizer(data=request.data)

        if serializer.is_valid():

            user = User.objects.filter(email=serializer.data.get("email")).first()

            if not user:
                return Response({"detail": "Not found in database."})

            password = serializer.data.get("password")

            if user is not None and user.is_active and user.check_password(password):

                login(request, user)  # создание сессии и установка куки

                user.is_active = True
                user.save()

                return Response(
                    {"detail": "Authentication completed."}, status=status.HTTP_200_OK
                )

        return Response(
            {"detail": "Wrong credentials."}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutUserViewSet(viewsets.ModelViewSet):
    """
    API-представление для завершения сессии (Logout).
    """

    serializer_class = UserLogoutSerilaizer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def create(self, request):
        """
        Удаляет текущую сессию пользователя.
        """

        logout(request)

        return Response(
            {"detail": "Session has closed."}, status=status.HTTP_204_NO_CONTENT
        )


class RegisterUserViewSet(viewsets.ModelViewSet):
    """
    API-представление для регистрации нового пользователя.
    """

    queryset = User.objects.none()
    serializer_class = UserRegistrationSerilaizer
    permission_classes = (permissions.AllowAny,)  # доступ для всех

    def create(self, request):

        serializer = UserRegistrationSerilaizer(data=request.data)

        if serializer.is_valid():
            serializer.save(is_active=False)
            return Response(
                {
                    "message": f"User {serializer.validated_data.get('username')} created successfully!"
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API-представление для просмотра своего профиля пользовтеля.
    """

    serializer_class = MyInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


# class MyInfoEditViewSet(viewsets.ModelViewSet):
#     """
#     API-представление для изменения своего профиля пользовтеля.
#     """

#     http_method_names = ["patch"]

#     serializer_class = MyInfoEditSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):

#         return User.objects.filter(id=self.request.user.id)


class UserViewSet(viewsets.ModelViewSet):
    """
    API-представление для просмотра своего профиля пользовтеля.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class GroupsViewSet(viewsets.ModelViewSet):
    """
    API-представление для просмотра и добавления групп пользователей.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
