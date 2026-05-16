from rest_framework import serializers
from .models import Product_1

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product_1
        fields = '__all__'  