from django.db import models
from django.contrib.auth.models import User
from geopy.geocoders import Nominatim

class Perfil(models.Model):
    TIPO_USUARIO = (
        ('VOLUNTARIO', 'Voluntário'),
        ('ONG', 'ONG / Organização'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='VOLUNTARIO')
    telefone = models.CharField(max_length=20, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    habilidades = models.CharField(max_length=200, blank=True)
    mensagem = models.TextField(blank=True)
    foto = models.ImageField(upload_to='ongs/', null=True, blank=True)

    def __str__(self):
        nome = self.user.username if self.user else "Usuário sem conta"
        return f"{nome} ({self.get_tipo_display()})"


class Depoimento(models.Model):
    nome = models.CharField(max_length=100)
    cargo_subtitulo = models.CharField(max_length=150)
    texto = models.TextField()
    foto_url = models.URLField(blank=True)

    def __str__(self):
        return str(self.nome)


class Oportunidade(models.Model):
    ong = models.ForeignKey(User, on_delete=models.CASCADE, related_name='oportunidades')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    local = models.CharField(max_length=255)
    urgente = models.BooleanField(default=False)
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    inscritos = models.ManyToManyField(User, related_name='inscricoes', blank=True)
    
    # Coordenadas para o Google Maps
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Busca latitude e longitude automaticamente pelo endereço se estiverem vazias
        if self.local and not (self.latitude and self.longitude):
            try:
                geolocator = Nominatim(user_agent="voluntarios_hub")
                location = geolocator.geocode(self.local, timeout=10)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except Exception as e:
                print(f"Erro ao obter coordenadas geográficas: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo