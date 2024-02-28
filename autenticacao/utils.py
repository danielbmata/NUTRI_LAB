import re
from django.contrib import messages
from django.contrib.messages import constants

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