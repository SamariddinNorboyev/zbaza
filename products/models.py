from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()
    price = models.IntegerField(default=1000)

    @property
    def total_price(self):
        return self.amount * self.price

    def __str__(self):
        return self.name