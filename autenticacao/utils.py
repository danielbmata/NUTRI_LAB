import re  # Importa o módulo de expressões regulares do Python

from django.contrib import messages  # Importa o módulo de mensagens do Django, que permite exibir mensagens de uma requisição para outra

from django.contrib.messages import constants  # Importa o módulo de constantes do Django, que define níveis de mensagens como DEBUG, INFO, SUCCESS, WARNING e ERROR

from django.core.mail import EmailMultiAlternatives  # Importa a classe EmailMultiAlternatives do Django, que é usada para enviar emails com partes alternativas de texto e HTML

from django.template.loader import render_to_string  # Importa a função render_to_string do Django, que carrega um template e o renderiza com um contexto

from django.utils.html import strip_tags  # Importa a função strip_tags do Django, que remove todas as tags HTML de uma string

from django.conf import settings  # Importa o módulo de configurações do Django, que permite acessar as configurações do projeto Django onde está o email


# Função para verificar se a senha é válida
def password_is_valid(request, password, confirm_password):

    # Verifica se a senha tem pelo menos 6 caracteres
    if len(password) < 6:
        messages.add_message(request, constants.ERROR, 'Sua senha deve conter 6 ou mais caracteres')
        return False

    # Verifica se as senhas coincidem
    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem!')
        return False

    # Verifica se a senha contém letras maiúsculas
    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém letras maiúsculas')
        return False

    # Verifica se a senha contém letras minúsculas
    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém letras minúsculas')
        return False

    # Verifica se a senha contém números
    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, 'Sua senha não contém números')
        return False

    # Se todas as verificações forem positivas, retorna True
    return True


# Função para enviar emails
def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    # Renderiza o template HTML com os argumentos fornecidos
    html_content = render_to_string(path_template, kwargs)
    
    # Remove as tags HTML para criar uma versão em texto puro do conteúdo
    text_content = strip_tags(html_content)
    
    # Cria um email com alternativas, que inclui tanto a versão em texto puro quanto a versão HTML
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)
    
    # Anexa a versão HTML do email
    email.attach_alternative(html_content, "text/html")
    
    # Envia o email
    email.send()
    
    # Retorna um dicionário indicando que a operação foi bem-sucedida
    return {'status': 1}
