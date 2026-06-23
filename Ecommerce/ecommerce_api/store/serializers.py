from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem
from django.db import transaction
from decimal import Decimal

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'city']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'stock']


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'order_date', 'total_amount', 'items', 'items_count']

    def get_items_count(self, obj):
        return obj.items.count()


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'items']

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            # Validación: no permitir stock negativo
            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"Stock insuficiente para {product.name}. Disponible: {product.stock}"
                )

            # Crear OrderItem
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                subtotal=product.price * quantity
            )

            # Reducir inventario automáticamente
            product.stock -= quantity
            product.save()

        # Calcular total del pedido
        order.calculate_total()
        return order


class ProductStockSerializer(serializers.ModelSerializer):
    """Serializer para productos con bajo stock"""
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'stock']


class TopProductSerializer(serializers.Serializer):
    """Serializer para productos más vendidos"""
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)


class SalesByCategorySerializer(serializers.Serializer):
    """Serializer para ventas por categoría"""
    category = serializers.CharField()
    total_quantity = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)


class TopCustomerSerializer(serializers.Serializer):
    """Serializer para clientes con más compras"""
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField()
    total_orders = serializers.IntegerField()
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)