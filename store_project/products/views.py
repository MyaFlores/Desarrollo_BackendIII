from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from .models import Product_1
from .serializers import ProductSerializer

# VISTA 1: Lista de productos
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])  # ← Agregar esta línea
def product_list(request):
    """GET: Listar todos los productos (público) | POST: Crear nuevo producto (requiere token)"""
    
    if request.method == 'GET':
        products = Product_1.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Solo usuarios autenticados pueden llegar aquí gracias a IsAuthenticatedOrReadOnly
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# VISTA 2: Detalle de producto
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])  # ← Agregar esta línea
def product_detail(request, pk):
    """GET: Obtener un producto (público) | PUT: Actualizar (requiere token) | DELETE: Eliminar (requiere token)"""
    
    try:
        product = Product_1.objects.get(pk=pk)
    except Product_1.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        # Público: cualquiera puede ver
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Solo autenticados pueden actualizar
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Solo autenticados pueden eliminar
        product.delete()
        return Response({'mensaje': 'Producto eliminado'}, status=status.HTTP_204_NO_CONTENT)