from django.shortcuts import render

# Create your views here.


def home(request):
    print('Método da Requisição: ', request.method)
    print('Caminho: ', request.path)
    return render(request, 'base.html', {})