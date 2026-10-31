from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Oportunidade, Depoimento, Perfil
from .forms import CadastroVoluntarioForm, CadastroONGForm, OportunidadeForm

def home(request):
    oportunidades = Oportunidade.objects.filter(ativa=True).order_by('-data_criacao')
    depoimentos = Depoimento.objects.all()[:3]
    return render(request, 'core/index.html', {
        'oportunidades': oportunidades,
        'depoimentos': depoimentos,
    })

def listar_ongs(request):
    ongs = Perfil.objects.filter(tipo='ONG')
    return render(request, 'core/ongs.html', {'ongs': ongs})

def cadastrar_voluntario(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CadastroVoluntarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Perfil.objects.create(
                user=user,
                tipo='VOLUNTARIO',
                telefone=form.cleaned_data.get('telefone', ''),
                cidade=form.cleaned_data.get('cidade', ''),
                habilidades=form.cleaned_data.get('habilidades', '')
            )

            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect('home')
    else:
        form = CadastroVoluntarioForm()
    return render(request, 'core/cadastrar_voluntario.html', {'form': form})

def cadastrar_ong(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CadastroONGForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Perfil.objects.create(
                user=user,
                tipo='ONG',
                telefone=form.cleaned_data.get('telefone', ''),
                cidade=form.cleaned_data.get('cidade', ''),
                mensagem=form.cleaned_data.get('mensagem', ''),
                foto=request.FILES.get('foto'),# <--- Adicionado foto
            )

            login(request, user)
            messages.success(request, "Cadastro de ONG realizado com sucesso!")
            return redirect('home')
    else:
        form = CadastroONGForm()
    return render(request, 'core/cadastrar_ong.html', {'form': form})

def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bem-vindo(a), {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    messages.info(request, "Sessão encerrada.")
    return redirect('home')

@login_required
def criar_oportunidade(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'ONG':
        messages.error(request, "Apenas Organizações/ONGs podem cadastrar novas oportunidades.")
        return redirect('home')

    if request.method == 'POST':
        form = OportunidadeForm(request.POST)
        if form.is_valid():
            oportunidade = form.save(commit=False)
            oportunidade.ong = request.user
            oportunidade.save()
            messages.success(request, "Oportunidade cadastrada com sucesso!")
            return redirect('home')
    else:
        form = OportunidadeForm()
    return render(request, 'core/criar_oportunidade.html', {'form': form})

@login_required
def inscrever_oportunidade(request, vaga_id):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'VOLUNTARIO':
        messages.error(request, "Apenas Voluntários podem se inscrever em oportunidades.")
        return redirect('home')

    vaga = get_object_or_404(Oportunidade, id=vaga_id)
    if request.user in vaga.inscritos.all():
        vaga.inscritos.remove(request.user)
        messages.info(request, "Inscrição cancelada.")
    else:
        vaga.inscritos.add(request.user)
        messages.success(request, "Inscrição realizada com sucesso!")

    return redirect('home')

@login_required
def editar_perfil_ong(request):
    perfil = get_object_or_404(Perfil, user=request.user, tipo='ONG')

    if request.method == 'POST':
        # Passamos request.POST, request.FILES e a instância do user logado
        form = CadastroONGForm(request.POST, request.FILES, instance=request.user)
        
        # Tornamos os campos de senha não obrigatórios na edição
        form.fields['password'].required = False
        if 'confirm_password' in form.fields:
            form.fields['confirm_password'].required = False

        if form.is_valid():
            user = form.save(commit=False)
            
            # Atualiza a senha apenas se o usuário preencheu o campo
            nova_senha = form.cleaned_data.get('password')
            if nova_senha:
                user.set_password(nova_senha)
            
            user.save()

            # Atualiza os dados do Perfil existente
            perfil.telefone = form.cleaned_data.get('telefone', perfil.telefone)
            perfil.cidade = form.cleaned_data.get('cidade', perfil.cidade)
            perfil.mensagem = form.cleaned_data.get('mensagem', perfil.mensagem)
            
            # Atualiza a foto se uma nova for enviada
            if request.FILES.get('foto'):
                perfil.foto = request.FILES['foto']
                
            perfil.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('listar_ongs')
    else:
        # Preenche o formulário com os dados atuais do User e do Perfil
        dados_iniciais = {
            'telefone': perfil.telefone,
            'cidade': perfil.cidade,
            'mensagem': perfil.mensagem,
        }
        form = CadastroONGForm(instance=request.user, initial=dados_iniciais)
        form.fields['password'].required = False
        if 'confirm_password' in form.fields:
            form.fields['confirm_password'].required = False

    return render(request, 'core/editar_perfil_ong.html', {'form': form})

@login_required
def minhas_oportunidades(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'ONG':
        messages.error(request, "Apenas ONGs têm acesso a esta página.")
        return redirect('home')

    # Busca apenas as vagas criadas pela ONG logada
    minhas_vagas = Oportunidade.objects.filter(ong=request.user).prefetch_related('inscritos__perfil').order_by('-data_criacao')
    
    return render(request, 'core/minhas_oportunidades.html', {'vagas': minhas_vagas})
