from operator import truediv
from unicodedata import category
from django.db import models
from budget.models import Budget
from django.core.validators import MinValueValidator
from decimal import Decimal

class Expenses(models.Model):
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=30,blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    budget = models.ForeignKey(Budget,on_delete=models.CASCADE,related_name='budget')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} + " " + {self.updated_at}'