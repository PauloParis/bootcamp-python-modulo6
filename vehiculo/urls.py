from django.urls import path

from .views import inicio, agregar, listar, editar, eliminar, register, login_View, logout_view


urlpatterns = [
    path('', inicio, name='inicio'),
    path('vehiculo/add', agregar, name='agregar'),
    path('vehiculo/list', listar, name='listar'),
    path('vehiculo/edit/<int:id>', editar, name='editar'),
    path('vehiculo/delete/<int:id>', eliminar, name='eliminar'),
    path('register/', register, name='register'),
    path('login/', login_View, name='login'),
    path('logout/', logout_view, name='logout'),
]