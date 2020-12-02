from django.db import models
from django.contrib.auth.models import User
from product.models import Products


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_cart")
    item = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="product_cart")
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    created = models.DateTimeField(auto_now_add=True)
    bought = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "Cart"


STATE = (
    ('NAI', 'Nairobi'),
    ('KIS', 'Kisumu'),
    ('NAK', 'Nakuru'),
    ('ELD', 'Eldoret'),
    ('NAV', 'Naivasha'),
    ('MOM', 'Mombasa'),
)


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_order")
    orderedproduct = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00)
    vat_tax = models.IntegerField(default=15)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address_1 = models.CharField(max_length=200, null=True)
    address_2 = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, choices=STATE, null=True)
    zip_code = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = "Orders"
