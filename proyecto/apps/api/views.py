from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from .serializers import InfoSistemaSerializer

@api_view(['GET'])
def endpoint_prueba(request):
    ambiente = "development" if settings.DEBUG else "production"
    
    data = {
        "mensaje": "¡API funcionando correctamente!",
        "version": "1.0.0",
        "ambiente": ambiente,
        "estado": "activo"
    }
    
    serializer = InfoSistemaSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "healthy",
        "server": "running",
        "timestamp": "2026-05-09 15:30:00"
    }, status=status.HTTP_200_OK)