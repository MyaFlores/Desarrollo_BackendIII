from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import admin


class Product_1(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
@admin.register(Product_1)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available')
    search_fields = ('name',)
    list_filter = ('is_available',)