from django.urls import path
from . import views

urlpatterns = [
    path('prueba/', views.endpoint_prueba, name='endpoint_prueba'),
    path('health/', views.health_check, name='health_check'),
]