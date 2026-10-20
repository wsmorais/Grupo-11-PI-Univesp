from django import forms
from .models import Perfil

class VoluntarioForm(forms.ModelForm):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = Perfil
        fields = ['telefone', 'cidade', 'habilidades', 'mensagem']
        labels = {
            'telefone': 'Telefone',
            'cidade': 'Cidade',
            'habilidades': 'Habilidades / Área',
            'mensagem': 'Mensagem',
        }
        widgets = {
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'habilidades': forms.TextInput(attrs={'class': 'form-control'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control'}),
        }
