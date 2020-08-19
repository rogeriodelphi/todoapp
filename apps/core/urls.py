from django.urls import path

app_name = 'core'

from . import views

urlpatterns = [
    path('buscar/', views.search_tasks, name='search_tasks'),
    path('busca/', views.search_busca_datas, name='search_busca_datas'),
    path('', views.home, name='home'),
]