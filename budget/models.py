from operator import truediv
from unicodedata import category, name
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.forms import CharField
# budget_choices = (
#     ("Master budget","Master budget"),
#     ("Operating budget","Operating budget"),
#     ("Cash budget","Cash budget"),
#     ("Financial budget","Financial budget"),
#     ("Static budget","Static budget"),
#     ("HR budget","HR budget"),
# )

class Budget(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #saving = models.DecimalField(max_digits=20, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.budget)
        

