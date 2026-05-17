from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserRegistrationSerilaizer(serializers.ModelSerializer):
    """
    Серилизатор для регистрации новго пользователя.
    Использует ModelSerializer, т.к. работаем с моделью User.
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:

        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Без возврата пароля через GET

    def validate(self, data: dict) -> dict:
        """
        Проверка совпадения пароля.
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords must be the same."}
            )
        return data

    def create(self, validated_data: dict) -> User:
        """
        Создает и возвращает нового пользователя, хешируя пароль.
        """
        # Убираем 'password2', т.к. его нет в модели User
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
        )
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ["url", "name"]
