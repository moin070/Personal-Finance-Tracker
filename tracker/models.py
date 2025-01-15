from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')

    def __str__(self):
        return f"{self.amount} - {self.description}"

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.amount} - {self.description}"


# tracker/models.py


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, null=True, blank=True)  # Optional for category-specific budgets
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.category or 'Overall'} Budget for {self.month}/{self.year}"
