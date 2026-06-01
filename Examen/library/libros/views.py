from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Libro
from .serializers import LibroSerializer

@api_view(['GET'])
def libro_list(request):
    author = request.query_params.get('author', None)
    
    if author:
        libros = Libro.objects.filter(author__iexact=author)
        message = f'Books found for author: {author}'
    else:
        libros = Libro.objects.all()
        message = 'All books retrieved'
    
    serializer = LibroSerializer(libros, many=True)
    
    return Response({
        'message': message,
        'total': libros.count(),
        'data': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def libro_detail(request, id):
    try:
        libro = Libro.objects.get(id=id)
        serializer = LibroSerializer(libro)
        return Response({
            'message': 'Book found',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except Libro.DoesNotExist:
        return Response({
            'message': f'Book with id {id} not found',
            'error': 'Resource does not exist'
        }, status=status.HTTP_404_NOT_FOUND)