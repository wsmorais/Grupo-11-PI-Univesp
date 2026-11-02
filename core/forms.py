from django import forms
from .models import Depoimento
from django.contrib.auth.models import User
from .models import Perfil, Oportunidade

class CadastroVoluntarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Senha", required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirme a Senha", required=False)
    telefone = forms.CharField(max_length=20, required=False, label="Telefone")
    cidade = forms.CharField(max_length=100, required=False, label="Cidade")
    habilidades = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Habilidades")
    foto = forms.ImageField(required=False, label="Foto de Perfil")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'foto', 'telefone', 'cidade', 'habilidades']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se o formulário receber uma instância (ou seja, estiver EDITANDO um perfil existente),
        # bloqueia o campo username para alteração
        if self.instance and self.instance.pk:
            self.fields['username'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        
        # Exige validação de senha apenas no cadastro (quando for um novo usuário)
        if not self.instance.pk and (not p1 or not p2):
            raise forms.ValidationError("Informe e confirme a senha.")

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
        fields = ['texto', 'cargo_subtitulo']  # 'foto_url' removido daqui
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
        }