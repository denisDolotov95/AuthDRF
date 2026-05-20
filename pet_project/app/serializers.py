from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import AccessGroupRule, BusinessElement, Order, Product


class UserAuthenticationSerilaizer(serializers.ModelSerializer):
    """
    Серилизатор для аутентификации новго пользователя.
    """

    email = serializers.EmailField(required=True, style={"input_type": "email"})
    password = serializers.CharField(required=True, style={"input_type": "password"})

    class Meta:

        model = User
        fields = ["email", "password"]


class UserRegistrationSerilaizer(serializers.ModelSerializer):
    """
    Серилизатор для регистрации новго пользователя.
    """

    first_name = serializers.CharField(
        write_only=True,
        required=True,
    )
    last_name = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    email = serializers.EmailField(
        write_only=True, required=True, style={"input_type": "email"}
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
            is_active=True,
        )
        return user


class UserInfoSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "is_superuser",
            "email",
            "date_joined",
            "last_login",
            "groups",
        ]
        read_only_fields = ["last_login", "date_joined", "is_superuser", "groups"]

    def validate_email(self, value):
        # Проверяем уникальность при создании нового пользователя
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "The user already exists with the current email address."
            )
        return value


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        # fields = [
        #     "url",
        #     "username",
        #     "first_name",
        #     "last_name",
        #     "is_superuser",
        #     "is_active",
        #     "email",
        #     "date_joined",
        # ]
        fields = "__all__"
        read_only_fields = ["date_joined", "is_active", "url"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ["url", "name"]


class BusinessElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessElement
        fields = "__all__"
        read_only_fields = ["code"]


class AccessGroupRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessGroupRule
        fields = "__all__"


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
        # fields = "__all__"

    def create(self, validated_data: dict) -> User:
        """
        Создает и возвращает новый ордер.
        """
        # Убираем 'password2', т.к. его нет в модели User
        b_element = BusinessElement.objects.get(type="order")
        order = Order.objects.create(**validated_data, element_id=b_element.id)
        return order


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]
        # fields = "__all__"

    def create(self, validated_data: dict) -> User:
        """
        Создает и возвращает новый продукт.
        """
        # Убираем 'password2', т.к. его нет в модели User
        b_element = BusinessElement.objects.get(type="product")
        prodact = Product.objects.create(**validated_data, element_id=b_element.id)
        return prodact
