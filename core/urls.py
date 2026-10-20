from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voluntario/cadastrar/', views.cadastrar_voluntario, name='cadastrar_voluntario'),
    path('ongs/', views.listar_ongs, name='listar_ongs'),
]
