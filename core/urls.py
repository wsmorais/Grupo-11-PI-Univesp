# pylint: disable=missing-module-docstring
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]