from django.shortcuts import render, redirect
from .models import Oportunidade, Depoimento, Perfil
from .forms import VoluntarioForm
from django.contrib.auth.models import User

def home(request):
    oportunidades = Oportunidade.objects.filter(ativa=True).order_by('-data_criacao')
    depoimentos = Depoimento.objects.all()[:3]
    context = {
        'oportunidades': oportunidades,
        'depoimentos': depoimentos,
    }
    return render(request, 'core/index.html', context)

def cadastrar_voluntario(request):
    if str(request.user) != 'AnonymousUser':
        print(f'usuário:{request.user} ')
        if request.method == 'POST':
            form = VoluntarioForm(request.POST)
            if form.is_valid():
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                user = User.objects.create_user(username=nome, email=email)

                perfil = form.save(commit=False)
                perfil.user = user
                perfil.tipo = 'VOLUNTARIO'
                perfil.save()

                return redirect('home')
        else:
            form = VoluntarioForm()
        return render(request, 'core/cadastrar_voluntario.html', {'form': form})
    

def listar_ongs(request):
    # Aqui você pode buscar as ONGs do banco (Perfil com tipo='ONG')
    # pylint: disable=no-member
    ongs = Perfil.objects.filter(tipo='ONG')
    return render(request, 'core/ongs.html', {'ongs': ongs})
