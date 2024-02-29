from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import password_is_valid, email_html
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages, auth
import os
from django.conf import settings
from .models import Ativacao
from hashlib import sha256


def cadastro(request):
    # Se o método da requisição for GET
    if request.method == "GET":
        # Se o usuário já estiver autenticado
        if request.user.is_authenticated:
            # Redireciona para a página inicial
            return redirect('/')
        # Renderiza a página de cadastro
        return render(request, 'cadastro.html')  

    # Se o método da requisição for POST
    elif request.method == "POST":
        # Obtém os dados do formulário
        username = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Verifica se a senha é válida
        if not password_is_valid(request, senha, confirmar_senha):
            # Se não for, redireciona para a página de cadastro
            return redirect('/auth/cadastro')  

        # Tenta criar um novo usuário
        try:
            # Cria um novo usuário com os dados do formulário
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=senha,
                                            is_active=False)  
            # Salva o usuário no banco de dados
            user.save()  
            
            # Gera um token de ativação
            token = sha256(f"{username}{email}".encode()).hexdigest()
            # Cria um novo registro de ativação com o token e o usuário
            ativacao = Ativacao(token=token, user=user)
            # Salva o registro de ativação no banco de dados
            ativacao.save()
            
            # Define o caminho para o template do email de confirmação de cadastro
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            
            # Envia o email de confirmação de cadastro
            email_html(path_template, 'Cadastro confirmado', [email,], username=username)
             
            # Adiciona uma mensagem de sucesso
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')
            # Redireciona para a página de login
            return redirect('/auth/logar')  

        # Se ocorrer algum erro
        except:  
            # Adiciona uma mensagem de erro
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            # Redireciona para a página de cadastro
            return redirect('/auth/cadastro')



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