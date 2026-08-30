# pylint: disable=missing-module-docstring, missing-function-docstring
from django.shortcuts import render
from .models import Oportunidade, Depoimento

def home(request):
    # pylint: disable=no-member
    oportunidades = Oportunidade.objects.filter(ativa=True).order_by('-data_criacao')
    depoimentos = Depoimento.objects.all()[:3]

    context = {
        'oportunidades': oportunidades,
        'depoimentos': depoimentos,
    }
    return render(request, 'core/index.html', context)
