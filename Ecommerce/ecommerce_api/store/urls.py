from django.urls import path
from . import views

urlpatterns = [
    # CRUD Clientes
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),

    # CRUD Productos
    path('products/', views.ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # CRUD Pedidos
    path('orders/', views.OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),

    # Consultas avanzadas
    path('products/category/<str:category>/', views.products_by_category, name='products-by-category'),
    path('products/low-stock/', views.low_stock_products, name='low-stock'),
    path('customers/top/', views.top_customers, name='top-customers'),
    path('analytics/sales-by-category/', views.sales_by_category, name='sales-by-category'),
    path('analytics/top-products/', views.top_products, name='top-products'),
    path('analytics/orders-by-date/', views.orders_by_date_range, name='orders-by-date'),
    path('analytics/dashboard/', views.dashboard_stats, name='dashboard'),
]