from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Registro y Login
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    # Refresh Token (usando la vista de SimpleJWT)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Perfil (protegido)
    path('profile/', views.profile, name='profile'),
]