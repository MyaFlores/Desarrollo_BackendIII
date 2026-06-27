from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer


# ==========================================
# 1. REGISTRO DE USUARIOS
# POST /api/register/
# ==========================================
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registra un nuevo usuario en el sistema.
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Generar tokens JWT para el usuario registrado
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Error de validación',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


# ==========================================
# 2. LOGIN
# POST /api/login/
# ==========================================
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Autentica a un usuario y devuelve tokens JWT.
    """
    serializer = LoginSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'message': 'Error de validación',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    
    # Autenticar usuario
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({
            'success': False,
            'message': 'Credenciales inválidas',
            'error': 'Usuario o contraseña incorrectos'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'success': True,
        'message': 'Login exitoso',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        },
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)


# ==========================================
# 3. REFRESH TOKEN
# POST /api/token/refresh/
# ==========================================
# Usaremos la vista de SimpleJWT directamente en las URLs


# ==========================================
# 4. PERFIL DE USUARIO AUTENTICADO
# GET /api/profile/
# ==========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Obtiene la información del usuario autenticado.
    """
    user = request.user
    serializer = UserSerializer(user)
    
    return Response({
        'success': True,
        'message': 'Perfil obtenido exitosamente',
        'user': serializer.data
    }, status=status.HTTP_200_OK)