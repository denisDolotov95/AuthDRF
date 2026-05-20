import uuid

from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.


class BusinessElement(models.Model):
    """
    Объекты приложения: товары, заказы и т.д.
    """

    # ELEMENT_TYPE_CHOICES = [("order", "order"), ("product", "product")]

    type = models.CharField(max_length=100, unique=True)
    code = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )  # Например, 'order', 'product'

    def __str__(self):
        return self.type


class Order(models.Model):
    """
    Объекты приложения: ордера.
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default=False)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=False)
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE
    )  # Например, 'order', 'product'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Объекты приложения: заказы.
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default=False)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=False)
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE
    )  # Например, 'orders', 'products'

    def __str__(self):
        return self.name


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
