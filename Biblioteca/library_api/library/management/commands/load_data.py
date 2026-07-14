import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import Book, Profile

class Command(BaseCommand):
    help = 'Carga datos de prueba'

    def handle(self, *args, **kwargs):
        print("Cargando datos de prueba...")

        # Libros de prueba
        books_data = [
            {'title': 'Cien años de soledad', 'author': 'Gabriel García Márquez', 'isbn': '9788437604947', 'published_year': 1967},
            {'title': 'El amor en los tiempos del cólera', 'author': 'Gabriel García Márquez', 'isbn': '9780307951133', 'published_year': 1985},
            {'title': 'Don Quijote de la Mancha', 'author': 'Miguel de Cervantes', 'isbn': '9788420652492', 'published_year': 1605},
            {'title': 'La sombra del viento', 'author': 'Carlos Ruiz Zafón', 'isbn': '9788408073279', 'published_year': 2001},
            {'title': 'El Principito', 'author': 'Antoine de Saint-Exupéry', 'isbn': '9780156012195', 'published_year': 1943},
        ]

        for data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=data['isbn'],
                defaults=data
            )
            if created:
                print(f"Libro creado: {book.title}")

        # Crear usuarios adicionales de prueba
        users_data = [
            {'username': 'bibliotecario1', 'email': 'biblio1@email.com', 'password': 'Biblio123!', 'role': 'BIBLIOTECARIO'},
            {'username': 'cliente1', 'email': 'cliente1@email.com', 'password': 'Cliente123!', 'role': 'CLIENTE'},
            {'username': 'cliente2', 'email': 'cliente2@email.com', 'password': 'Cliente123!', 'role': 'CLIENTE'},
        ]

        for data in users_data:
            if not User.objects.filter(username=data['username']).exists():
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )
                # Asignar rol
                profile = user.profile
                profile.role = data['role']
                profile.save()
                print(f"Usuario creado: {user.username} - {data['role']}")

        print(f"\nResumen:")
        print(f"   - Usuarios: {User.objects.count()}")
        print(f"   - Libros: {Book.objects.count()}")