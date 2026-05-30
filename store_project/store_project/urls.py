from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),  # Conecta las URLs de la app product
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # Endpoint para obtener token de autenticación
]