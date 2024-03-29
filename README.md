[![Python Version](https://img.shields.io/badge/python-3.7.5-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.2.12-brightgreen.svg)](https://djangoproject.com)
[![Updates](https://pyup.io/repos/github/rogeriodelphi/todoapp/shield.svg)](https://pyup.io/repos/github/rogeriodelphi/todoapp/)
[![Python 3](https://pyup.io/repos/github/rogeriodelphi/todoapp/python-3-shield.svg)](https://pyup.io/repos/github/rogeriodelphi/todoapp/)
[![codecov](https://codecov.io/gh/rogeriodelphi/todoapp/branch/master/graph/badge.svg)](https://codecov.io/gh/rogeriodelphi/todoapp)

# ToDoAPP
```bash
*Sistema de Gestão de Tarefas*  
Projeto desenvolvido em _Python_ no _Windows_, testado no GNU/_Linux_ e _Windows_.  
```
Implementações
* Cadastro de categorias e tarefas, ...
* Login/Logout;
* Criação de perfil para cada usuário;
* Definição de permissões para usuários;
* Autenticação no Django com Python Social Auth;
* Autenticação utizando o Google Recaptcha;  

## Rodando o projeto localmente

Primeiramente, realize a clonagem do repositório para o seu computador:

```bash
https://github.com/rogeriodelphi/todoapp.git
```

Instale os requerimentos:

```bash
pip install -r requirements.txt
```

Rode as migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

Finalmente, rode o servidor de desenvolvimento:

```bash
python manage.py runserver
```

O projeto estará disponível em **127.0.0.1:8000**.