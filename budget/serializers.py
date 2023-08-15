from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import *

# class BudgetChoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BudgetChoices
#        # fields = ['id','name','des','amt','date']
#         fields = '__all__'

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        # fields = ['id','name']
        fields = '__all__'
     
