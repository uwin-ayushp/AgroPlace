from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='products/photos')

    def __str__(self):
        return self.name


class Recommendation(models.Model):
    recommendation_order = models.IntegerField()
    score = models.FloatField()

    def __str__(self):
        return f"Recommendation {self.id}"