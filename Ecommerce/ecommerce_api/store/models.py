from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronica', 'Electrónica'),
        ('ropa', 'Ropa'),
        ('hogar', 'Hogar'),
        ('libros', 'Libros'),
        ('deportes', 'Deportes'),
        ('juguetes', 'Juguetes'),
        ('alimentos', 'Alimentos'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} (Stock: {self.stock})"

    class Meta:
        ordering = ['name']


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

    class Meta:
        ordering = ['-order_date']

    def calculate_total(self):
        """Calcula el total del pedido sumando los subtotales de los items"""
        total = self.items.aggregate(total=Sum('subtotal'))['total'] or 0
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        # Calcular subtotal automáticamente
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
        # Actualizar el total del pedido
        self.order.calculate_total()