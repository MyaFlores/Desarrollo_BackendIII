from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('me/', views.me, name='me'),

    # Libros
    path('books/', views.BookListCreateView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),

    # Usuarios (solo admin)
    path('users/', views.user_list, name='user-list'),
    path('users/<int:id>/assign-role/', views.assign_role, name='assign-role'),
]