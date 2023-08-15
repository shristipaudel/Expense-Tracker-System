from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import Saving       
        
class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving 
        fields = '__all__'
        