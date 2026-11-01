import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail

from .models import Oportunidade, Depoimento, Perfil
from .forms import (
    CadastroVoluntarioForm, 
    CadastroONGForm, 
    OportunidadeForm, 
    DepoimentoForm
)

# ==========================================
# PÁGINAS PÚBLICAS & NAVEGAÇÃO
# ==========================================

def home(request):
    oportunidades = Oportunidade.objects.filter(ativa=True).select_related('ong').order_by('-data_criacao')[:6]
    depoimentos = Depoimento.objects.all().order_by('-id')[:3]
    return render(request, 'core/index.html', {
        'oportunidades': oportunidades,
        'depoimentos': depoimentos,
    })


def listar_ongs(request):
    ongs = Perfil.objects.filter(tipo='ONG').select_related('user')
    return render(request, 'core/ongs.html', {'ongs': ongs})


def historias(request):
    depoimentos = Depoimento.objects.all().order_by('-id')
    form = None

    if request.user.is_authenticated and hasattr(request.user, 'perfil') and request.user.perfil.tipo == 'VOLUNTARIO':
        if request.method == 'POST':
            form = DepoimentoForm(request.POST)
            if form.is_valid():
                depoimento = form.save(commit=False)
                depoimento.nome = request.user.get_full_name() or request.user.username
                
                # ATRIBUI A FOTO DO PERFIL AUTOMATICAMENTE
                perfil = request.user.perfil
                if perfil.foto:
                    # Se o modelo Depoimento usa foto_url (campo texto/URL)
                    depoimento.foto_url = perfil.foto.url
                    
                    # NOTA: Caso o modelo Depoimento use ImageField chamado 'foto', 
                    # use a linha abaixo em vez de foto_url:
                    # depoimento.foto = perfil.foto

                depoimento.save()
                messages.success(request, "Sua história foi publicada com sucesso!")
                return redirect('historias')
        else:
            form = DepoimentoForm()

    return render(request, 'core/historias.html', {
        'depoimentos': depoimentos,
        'form': form
    })


def listar_oportunidades(request):
    oportunidades = Oportunidade.objects.filter(ativa=True).select_related('ong').order_by('-data_criacao')
    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    return render(request, 'core/oportunidades.html', {
        'oportunidades': oportunidades,
        'google_maps_api_key': google_maps_api_key
    })


# ==========================================
# AUTENTICAÇÃO E PERFIL
# ==========================================

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
        form = CadastroONGForm(request.POST, request.FILES)
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
                foto=request.FILES.get('foto'),
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
def editar_perfil_ong(request):
    perfil = get_object_or_404(Perfil, user=request.user, tipo='ONG')

    if request.method == 'POST':
        form = CadastroONGForm(request.POST, request.FILES, instance=request.user)
        form.fields['password'].required = False
        if 'confirm_password' in form.fields:
            form.fields['confirm_password'].required = False

        if form.is_valid():
            user = form.save(commit=False)
            nova_senha = form.cleaned_data.get('password')
            if nova_senha:
                user.set_password(nova_senha)
            user.save()

            perfil.telefone = form.cleaned_data.get('telefone', perfil.telefone)
            perfil.cidade = form.cleaned_data.get('cidade', perfil.cidade)
            perfil.mensagem = form.cleaned_data.get('mensagem', perfil.mensagem)
            
            if request.FILES.get('foto'):
                perfil.foto = request.FILES['foto']
                
            perfil.save()

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('listar_ongs')
    else:
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
def editar_perfil_voluntario(request):
    perfil = get_object_or_404(Perfil, user=request.user, tipo='VOLUNTARIO')

    if request.method == 'POST':
        form = CadastroVoluntarioForm(request.POST, request.FILES, instance=request.user)
        form.fields['password'].required = False
        if 'confirm_password' in form.fields:
            form.fields['confirm_password'].required = False

        if form.is_valid():
            user = form.save(commit=False)
            nova_senha = form.cleaned_data.get('password')
            if nova_senha:
                user.set_password(nova_senha)
            user.save()

            perfil.telefone = form.cleaned_data.get('telefone', perfil.telefone)
            perfil.cidade = form.cleaned_data.get('cidade', perfil.cidade)
            perfil.habilidades = form.cleaned_data.get('habilidades', perfil.habilidades)
            
            if request.FILES.get('foto'):
                perfil.foto = request.FILES['foto']
                
            perfil.save()

            messages.success(request, "Seu perfil foi atualizado com sucesso!")
            return redirect('home')
    else:
        dados_iniciais = {
            'telefone': perfil.telefone,
            'cidade': perfil.cidade,
            'habilidades': perfil.habilidades,
        }
        form = CadastroVoluntarioForm(instance=request.user, initial=dados_iniciais)
        form.fields['password'].required = False
        if 'confirm_password' in form.fields:
            form.fields['confirm_password'].required = False

    return render(request, 'core/editar_perfil_voluntario.html', {'form': form})

# ==========================================
# GESTÃO DE OPORTUNIDADES & INSCRIÇÕES
# ==========================================

@login_required
def criar_oportunidade(request):
    # Verifica se existe perfil e se o tipo é ONG (ignorando maiúsculas/minúsculas)
    perfil = getattr(request.user, 'perfil', None)
    
    if not perfil or str(perfil.tipo).upper() != 'ONG':
        messages.error(request, "Apenas Organizações/ONGs podem cadastrar novas oportunidades.")
        return redirect('listar_oportunidades')

    if request.method == 'POST':
        form = OportunidadeForm(request.POST)
        if form.is_valid():
            oportunidade = form.save(commit=False)
            oportunidade.ong = request.user
            oportunidade.save()
            messages.success(request, "Oportunidade cadastrada com sucesso!")
            return redirect('listar_oportunidades')
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

        # Notificação por E-mail para a ONG
        if vaga.ong.email:
            try:
                send_mail(
                    subject=f"Novo Voluntário Inscrito: {vaga.titulo}",
                    message=(
                        f"Olá, {vaga.ong.username}!\n\n"
                        f"O voluntário {request.user.get_full_name() or request.user.username} "
                        f"inscreveu-se na oportunidade '{vaga.titulo}'.\n\n"
                        f"Contato do voluntário: {request.user.email}\n"
                    ),
                    from_email=None,
                    recipient_list=[vaga.ong.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erro no envio de e-mail: {e}")

    return redirect('listar_oportunidades')


@login_required
def minhas_oportunidades(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'ONG':
        messages.error(request, "Apenas ONGs têm acesso a esta página.")
        return redirect('home')

    minhas_vagas = Oportunidade.objects.filter(ong=request.user).prefetch_related('inscritos__perfil').order_by('-data_criacao')
    return render(request, 'core/minhas_oportunidades.html', {'vagas': minhas_vagas})


# ==========================================
# APIs ENDPOINTS (JSON)
# ==========================================

def api_oportunidades_mapa(request):
    oportunidades = Oportunidade.objects.filter(ativa=True, latitude__isnull=False, longitude__isnull=False)
    dados = [
        {
            'id': vaga.id,
            'titulo': vaga.titulo,
            'local': vaga.local,
            'lat': float(vaga.latitude),
            'lng': float(vaga.longitude),
        }
        for vaga in oportunidades
    ]
    return JsonResponse(dados, safe=False)

@login_required
def editar_oportunidade(request, vaga_id):
    # Garante que apenas a ONG dona da vaga pode editá-la
    vaga = get_object_or_404(Oportunidade, id=vaga_id, ong=request.user)

    if request.method == 'POST':
        form = OportunidadeForm(request.POST, instance=vaga)
        if form.is_valid():
            oportunidade = form.save(commit=False)
            # Limpa as coordenadas antigas para forçar o geopy a buscar o novo endereço
            oportunidade.latitude = None
            oportunidade.longitude = None
            oportunidade.save()
            messages.success(request, "Oportunidade atualizada com sucesso!")
            return redirect('minhas_oportunidades')
    else:
        form = OportunidadeForm(instance=vaga)

    return render(request, 'core/criar_oportunidade.html', {
        'form': form,
        'editando': True
    })


@login_required
def deletar_oportunidade(request, vaga_id):
    # Garante que apenas a ONG dona da vaga pode deletá-la
    vaga = get_object_or_404(Oportunidade, id=vaga_id, ong=request.user)
    
    if request.method == 'POST':
        vaga.delete()
        messages.success(request, "Oportunidade removida com sucesso!")
        return redirect('minhas_oportunidades')
        
    return render(request, 'core/confirmar_deletar.html', {'vaga': vaga})