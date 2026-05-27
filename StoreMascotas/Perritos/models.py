from django.db import models

class Perrito(models.Model):
    Tamaño = [
        ('Small','Pequeño'),
        ('Medium','Mediano'),
        ('Large','Grande'),
    ]

    Energia = [
        ('Low','Baja'),
        ('Medium','Media'),
        ('High','Alta'),
        ('VeryHigh','Muy Alta'),
    ]

    Genero = [
        ('M','Macho'),
        ('F','Hembra')
    ]

    Nombre = models.CharField(max_length=100)
    Raza = models.CharField(max_length=100)
    Edad = models.IntegerField()
    Tamaño = models.CharField(max_length=10, choices=Tamaño)
    Peso = models.DecimalField(max_digits=5, decimal_places=2)
    Color = models.CharField(max_length=100)
    Vacunado = models.BooleanField()
    Adoptado = models.BooleanField()
    Energia = models.CharField(max_length=10, choices=Energia, default='Medium')
    Genero = models.CharField(max_length=1, choices=Genero)

    def __str__(self):
        return f"{self.Nombre} - {self.Raza}"