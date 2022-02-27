import json

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import UserForm, UserProfileForm, UserFormChangeInformation
from .models import UserProfile


def add_user(request):
    template_name = 'accounts/add_user.html'
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Para que possa passar a senha e fazer um hash dela
            f = form.save(commit=False)
            f.set_password(f.password)
            f.save()
            messages.success(request, "Usuário salvo com sucesso!")
            # return redirect('accounts:user_login')
    # se a requisição for do tipo GET, instancia o formulário 'form'
    form = UserForm()
    context['form'] = form
    return render(request, template_name, context)


def user_login(request):
    template_name = 'accounts/user_login.html'
    if request.method == 'POST':
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6LflD4ceAAAAACq6YQst3lTxAddXA3uutfui1tWY"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)

        if cap_json['success'] == False:
            messages.error(request, "Captcha inválido, tente novamente!")
            return HttpResponseRedirect("/")
        else:
            # print("cap_server_response: " + cap_server_response.text)
            # print("Captcha Token: " + captcha_token)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', '/'))
            else:
                messages.error(request, "Usuário ou senha inválidos")
    return render(request, template_name, {})


@login_required(login_url='/contas/login/')
def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


@login_required(login_url='/contas/login/')
def user_change_password(request):
    template_name = 'accounts/user_change_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso!')
            update_session_auth_hash(request, form.user)
        else:
            messages.error(request, 'Não foi possível trocar a suanha senha!')
    form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def add_user_profile(request):
    template_name = 'accounts/add_user_profile.html'
    context = {}
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            messages.success(request, 'Perfil alterado com sucesso!')
    form = UserProfileForm()
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def list_user_profile(request):
    template_name = 'accounts/list_user_profile.html'
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    context = {
        'profile': profile
    }
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def change_user_profile(request, username):
    template_name = 'accounts/add_user_profile.html'
    context = {}
    profile = UserProfile.objects.get(user__username=username)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
    form = UserProfileForm(instance=profile)
    context['form'] = form
    return render(request, template_name, context)


@login_required(login_url='/contas/login/')
def change_user_information(request, username):
    template_name = 'accounts/change_user_information.html'
    context = {}
    user = User.objects.get(username=username)
    if request.method == 'POST':
        form = UserFormChangeInformation(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas com sucesso.")
    form = UserFormChangeInformation(instance=user)
    context['form'] = form
    return render(request, template_name, context)
