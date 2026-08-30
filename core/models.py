# pylint: disable=no-member, missing-docstring, invalid-str-returned, missing-final-newline
from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    TIPO_USUARIO = (
        ('VOLUNTARIO', 'Voluntário'),
        ('ONG', 'ONG / Organização'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='VOLUNTARIO')
    telefone = models.CharField(max_length=20, blank=True)
    cidade = models.CharField(max_length=100, blank=True)

    def __str__(self):
        nome = self.user.username if self.user else "Usuário sem conta"
        return f"{nome} ({self.get_tipo_display()})"


class Oportunidade(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    ong = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oportunidades')
    local = models.CharField(max_length=200)
    urgente = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return str(self.titulo)


class Depoimento(models.Model):
    nome = models.CharField(max_length=100)
    cargo_subtitulo = models.CharField(max_length=150)  # ex: Voluntária há 2 anos
    texto = models.TextField()
    foto_url = models.URLField(blank=True)

    def __str__(self):
        return str(self.nome)
