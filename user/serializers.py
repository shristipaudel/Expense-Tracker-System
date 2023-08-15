from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import CustomUser       
        
class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model =CustomUser 
        fields = '__all__'
        