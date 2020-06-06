from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import CategoryForm, TaskForm
from .models import Category, Task

def add_category(request):
    template_name = 'tasks/add_category.html'
    context = {}
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            messages.success(request, 'Categoria salva com sucesso.')
    #Se o método for get, renderiza o formulário em branco
    form = CategoryForm()
    context['form'] = form
    return render(request, template_name, context)


def list_categories(request):
    template_name = 'tasks/list_categories.html'
    categories = Category.objects.filter(owner=request.user)
    context = {
        'categories': categories
    }
    return render(request, template_name, context)


def edit_category(request, id_category):
    template_name = 'tasks/add_category.html'
    context = {}

    #Filtar por id e usuário
    category = get_object_or_404(Category, id=id_category, owner=request.user)
    #Verificada se o método é 'post' ou 'get'
    if request.method == 'POST':
        #Pega os dados que estão vindo no formulário
        form = CategoryForm(request.POST, instance=category)
        #verifica se está com os dados validados
        if form.is_valid():
            form.save()
            messages.info(request, 'Os dados foram atualiados com sucesso.')
            return redirect('category:list_categories')
    form = CategoryForm(instance=category)
    context['form'] = form
    return render(request, template_name, context)


def delete_category(request, id_category):
    category = Category.objects.get(id=id_category)
    if category.owner == request.user:
        category.delete()
    else:
        messages.error(request, 'Você não tem permissão para excluir essa categoria.')
        return redirect('core:home')
    return redirect('category:list_categories')


def add_task(request):
    template_name = 'tasks/add_task.html'
    context = {}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
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

def list_tasks(request):
    template_name = 'tasks/list_tasks.html'
    tasks = Task.objects.filter(owner=request.user).exclude(status='CD')
    context = {
        'tasks': tasks
    }
    return render(request, template_name, context)


def edit_task(request, id_task):
    template_name = 'tasks/add_task.html'
    context = {}

    #Filtar por id e usuário
    task = get_object_or_404(Task, id=id_task, owner=request.user)
    #Verificada se o método é 'post' ou 'get'
    if request.method == 'POST':
        #Pega os dados que estão vindo no formulário
        form = TaskForm(request.POST, instance=task)
        #verifica se está com os dados validados
        if form.is_valid():
            form.save()
            messages.info(request, 'Os dados foram atualiados com sucesso.')
            return redirect('tasks:list_tasks')
    form = TaskForm(instance=task)
    context['form'] = form
    return render(request, template_name, context)
