from django.urls import path
from . import views

urlpatterns = [
    path('libro/', views.libro_list, name='libro-list'),
    path('libro/<int:id>/', views.libro_detail, name='libro-detail'),
]