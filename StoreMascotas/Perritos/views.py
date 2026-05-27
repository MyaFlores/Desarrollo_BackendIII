from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Perrito
from .serializers import PerritoSerializer

# Helper para respuestas personalizadas
def custom_response(data, message="Success", total=None, status_code=status.HTTP_200_OK):
    response_data = {
        "message": message,
        "total": total if total is not None else len(data) if isinstance(data, list) else 1,
        "data": data
    }
    return Response(response_data, status=status_code)

# 1. Consulta general + Filtros + Ordenamiento
@api_view(['GET'])
def lista_perritos(request):
    queryset = Perrito.objects.all()
    
    # Filtros por query parameters (usando los nombres de campos CORRECTOS)
    min_edad = request.query_params.get('min_age')
    max_edad = request.query_params.get('max_age')
    vacunado = request.query_params.get('vaccinated')
    tamanio = request.query_params.get('size')
    adoptado = request.query_params.get('adopted')
    raza = request.query_params.get('breed')
    energia = request.query_params.get('energy')
    genero = request.query_params.get('gender')
    
    if min_edad:
        queryset = queryset.filter(Edad__gte=int(min_edad))  # ← Edad con mayúscula
    if max_edad:
        queryset = queryset.filter(Edad__lte=int(max_edad))  # ← Edad con mayúscula
    if vacunado is not None:
        queryset = queryset.filter(Vacunado=vacunado.lower() == 'true')  # ← Vacunado
    if tamanio:
        queryset = queryset.filter(Tamaño=tamanio)  # ← Tamaño
    if adoptado is not None:
        queryset = queryset.filter(Adoptado=adoptado.lower() == 'true')  # ← Adoptado
    if raza:
        queryset = queryset.filter(Raza__iexact=raza)  # ← Raza
    if energia:
        queryset = queryset.filter(Energia=energia)  # ← Energia
    if genero:
        queryset = queryset.filter(Genero=genero.upper())  # ← Genero
    
    # Ordenamiento
    ordering = request.query_params.get('ordering')
    if ordering:
        # Convertir nombres de campos a mayúsculas para ordenamiento
        ordering_map = {
            'edad': 'Edad',
            '-edad': '-Edad',
            'peso': 'Peso',
            '-peso': '-Peso',
            'nombre': 'Nombre',
            '-nombre': '-Nombre',
        }
        django_ordering = ordering_map.get(ordering, ordering)
        queryset = queryset.order_by(django_ordering)
    
    serializer = PerritoSerializer(queryset, many=True)
    return custom_response(serializer.data, "Dogs retrieved successfully", queryset.count())

# 2. Consulta por ID
@api_view(['GET'])
def perrito_detalle(request, pk):
    try:
        perrito = Perrito.objects.get(pk=pk)
        serializer = PerritoSerializer(perrito)
        return custom_response(serializer.data, "Dog found")
    except Perrito.DoesNotExist:
        return Response({
            "message": f"Dog with id {pk} not found",
            "error": "Resource does not exist"
        }, status=status.HTTP_404_NOT_FOUND)

# 3. Consulta por raza (path parameter)
@api_view(['GET'])
def perritos_por_raza(request, raza):
    queryset = Perrito.objects.filter(Raza__iexact=raza)  # ← Raza con mayúscula
    if not queryset.exists():
        return Response({
            "message": f"No dogs found for breed: {raza}",
            "total": 0,
            "data": []
        }, status=status.HTTP_200_OK)
    
    serializer = PerritoSerializer(queryset, many=True)
    return custom_response(serializer.data, f"Dogs of breed {raza}", queryset.count())

# 4. Búsqueda por nombre (path parameter)
@api_view(['GET'])
def buscar_por_nombre(request, nombre):
    queryset = Perrito.objects.filter(Nombre__icontains=nombre)  # ← Nombre con mayúscula
    serializer = PerritoSerializer(queryset, many=True)
    mensaje = f"Found {queryset.count()} dogs matching '{nombre}'"
    return custom_response(serializer.data, mensaje, queryset.count())

# 5. Endpoint personalizado: Perritos adoptables
@api_view(['GET'])
def perritos_adoptables(request):
    queryset = Perrito.objects.filter(Adoptado=False, Vacunado=True).exclude(Energia='low')  # ← Mayúsculas
    serializer = PerritoSerializer(queryset, many=True)
    return custom_response(serializer.data, "Adoptable dogs (vaccinated, not adopted, medium/high energy)", queryset.count())

# 6. Endpoint personalizado: Cachorros (edad < 12 meses)
@api_view(['GET'])
def cachorros(request):
    queryset = Perrito.objects.filter(Edad__lt=12)  # ← Edad con mayúscula (¡CORREGIDO!)
    serializer = PerritoSerializer(queryset, many=True)
    return custom_response(serializer.data, "Puppies (age < 12 months)", queryset.count())

# 7. Endpoint personalizado: Alta energía
@api_view(['GET'])
def alta_energia(request):
    queryset = Perrito.objects.filter(Energia='high')  # ← Energia con mayúscula
    serializer = PerritoSerializer(queryset, many=True)
    return custom_response(serializer.data, "High energy dogs", queryset.count())