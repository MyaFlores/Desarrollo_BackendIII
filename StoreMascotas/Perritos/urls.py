from django.urls import path
from . import views

urlpatterns = [
    path('dogs/', views.lista_perritos, name='lista_perritos'),
    path('dogs/<int:pk>/', views.perrito_detalle, name='perrito_detalle'),
    path('dogs/breed/<str:raza>/', views.perritos_por_raza, name='perritos_por_raza'),
    path('dogs/search/<str:nombre>/', views.buscar_por_nombre, name='buscar_por_nombre'),
    path('dogs/adoptable/', views.perritos_adoptables, name='perritos_adoptables'),
    path('dogs/puppies/', views.cachorros, name='cachorros'),
    path('dogs/high-energy/', views.alta_energia, name='alta_energia'),
]