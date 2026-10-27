from django.core.validators import MinValueValidator
from django.db import models

# Units: dimensions in centimetres, weight in kilograms, cost in any currency.
POSITIVE = [MinValueValidator(0.0001)]


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=64, unique=True)
    length = models.FloatField(validators=POSITIVE)
    width = models.FloatField(validators=POSITIVE)
    height = models.FloatField(validators=POSITIVE)
    weight = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Box(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # internal dimensions (usable space inside the box)
    length = models.FloatField(validators=POSITIVE)
    width = models.FloatField(validators=POSITIVE)
    height = models.FloatField(validators=POSITIVE)
    max_weight = models.FloatField(validators=POSITIVE)
    cost = models.DecimalField(max_digits=8, decimal_places=2,
                               validators=[MinValueValidator(0)])

    class Meta:
        verbose_name_plural = "boxes"

    def __str__(self):
        return self.name


class Order(models.Model):
    reference = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1,
                                           validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.sku}"
