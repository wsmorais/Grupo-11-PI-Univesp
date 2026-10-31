from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('voluntario/cadastrar/', views.cadastrar_voluntario, name='cadastrar_voluntario'),
    path('ong/cadastrar/', views.cadastrar_ong, name='cadastrar_ong'),
    path('ongs/', views.listar_ongs, name='listar_ongs'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('oportunidades/criar/', views.criar_oportunidade, name='criar_oportunidade'),
    path('oportunidades/<int:vaga_id>/inscrever/', views.inscrever_oportunidade, name='inscrever_oportunidade'),
    path('ong/editar/', views.editar_perfil_ong, name='editar_perfil_ong'),
    path('minhas-oportunidades/', views.minhas_oportunidades, name='minhas_oportunidades'),
]