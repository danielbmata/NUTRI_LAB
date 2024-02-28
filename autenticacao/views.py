from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import password_is_valid  # Importando a função de validação de senha
from django.contrib.auth.models import User

def cadastro(request):

    # Verifica se o método da requisição é GET (normalmente o usuário acessando a página)
    if request.method == "GET":
        return render(request, 'cadastro.html')  # Retorna o template 'cadastro.html'

    # Verifica se o método da requisição é POST (submissão do formulário de cadastro)
    elif request.method == "POST":
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Chama a função de validação de senha
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')  # Redireciona de volta em caso de erro na senha

        # Tenta criar um novo usuário no Django
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=senha,
                                            is_active=False)  # Usuário criado inativo inicialmente
            user.save()  # Salva o usuário no banco de dados
            return redirect('/auth/logar')  # Redireciona para a página de login após sucesso

        except:  # Caso não seja possível criar o usuário (ex.: nome já existe)
            return redirect('/auth/cadastro')  # Redireciona de volta para o cadastro


        


def logar(request):
    return render(request, 'logar.html')
