from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    NAME_MAX_LENGTH = 255
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    NAME_MAX_LENGTH = 255
    MAX_PRICE_DIGITS = 10
    MAX_DECIMAL_PLACES = 2

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    description = models.TextField()
    price = models.DecimalField(max_digits=MAX_PRICE_DIGITS, decimal_places=MAX_DECIMAL_PLACES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    MAX_TOTAL_PRICE_DIGITS = 10
    MAX_DECIMAL_PLACES = 2

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=MAX_TOTAL_PRICE_DIGITS, decimal_places=MAX_DECIMAL_PLACES)
    cart_data = models.JSONField(default=dict)  # To store cart items

    def __str__(self):
        return f"Order #{self.id} by {self.user if self.user else 'Guest'}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review of {self.product.name} by {self.user.username}'

class Customer(models.Model):
    MAX_ADDRESS_LENGTH = 255
    MAX_PHONE_LENGTH = 15

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=MAX_ADDRESS_LENGTH)
    phone = models.CharField(max_length=MAX_PHONE_LENGTH)
