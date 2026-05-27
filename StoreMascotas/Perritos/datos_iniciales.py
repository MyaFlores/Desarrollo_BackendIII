import os
import sys
import django

# Agregar la ruta del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar la variable de entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mascotas.settings')

# Inicializar Django
django.setup()

from Perritos.models import Perrito

# NOTA: Los nombres de los campos deben coincidir EXACTAMENTE con tu modelo
# Según el error, los campos son: Nombre, Raza, Edad, Tamaño, Peso, Color, Vacunado, Adoptado, Energia, Genero

perritos_muestra = [
    {"Nombre": "Walle", "Raza": "Pug", "Edad": 8, "Tamaño": "small", "Peso": 6.5, "Color": "Beige", "Vacunado": True, "Adoptado": False, "Energia": "medium", "Genero": "M"},
    {"Nombre": "Luna", "Raza": "Golden Retriever", "Edad": 24, "Tamaño": "large", "Peso": 28.0, "Color": "Dorado", "Vacunado": True, "Adoptado": True, "Energia": "high", "Genero": "F"},
    {"Nombre": "Max", "Raza": "Chihuahua", "Edad": 36, "Tamaño": "small", "Peso": 2.5, "Color": "Marrón", "Vacunado": False, "Adoptado": False, "Energia": "high", "Genero": "M"},
    {"Nombre": "Bella", "Raza": "Bulldog", "Edad": 15, "Tamaño": "medium", "Peso": 22.0, "Color": "Blanco", "Vacunado": True, "Adoptado": False, "Energia": "low", "Genero": "F"},
    {"Nombre": "Rocky", "Raza": "Pastor Alemán", "Edad": 10, "Tamaño": "large", "Peso": 30.0, "Color": "Negro", "Vacunado": True, "Adoptado": True, "Energia": "high", "Genero": "M"},
    {"Nombre": "Coco", "Raza": "French Poodle", "Edad": 6, "Tamaño": "small", "Peso": 4.0, "Color": "Blanco", "Vacunado": True, "Adoptado": False, "Energia": "high", "Genero": "M"},
    {"Nombre": "Nala", "Raza": "Husky", "Edad": 18, "Tamaño": "large", "Peso": 25.0, "Color": "Gris", "Vacunado": True, "Adoptado": False, "Energia": "high", "Genero": "F"},
]

def cargar_datos():
    """Carga los perritos de muestra en la base de datos"""
    for data in perritos_muestra:
        perrito, created = Perrito.objects.get_or_create(Nombre=data["Nombre"], defaults=data)
        if created:
            print(f"✅ Creado: {perrito.Nombre}")
        else:
            print(f"⏭️ Ya existía: {perrito.Nombre}")
    
    print(f"\n📊 Total de perritos en la BD: {Perrito.objects.count()}")

if __name__ == "__main__":
    cargar_datos()