from datetime import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.tasks.models import Task

today = datetime.now()
start_time = today - timedelta(days=today.isoweekday())
end_time = start_time + timedelta(days=6)
num_week =  datetime.date(today).isocalendar()[1]


@login_required(login_url='/contas/login/')
def home(request):
    today = datetime.now().strftime("%V")
    template_name = 'core/home.html'
    # traz todas as tarefada semana
    # viagens_no_mes = Viagem.objects.filter(data__month=datetime.date.today().month, data__year=datetime.date.today().year).count()
    tasks = Task.objects.filter(end_time__range=(start_time, end_time), user=request.user)
    #    tasks = Task.objects.filter(end_time=datetime.today()).exclude(status='CO')
    #    tasks = Task.objects.filter(end_time__month=now)
    context = {
        'tasks': tasks,
        'today': today,
        'num_week': num_week,
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def search_tasks(request):
    template_name = 'core/search_tasks.html'
    query = request.GET.get('query')
    tasks = Task.objects.filter(title__icontains=query, user=request.user).exclude(status='CO')
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def search_busca_datas(request):
    template_name = 'core/search_busca_datas.html'
    # new_format = datetime.datetime.strptime("%Y-%m-%d")
    datainicial = request.GET.get('busca_datainicial')
    datafinal = request.GET.get('busca_datafinal')
    datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime("%Y-%m-%d")
    #    tasks = Task.objects.filter(end_time=search_busca_datainicial)
    tasks = Task.objects.filter(end_time__range=(datainicial, datafinal), user=request.user)
    context = {
        'tasks': tasks
    }
    #    print(request.GET.get('busca_datainicial'))
    return render(request, template_name, context)
