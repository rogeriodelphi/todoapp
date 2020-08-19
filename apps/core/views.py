# import datetime
# initial_date = 28-06-2020
# new_format = datetime.datetime.strptime("%Y-%m-%d")


from datetime import datetime
import datetime

start_date= datetime.date(2020, 6, 23)
end_date = datetime.date(2020, 6, 24)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.tasks .models import Task

# Create your views here.

@login_required(login_url='/contas/login/')
def home(request):
    template_name = 'core/home.html'
    #traz todos do dia atual e que não esteja concluída
    tasks = Task.objects.filter(end_date__range=(start_date, end_date), owner=request.user).exclude(status='CD')
#    tasks = Task.objects.filter(end_date=datetime.today()).exclude(status='CD')
#    tasks = Task.objects.filter(end_date__month=now)
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def search_tasks(request):
    template_name = 'core/search_tasks.html'
    query = request.GET.get('query')
    tasks = Task.objects.filter(name__icontains=query, owner=request.user).exclude(status='CD')
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def search_busca_datas(request):
    template_name = 'core/search_busca_datas.html'
    # new_format = datetime.datetime.strptime("%Y-%m-%d")
    datainicial=request.GET.get('busca_datainicial')
    datafinal=request.GET.get('busca_datafinal')
    datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime("%Y-%m-%d")
#    tasks = Task.objects.filter(end_date=search_busca_datainicial)
    tasks = Task.objects.filter(end_date__range=(datainicial, datafinal), owner=request.user)
    context = {
        'tasks': tasks
    }
#    print(request.GET.get('busca_datainicial'))
    return render(request, template_name, context)