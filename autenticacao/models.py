from django.db import models  # Importa o módulo de modelos do Django
from django.contrib.auth.models import User

# Define a classe Ativacao, que é um modelo do Django
class Ativacao(models.Model):
    token = models.CharField(max_length=64)  # Define um campo de caracteres para o token com um comprimento máximo de 64
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  # Define uma chave estrangeira para o usuário. Se o usuário for excluído, não faz nada
    ativo = models.BooleanField(default=False)  # Define um campo booleano para ativo, que por padrão é False
    
    # Define a representação em string do modelo
    def __str__(self):
        return self.user.username  # Retorna o nome de usuário do usuário associado
