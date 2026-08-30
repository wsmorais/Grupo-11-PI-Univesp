# pylint: disable=missing-module-docstring, missing-class-docstring
from django.contrib import admin
from .models import Perfil, Oportunidade, Depoimento


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'cidade', 'telefone')
    list_filter = ('tipo', 'cidade')
    search_fields = ('user__username', 'user__email', 'cidade')


@admin.register(Oportunidade)
class OportunidadeAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ong', 'local', 'urgente', 'ativa', 'data_criacao')
    list_filter = ('ativa', 'urgente', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'local', 'ong__username')


@admin.register(Depoimento)
class DepoimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo_subtitulo')
