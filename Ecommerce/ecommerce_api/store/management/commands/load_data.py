import random
from django.core.management.base import BaseCommand
from store import models
from store.models import Customer, Product, Order, OrderItem
from decimal import Decimal
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Carga datos de prueba (15 productos, 10 clientes, 30 pedidos)'

    def handle(self, *args, **kwargs):
        print("🚀 Cargando datos de prueba...")

        # ========== PRODUCTOS (15) ==========
        products_data = [
            # Electrónica
            {'name': 'Smartphone X100', 'category': 'electronica', 'price': 5999.99, 'stock': 50},
            {'name': 'Laptop Pro 15"', 'category': 'electronica', 'price': 15999.99, 'stock': 30},
            {'name': 'Auriculares Bluetooth', 'category': 'electronica', 'price': 899.99, 'stock': 100},
            {'name': 'Televisor 4K 55"', 'category': 'electronica', 'price': 8999.99, 'stock': 20},
            # Ropa
            {'name': 'Camiseta Básica', 'category': 'ropa', 'price': 299.99, 'stock': 200},
            {'name': 'Jeans Clásico', 'category': 'ropa', 'price': 799.99, 'stock': 150},
            {'name': 'Chaqueta de Cuero', 'category': 'ropa', 'price': 2999.99, 'stock': 40},
            # Hogar
            {'name': 'Sillón Reclinable', 'category': 'hogar', 'price': 4999.99, 'stock': 25},
            {'name': 'Juego de Sábanas', 'category': 'hogar', 'price': 599.99, 'stock': 80},
            {'name': 'Lámpara de Pie', 'category': 'hogar', 'price': 899.99, 'stock': 60},
            # Libros
            {'name': 'Cien años de soledad', 'category': 'libros', 'price': 349.99, 'stock': 50},
            {'name': 'El Principito', 'category': 'libros', 'price': 249.99, 'stock': 70},
            # Deportes
            {'name': 'Balón de Fútbol', 'category': 'deportes', 'price': 499.99, 'stock': 90},
            {'name': 'Raqueta de Tenis', 'category': 'deportes', 'price': 1299.99, 'stock': 35},
            # Juguetes
            {'name': 'Robot Programable', 'category': 'juguetes', 'price': 1499.99, 'stock': 20},
        ]

        products = []
        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'category': data['category'],
                    'price': data['price'],
                    'stock': data['stock']
                }
            )
            products.append(product)
            if created:
                print(f"✅ Producto creado: {product.name}")

        # ========== CLIENTES (10) ==========
        customers_data = [
            {'name': 'Ana García', 'email': 'ana@email.com', 'city': 'Ciudad de México'},
            {'name': 'Carlos López', 'email': 'carlos@email.com', 'city': 'Guadalajara'},
            {'name': 'María Fernández', 'email': 'maria@email.com', 'city': 'Monterrey'},
            {'name': 'José Martínez', 'email': 'jose@email.com', 'city': 'Puebla'},
            {'name': 'Laura Rodríguez', 'email': 'laura@email.com', 'city': 'Ciudad de México'},
            {'name': 'Miguel Sánchez', 'email': 'miguel@email.com', 'city': 'Guadalajara'},
            {'name': 'Sofía Pérez', 'email': 'sofia@email.com', 'city': 'Monterrey'},
            {'name': 'David González', 'email': 'david@email.com', 'city': 'Querétaro'},
            {'name': 'Elena Gómez', 'email': 'elena@email.com', 'city': 'Puebla'},
            {'name': 'Javier Ruiz', 'email': 'javier@email.com', 'city': 'Ciudad de México'},
        ]

        customers = []
        for data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=data['email'],
                defaults={'name': data['name'], 'city': data['city']}
            )
            customers.append(customer)
            if created:
                print(f"✅ Cliente creado: {customer.name}")

        # ========== PEDIDOS (30) ==========
        order_count = 0
        start_date = datetime.now() - timedelta(days=90)

        for i in range(30):
            customer = random.choice(customers)
            order = Order.objects.create(
                customer=customer,
                order_date=start_date + timedelta(days=random.randint(1, 90))
            )

            # Cada pedido tiene 1-4 items
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, min(num_items, len(products)))

            for product in selected_products:
                quantity = random.randint(1, 5)
                if product.stock >= quantity:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        subtotal=product.price * quantity
                    )
                    product.stock -= quantity
                    product.save()

            order.calculate_total()
            order_count += 1
            print(f"✅ Pedido #{order.id}: {customer.name} - ${order.total_amount}")

        # ========== RESUMEN ==========
        print(f"\n📊 Resumen:")
        print(f"   - Clientes: {Customer.objects.count()}")
        print(f"   - Productos: {Product.objects.count()}")
        print(f"   - Pedidos: {Order.objects.count()}")
        print(f"   - Items: {OrderItem.objects.count()}")
        print(f"   - Ventas totales: ${Order.objects.aggregate(total=models.Sum('total_amount'))['total'] or 0}")