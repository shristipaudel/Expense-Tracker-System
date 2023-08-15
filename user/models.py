from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
import datetime

class CustomUser(AbstractUser):  # use this for extending deafult django auth system
    full_name = models.CharField(max_length=255)
    user_type = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='user_group_type',null=True, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# class UserType(models.Model):
#     user_type = models.CharField(max_length=30, choices=user_type_choice)

#     def __str__(self):
#         return self.user_type