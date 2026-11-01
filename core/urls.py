from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ongs/', views.listar_ongs, name='listar_ongs'),
    path('historias/', views.historias, name='historias'),
    path('oportunidades/', views.listar_oportunidades, name='listar_oportunidades'),
    
    # Suporta ambos os nomes para evitar NoReverseMatch
    path('login/', views.login_usuario, name='login'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout'),
    path('logout/', views.logout_usuario, name='logout_usuario'),

    path('cadastrar/voluntario/', views.cadastrar_voluntario, name='cadastrar_voluntario'),
    path('cadastrar/ong/', views.cadastrar_ong, name='cadastrar_ong'),
    path('perfil/ong/editar/', views.editar_perfil_ong, name='editar_perfil_ong'),
    
    path('oportunidades/nova/', views.criar_oportunidade, name='criar_oportunidade'),
    path('oportunidades/minhas/', views.minhas_oportunidades, name='minhas_oportunidades'),
    path('oportunidades/<int:vaga_id>/inscrever/', views.inscrever_oportunidade, name='inscrever_oportunidade'),
    path('oportunidades/<int:vaga_id>/editar/', views.editar_oportunidade, name='editar_oportunidade'),
    path('oportunidades/<int:vaga_id>/deletar/', views.deletar_oportunidade, name='deletar_oportunidade'),    
    path('api/mapa/oportunidades/', views.api_oportunidades_mapa, name='api_oportunidades_mapa'),
]