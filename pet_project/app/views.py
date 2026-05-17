from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from .serializers import GroupSerializer, UserSerializer, UserRegistrationSerilaizer


class RegisterUserViewSet(viewsets.ModelViewSet):
    """
    API-представление для регистрации нового пользователя.
    """

    queryset = User.objects.none()
    serializer_class = UserRegistrationSerilaizer
    permission_classes = (permissions.AllowAny,)  # доступ для всех

    def create(self, request, *args, **kwargs):

        serializer = UserRegistrationSerilaizer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": f"User {serializer.data.get('username')} created successfully!"
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
