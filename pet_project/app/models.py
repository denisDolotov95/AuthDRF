import uuid

from django.contrib.auth.models import Group, User
from django.db import models
from django.utils import timezone

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

    created_at = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=False)
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE
    )  # Например, 'order', 'product'

    def __str__(self):
        return f"Заказ №{self.id} от {self.creator.username}"


class Product(models.Model):
    """
    Объекты приложения: заказы.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, default=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=False
    )
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=False)
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE
    )  # Например, 'orders', 'products'

    def __str__(self):
        return f"Продукт №{self.id} / {self.name} от {self.creator.username}, цена {self.price}"


class OrderItem(models.Model):
    """
    Промежуточная таблица (Позиции заказа).
    Связывает Order и Product.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE, default=False
    )  # Например, 'orders', 'products'


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
