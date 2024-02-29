from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import password_is_valid, email_html
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth
import os
from django.conf import settings



def cadastro(request):

    # Verifica se o método da requisição é GET (normalmente o usuário acessando a página)
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')  # Retorna o template 'cadastro.html'

    # Verifica se o método da requisição é POST (submissão do formulário de cadastro)
    elif request.method == "POST":
        username = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Chama a função de validação de senha
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')  # Redireciona de volta em caso de erro na senha

        # Tenta criar um novo usuário
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=senha,
                                            is_active=False)  # Usuário criado inativo inicialmente
            user.save()  # Salva o usuário no banco de dados
            
            # Define o caminho para o template do email de confirmação de cadastro
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            # Envia um email de confirmação de cadastro
            email_html(path_template, 'Cadastro confirmado', [email,], username=username)


            
            
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
            return redirect('/auth/logar')  # Redireciona para a página de login após sucesso

        except:  # Caso não seja possível criar o usuário (ex.: nome já existe)
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')  # Redireciona de volta para o cadastro


# Define a função logar, que lida com as requisições de login
def logar(request):  
    if request.method == "GET":  # Se a requisição for GET:
        if request.user.is_authenticated:  # Se o usuário já estiver autenticado:
            return redirect('/')  # Redireciona para a página inicial
        return render(request, 'logar.html')  # Renderiza a página de login
    
    elif request.method == "POST":  # Se a requisição for POST:
        username = request.POST.get('usuario')  # Obtém o nome de usuário do formulário
        senha = request.POST.get('senha')  # Obtém a senha do formulário
        usuario = auth.authenticate(username=username, password=senha)  # Autentica o usuário
        if not usuario:  # Se a autenticação falhar:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')  # Adiciona uma mensagem de erro
            return redirect('/auth/logar')  # Redireciona para a página de login
        else:  # Se a autenticação for bem-sucedida:
            auth.login(request, usuario)  # Faz login com o usuário
            
    return redirect('/')  # Redireciona para a página inicial


def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')