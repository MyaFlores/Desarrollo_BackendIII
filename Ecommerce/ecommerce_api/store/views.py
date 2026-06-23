from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Sum, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Product, Order, OrderItem
from .serializers import (
    CustomerSerializer, ProductSerializer, OrderSerializer,
    OrderCreateSerializer, ProductStockSerializer,
    TopProductSerializer, SalesByCategorySerializer, TopCustomerSerializer
)
from datetime import datetime

# ==========================================
# CRUD: Clientes
# ==========================================

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'city']
    ordering = ['name']


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# ==========================================
# CRUD: Productos con filtros
# ==========================================

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['price', 'stock', 'name']
    ordering = ['name']


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ==========================================
# CRUD: Pedidos
# ==========================================

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order_date', 'total_amount']
    ordering = ['-order_date']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


# ==========================================
# CONSULTAS AVANZADAS
# ==========================================

# 1. Obtener productos por categoría
@api_view(['GET'])
def products_by_category(request, category):
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products, many=True)
    return Response({
        'success': True,
        'category': category,
        'total': products.count(),
        'products': serializer.data
    })


# 2. Obtener productos con stock menor a 10 (alerta de inventario)
@api_view(['GET'])
def low_stock_products(request):
    products = Product.objects.filter(stock__lt=10).order_by('stock')
    serializer = ProductStockSerializer(products, many=True)
    return Response({
        'success': True,
        'total': products.count(),
        'products': serializer.data
    })


# 3. Obtener clientes con más compras realizadas
@api_view(['GET'])
def top_customers(request):
    # Agrupar por cliente y contar pedidos y total gastado
    customers = Customer.objects.annotate(
        total_orders=Count('orders'),
        total_spent=Sum('orders__total_amount')
    ).filter(total_orders__gt=0).order_by('-total_orders')

    data = [
        {
            'customer_id': c.id,
            'customer_name': c.name,
            'total_orders': c.total_orders,
            'total_spent': c.total_spent or 0
        }
        for c in customers[:10]  # Top 10
    ]

    return Response({
        'success': True,
        'total': len(data),
        'customers': data
    })


# 4. Obtener ventas totales por categoría
@api_view(['GET'])
def sales_by_category(request):
    from decimal import Decimal

    # Calcular ventas por categoría
    results = OrderItem.objects.values(
        'product__category'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('subtotal')
    ).order_by('-total_revenue')

    data = [
        {
            'category': item['product__category'],
            'total_quantity': item['total_quantity'],
            'total_revenue': item['total_revenue'] or 0
        }
        for item in results
    ]

    return Response({
        'success': True,
        'total': len(data),
        'categories': data
    })


# 5. Obtener los 5 productos más vendidos
@api_view(['GET'])
def top_products(request):
    # Agrupar por producto y sumar cantidades
    results = OrderItem.objects.values(
        'product_id',
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('subtotal')
    ).order_by('-total_quantity')[:5]

    data = [
        {
            'product_id': item['product_id'],
            'product_name': item['product__name'],
            'total_quantity': item['total_quantity'],
            'total_revenue': item['total_revenue'] or 0
        }
        for item in results
    ]

    return Response({
        'success': True,
        'total': len(data),
        'top_products': data
    })


# 6. Obtener pedidos en rango de fechas
@api_view(['GET'])
def orders_by_date_range(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({
            'success': False,
            'message': 'Debes proporcionar start_date y end_date (YYYY-MM-DD)'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return Response({
            'success': False,
            'message': 'Formato de fecha inválido. Usa YYYY-MM-DD'
        }, status=status.HTTP_400_BAD_REQUEST)

    orders = Order.objects.filter(
        order_date__date__gte=start,
        order_date__date__lte=end
    ).order_by('order_date')

    serializer = OrderSerializer(orders, many=True)

    return Response({
        'success': True,
        'start_date': start_date,
        'end_date': end_date,
        'total': orders.count(),
        'orders': serializer.data
    })


# 7. Dashboard de estadísticas
@api_view(['GET'])
def dashboard_stats(request):
    from django.db.models import Avg

    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    avg_order_value = Order.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0

    return Response({
        'success': True,
        'stats': {
            'total_customers': total_customers,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'average_order_value': round(avg_order_value, 2)
        }
    })