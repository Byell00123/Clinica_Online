# Clinica_Online/src/healing/usuarios/views.py
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def home(request): # http://127.0.0.1:8000/

    if request.method == "GET":
        return render(request, 'home_projeto.html')
    
    elif request.method == "POST":
        return render(request, 'home_projeto.html')

def cadastro(request): # http://127.0.0.1:8000/usuarios/cadastro/
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        primeiro_nome = request.POST.get('primeiro_nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        compara_usuarios = User.objects.filter(email=email) # Exibe --> <QuerySet []> <-- E Retorna True(se tiver algo no colchetes) ou False(se não tiver algo no colchetes),
        # e True significa que esse valor de email ja exite no Banco de Dados e False significa que esse valor de email não exite no Banco de Dados logo podendo ser utilizado.

        if compara_usuarios.exists():  # Se email == True, não permite criar o usuario pois ja existe alguem com aquele email
            messages.add_message(request,constants.ERROR, "Este email já está em uso. Por favor, escolha outro.")
            return redirect('/usuarios/cadastro/')

        if senha != confirmar_senha:
            messages.add_message(request,constants.WARNING, "As senhas não correspondem. Por favor, verifique e tente novamente.")
            return redirect('/usuarios/cadastro/')

        if len(senha) < 8 or valida_senha(request): #Se a senha tiver menos que 8 digitos ou a Senha for True(se não tiver caracters especiais + 0-9 + A-Z + a-z), 
            messages.add_message(request, constants.WARNING, "A senha precisa ter pelo menos 8 caracteres e incluir pelo menos um dos seguintes caracteres especiais: *, @, -, _. Além disso, a senha deve conter pelo menos um número, uma letra maiúscula e uma letra minúscula.")
            return redirect('/usuarios/cadastro/')

        try:
            cria_usuario = User.objects.create_user(first_name=primeiro_nome, last_name=sobrenome, username=email, email=email, password=senha, is_active=True)
            messages.add_message(request,constants.INFO, "A primeira etapa do cadastro foi realizada com sucesso. Agora faça login para prosseguir.")
            return redirect('/usuarios/login/')
        except:
            messages.add_message(request,constants.ERROR, "Algo inesperado aconteceu durante a realização do seu cadastro. Por favor, tente novamente.")
            return redirect('/usuarios/login/')

def login(request): # http://127.0.0.1:8000/usuarios/login/
    if request.method == "GET":
        return render(request,'login.html')
    
    elif request.method == "POST":
        nome_de_usuario = request.POST.get('email')
        senha = request.POST.get('senha')

        valida_usuario = auth.authenticate(request, username=nome_de_usuario, password=senha) #Retorna True(se tiver usuario cadatrado com essas dados) ou False(se não tiver usuario 
# cadatrado com essas dados). True significa que esse valor de email ja exite no Banco de Dados e False significa que esse valor de email não exite no Banco de Dados 
# logo podendo ser utilizado.

        if valida_usuario: # Se valida_usuario == True, o usuario ja existe e sera feito o login
            auth.login(request, valida_usuario)
            if not User.is_active: #TODO: Devido a forma que está sendo feito o cadastro todos os usuarios são ativados.
                messages.info(request, "Usuário desativado.")

            messages.info(request, "Você completou primeira etapa do cadastro! Agora é só ativar sua conta adicionando mais alguns detalhes. Fique atento ao seu e-mail para as próximas instruções.")
            return redirect('/pacientes/home/')
            
        messages.add_message(request, constants.ERROR, "Nome de Usuario e/ou Senha incorreto(s).")
        return redirect('/usuarios/login/')

#@login_required
def sair(request): # http://127.0.0.1:8000/usuarios/sair/
    if request.user.is_authenticated:
        messages.add_message(request, constants.SUCCESS, "Logout realizado com sucesso. Volte sempre..")
    else:
        messages.add_message(request, constants.WARNING, "Essa ação não é necessária, você não está logado.")
    auth.logout(request)
    return redirect('/usuarios/login/')

def valida_senha(request):
    #TODO: Depois trazer o o ` elif senha != confirmar_senha: ´ para essa função.
    senha = request.POST.get('senha')
    caracteresp = 0
    letrasmai = 0
    letrasmin = 0
    numero = 0
    
    for i in senha:
        if i == "*" or i == "@" or i == "-" or i == "_":
            caracteresp += 1
        elif i.isupper(): # isupper() == letras maiúsculas.
            letrasmai += 1
        elif i.islower(): # islower() == letras minúsculas.
            letrasmin += 1
        elif i.isdigit(): # isdigit() == numeros de 0 a 9
            numero += 1
            
    if caracteresp < 1 or letrasmai < 1 or letrasmin < 1 or numero < 1:
        return True # É Verdadeiro o afirmação de que a senha é ruim. Ou tente entender como: é Verdadeiro que senha reprovou em algo
    else:
        return False # É Falso o afirmação de que a senha é ruim. Ou tente entender como: é Falso que senha reprovou em algo