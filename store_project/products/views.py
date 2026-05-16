from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product_1
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    """GET: Listar todos los productos | POST: Crear nuevo producto"""
    if request.method == 'GET':
        products = Product_1.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """GET: Obtener un producto | PUT: Actualizar | DELETE: Eliminar"""
    try:
        product = Product_1.objects.get(pk=pk)
    except Product_1.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response({'mensaje': 'Producto eliminado'}, status=status.HTTP_204_NO_CONTENT)