from django.contrib.auth.models import User
from django.db import models

from users.models import MyUser


class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()
    price = models.IntegerField(default=1000)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.amount * self.price

    def __str__(self):
        return self.name



class Actions(models.Model):
    by_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.product.name} by {self.by_user.username}'