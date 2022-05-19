from datetime import datetime, date
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.urls import reverse_lazy

from django.views import generic
from django.utils.safestring import mark_safe
from datetime import timedelta
import calendar
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CategoryForm, TaskForm, AddMemberForm
from .models import Category, Task, TaskMember
from .utils import Calendar


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required(login_url='/contas/login/')
def add_category(request):
    template_name = 'tasks/add_category.html'
    context = {}
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            messages.success(request, 'Categoria salva com sucesso.')
            return redirect('tasks:list_categories')
    # Se o método for get, renderiza o formulário em branco
    form = CategoryForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_categories(request):
    template_name = 'tasks/list_categories.html'
    categories = Category.objects.filter(user=request.user)
    context = {
        'categories': categories
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_category(request, id_category):
    template_name = 'tasks/add_category.html'
    context = {}

    # Filtar por id e usuário
    category = get_object_or_404(Category, id=id_category, user=request.user)
    # Verificada se o método é 'post' ou 'get'
    if request.method == 'POST':
        # Pega os dados que estão vindo no formulário
        form = CategoryForm(request.POST, instance=category)
        # verifica se está com os dados validados
        if form.is_valid():
            form.save()
            messages.info(request, 'Os dados foram atualiados com sucesso.')
            return redirect('tasks:list_categories')
    form = CategoryForm(instance=category)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def delete_category(request, id_category):
    category = Category.objects.get(id=id_category)
    if category.user == request.user:
        category.delete()
    else:
        messages.error(request, 'Você não tem permissão para excluir esta categoria.')
        return redirect('core:home')
    return redirect('tasks:list_categories')


@login_required(login_url='/contas/login/')
def add_task(request):
    template_name = 'tasks/add_task.html'
    context = {}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            # salvar many to many
            form.save_m2m()
            messages.success(request, 'Tarefa salva com sucesso.')
            return redirect('tasks:list_tasks')
        else:
            print(form.errors)
    # Se o método for get, renderiza o formulário em branco
    form = TaskForm()
    print(context)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_tasks(request):
    template_name = 'tasks/list_tasks.html'
    # Retorna todas as tarefas, com exceção das que estão concluídas
    # tasks = Task.objects.filter(user=request.user).exclude(status='CO')
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_task(request, id_task):
    template_name = 'tasks/add_task.html'
    context = {}

    # Filtar por id e usuário
    task = get_object_or_404(Task, id=id_task, user=request.user)
    # Verificada se o método é 'post' ou 'get'
    if request.method == 'POST':
        # Pega os dados que estão vindo no formulário
        form = TaskForm(request.POST, instance=task)
        # verifica se está com os dados validados
        if form.is_valid():
            form.save()
            messages.info(request, 'Os dados foram atualizados com sucesso.')
            return redirect('tasks:list_tasks')
    form = TaskForm(instance=task)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def task_delete(request, id_task):
    task = Task.objects.get(id=id_task)
    # se o dono setado nessa tarefa recuperada é o mesmo que tem logado na função
    if task.user == request.user:
        # Pode deletar, pois ele é o dono da tarefa
        task.delete()
    else:
        messages.error(request, 'Você não tem permissão para excluir esta tarefa.')
        return redirect('core:home')
    return redirect('tasks:list_tasks')


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = '/contas/login/'
    model = Task
    template_name = 'tasks/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


@login_required(login_url='/contas/login/')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    taskmember = TaskMember.objects.filter(task=task)
    context = {
        'task': task,
        'taskmember': taskmember
    }
    return render(request, 'tasks/task-details.html', context)


def add_taskmember(request, task_id):
    forms = AddMemberForm()
    if request.method == 'POST':
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = TaskMember.objects.filter(task=task_id)
            task = Task.objects.get(id=task_id)
            if member.count() <= 3:
                user = forms.cleaned_data['user']
                TaskMember.objects.create(
                    task=task,
                    user=user
                )
                return redirect('tasks:calendar')
            else:
                print('--------------Limite de usuários excedido!-----------------')
    context = {
        'form': forms
    }
    return render(request, 'tasks/add_member.html', context)


class TaskMemberDeleteView(generic.DeleteView):
    model = TaskMember
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks:calendar')