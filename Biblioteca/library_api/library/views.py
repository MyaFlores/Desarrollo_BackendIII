from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Book, Profile
from .serializers import (
    UserSerializer, RegisterSerializer, AssignRoleSerializer,
    BookSerializer
)
from .permissions import (
    IsAdmin, IsBibliotecario, IsAdminOrBibliotecario,
    IsAdminOrReadOnly
)

# ==========================================
# REGISTRO
# POST /api/register/
# ==========================================
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# LOGIN
# POST /api/login/
# ==========================================
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            'success': False,
            'message': 'Usuario y contraseña son obligatorios'
        }, status=status.HTTP_400_BAD_REQUEST)

    from django.contrib.auth import authenticate
    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
            'success': False,
            'message': 'Credenciales inválidas'
        }, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'success': True,
        'message': 'Login exitoso',
        'user': UserSerializer(user).data,
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)


# ==========================================
# PERFIL DEL USUARIO AUTENTICADO
# GET /api/me/
# ==========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response({
        'success': True,
        'user': serializer.data
    }, status=status.HTTP_200_OK)


# ==========================================
# CRUD DE LIBROS
# ==========================================

# GET /api/books/ - Todos los autenticados
# POST /api/books/ - ADMIN y BIBLIOTECARIO
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminOrBibliotecario()]


# GET /api/books/{id}/ - Todos los autenticados
# PUT /api/books/{id}/ - ADMIN y BIBLIOTECARIO
# DELETE /api/books/{id}/ - ADMIN
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'DELETE':
            return [IsAdmin()]
        else:  # PUT
            return [IsAdminOrBibliotecario()]


# ==========================================
# ADMIN: ASIGNAR ROLES
# POST /api/users/{id}/assign-role/
# ==========================================
@api_view(['POST'])
@permission_classes([IsAdmin])
def assign_role(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AssignRoleSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    role = serializer.validated_data['role']
    profile = user.profile
    old_role = profile.role
    profile.role = role
    profile.save()

    return Response({
        'success': True,
        'message': f'Rol actualizado de "{old_role}" a "{role}"',
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


# ==========================================
# ADMIN: VER USUARIOS
# GET /api/users/
# ==========================================
@api_view(['GET'])
@permission_classes([IsAdmin])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({
        'success': True,
        'total': users.count(),
        'users': serializer.data
    }, status=status.HTTP_200_OK)