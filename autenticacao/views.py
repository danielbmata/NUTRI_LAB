from django.shortcuts import render
from django.http import HttpResponse

def cadastro(request):

    if request.method == "GET":
        return render(request, 'cadastro.html')
    
    elif request.method == "POST":
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        return HttpResponse(f'{usuario} e {email}')


def logar(request):
    return render(request, 'logar.html')
