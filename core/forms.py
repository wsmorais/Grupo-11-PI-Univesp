from django import forms
from .models import Depoimento
from django.contrib.auth.models import User
from .models import Perfil, Oportunidade

class CadastroVoluntarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirme a Senha")
    telefone = forms.CharField(max_length=20, required=False, label="Telefone")
    cidade = forms.CharField(max_length=100, required=False, label="Cidade")
    habilidades = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Habilidades")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data


class CadastroONGForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirme a Senha")
    telefone = forms.CharField(max_length=20, required=False, label="Telefone")
    cidade = forms.CharField(max_length=100, required=False, label="Cidade")
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Sobre a ONG", required=False)
    foto = forms.ImageField(label="Logo / Imagem da ONG", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data


class OportunidadeForm(forms.ModelForm):
    class Meta:
        model = Oportunidade
        fields = ['titulo', 'descricao', 'local', 'urgente']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Tutor de Matemática'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva as atividades...'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: São Paulo - SP'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DepoimentoForm(forms.ModelForm):
    class Meta:
        model = Depoimento
        fields = ['texto', 'cargo_subtitulo', 'foto_url']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte como foi sua experiência como voluntário...'
            }),
            'cargo_subtitulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Voluntário há 2 anos'
            }),
            'foto_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL da foto (opcional)'
            }),
        }