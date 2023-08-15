from django.db import models
from budget.models import Budget

class Saving(models.Model):
    budget = models.OneToOneField(Budget, on_delete = models.CASCADE)
    #saving = models.DecimalField(max_digits=20, decimal_places=2)
    #remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # return str(self.saving)
        return {self.budget}