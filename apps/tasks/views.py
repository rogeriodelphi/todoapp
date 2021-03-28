from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import CategoryForm, TaskForm
from .models import Category, Task

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
    #Se o método for get, renderiza o formulário em branco
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

    #Filtar por id e usuário
    category = get_object_or_404(Category, id=id_category, user=request.user)
    #Verificada se o método é 'post' ou 'get'
    if request.method == 'POST':
        #Pega os dados que estão vindo no formulário
        form = CategoryForm(request.POST, instance=category)
        #verifica se está com os dados validados
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
            #salvar many to many
            form.save_m2m()
            messages.success(request, 'Tarefa salva com sucesso.')
        else:
            print(form.errors)
    #Se o método for get, renderiza o formulário em branco
    form = TaskForm()
    context['form'] = form
    return render(request, template_name, context)

@login_required(login_url='/contas/login/')
def list_tasks(request):
    template_name = 'tasks/list_tasks.html'
    tasks = Task.objects.filter(user=request.user).exclude(status='CD')
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def edit_task(request, id_task):
    template_name = 'tasks/add_task.html'
    context = {}

    #Filtar por id e usuário
    task = get_object_or_404(Task, id=id_task, user=request.user)
    #Verificada se o método é 'post' ou 'get'
    if request.method == 'POST':
        #Pega os dados que estão vindo no formulário
        form = TaskForm(request.POST, instance=task)
        #verifica se está com os dados validados
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
    #se o dono setado nessa tarefa recuperada é o mesmo que tem logado na função
    if task.user == request.user:
        #Pode deletar, pois ele é o dono da tarefa
        task.delete()
    else:
        messages.error(request, 'Você não tem permissão para excluir esta tarefa.')
        return redirect('core:home')
    return redirect('tasks:list_tasks')
