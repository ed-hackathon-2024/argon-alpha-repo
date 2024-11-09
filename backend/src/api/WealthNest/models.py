# WealthNest/models.py
from django.db import models

class User(models.Model):

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20)
    user_goal = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.age} years old)"

class Product(models.Model):
    name = models.TextField()
    category = models.TextField()
    sub_category = models.TextField()
    price = models.FloatField()
    vat_rate = models.FloatField()
    organization_id = models.TextField()
    org_unit_id = models.TextField()
    created_date = models.TextField()