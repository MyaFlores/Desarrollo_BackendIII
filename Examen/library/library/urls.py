from django.contrib import admin
from django.urls import include, path
from libros import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('libros.urls')),
]
