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