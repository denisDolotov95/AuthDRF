from django.contrib.auth.models import User
from rest_framework import permissions

from .models import AccessGroupRule, BusinessElement


class DynamicGroupPermission(permissions.BasePermission):
    """
    Проверяет права доступа, обращаясь к таблице access_roles_rules.
    """

    def __get_access(self, user: User, element: str):

        b_element = BusinessElement.objects.get(type=element)
        user_groups = user.groups.all()
        access = AccessGroupRule.objects.filter(
            group__in=user_groups.values("id"), element_id=b_element.id
        ).first()
        return access

    def has_permission(self, request, view):
        """
        Проверка доступа на уровне эндпоинта (создание, список).
        """
        user: User = request.user
        if not user.is_authenticated:
            return False

        # Определяем код элемента из атрибута View (его нужно добавить во View)
        element = getattr(view, "business_element", None)
        if not element:
            return False

        try:
            access = self.__get_access(user, element)

            if request.method == "GET":
                return access.read_permission or access.read_all_permission

            if request.method == "POST":
                return access.create_permission
            return True  # Для PATCH/DELETE проверяем в has_object_permission
        except AccessGroupRule.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Проверка доступа к конкретному объекту (владение).
        """
        user: User = request.user
        # Определяем код элемента из атрибута View (его нужно добавить во View)
        element = getattr(view, "business_element", None)

        try:
            access = self.__get_access(user, element)

            if request.method in permissions.SAFE_METHODS:  # GET
                return access.read_all_permission or (
                    access.read_permission and obj.creator_id == user.id
                )

            if request.method in ["PATCH", "PUT"]:
                return access.update_all_permission or (
                    access.update_permission and obj.creator_id == user.id
                )

            if request.method == "DELETE":
                return access.delete_all_permission or (
                    access.delete_permission and obj.creator_id == user.id
                )
        except AccessGroupRule.DoesNotExist:
            return False
