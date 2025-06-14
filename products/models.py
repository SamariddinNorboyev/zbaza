from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()

    def __str__(self):
        return self.name