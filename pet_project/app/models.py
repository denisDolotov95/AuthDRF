import uuid
from django.db import models
from django.contrib.auth.models import Group

# Create your models here.


# class Prodact(models.Model):
#     """
#     Объекты приложения: товары, заказы и т.д.
#     """

#     name = models.CharField(max_length=100, unique=True)
#     code = models.UUIDField(
#         default=uuid.uuid4(), unique=True, editable=False
#     )  # Например, 'orders', 'products'

#     def __str__(self):
#         return self.name


class BusinessElement(models.Model):
    """
    Объекты приложения: товары, заказы и т.д.
    """

    # ELEMENT_TYPE_CHOICES = [("order", "order"), ("product", "product")]

    type = models.CharField(max_length=100, unique=True)
    code = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )  # Например, 'orders', 'products'

    def __str__(self):
        return self.type


# class Order(models.Model):
#     """
#     Объекты приложения: товары, заказы и т.д.
#     """

#     name = models.CharField(max_length=100, unique=True)
#     element = models.ForeignKey(
#         BusinessElement, on_delete=models.CASCADE
#     )  # Например, 'orders', 'products'

#     def __str__(self):
#         return self.name


class AccessGroupRule(models.Model):
    """
    Правила доступа группы к элементам бизнеса.
    """

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)

    # Права на чтение
    read_permission = models.BooleanField(default=False)  # Свои
    read_all_permission = models.BooleanField(default=False)  # Все

    # Права на создание
    create_permission = models.BooleanField(default=False)

    # Права на обновление
    update_permission = models.BooleanField(default=False)  # Свои
    update_all_permission = models.BooleanField(default=False)  # Все

    # Права на удаление
    delete_permission = models.BooleanField(default=False)  # Свои
    delete_all_permission = models.BooleanField(default=False)  # Все

    class Meta:
        unique_together = ("group", "element")
