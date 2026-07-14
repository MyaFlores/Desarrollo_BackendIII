from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Modelo de Libro
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    published_year = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


# Modelo de Perfil (extiende User con rol)
class Profile(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('BIBLIOTECARIO', 'Bibliotecario'),
        ('CLIENTE', 'Cliente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


# Señal: Crear perfil automáticamente cuando se crea un usuario
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Primer usuario ADMIN, resto CLIENTE
        if User.objects.count() == 1:
            role = 'ADMIN'
        else:
            role = 'CLIENTE'
        Profile.objects.create(user=instance, role=role)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()