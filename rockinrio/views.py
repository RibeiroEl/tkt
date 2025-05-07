from django.shortcuts import render, redirect
from .models import Codigo
from .rio import *
from django.http import JsonResponse
import json

def index(request):
    """Página inicial com o formulário de cadastro"""
    if request.session.get("verify"):
        return redirect("landing")
    
    # Obter códigos personalizados para o host
    host = request.META.get("HTTP_HOST", "404")
    hcode = "<script></script>"
    bcode = "<script></script>"
    try:
        objeto = Codigo.objects.get(host=host)
        hcode = objeto.header
        bcode = objeto.body
    except:
        pass
    
    return render(request, "index.html", {"hcode": hcode, "bcode": bcode})

def landing(request):
    """Página após alguma verificação inicial (mantido conforme original)"""
    request.session["verify"] = True
    
    host = request.META.get("HTTP_HOST", "404")
    hcode = "<script></script>"
    bcode = "<script></script>"
    try:
        objeto = Codigo.objects.get(host=host)
        hcode = objeto.header
        bcode = objeto.body
    except:
        pass
    return render(request, "index.html", {"hcode": hcode, "bcode": bcode})

def form_submit(request):
    """Processa submissão do formulário via AJAX e retorna JSON"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email').lower()
            phone = data.get('phone')
            
            # Validar dados usando RockValid
            rio = RockValid()
            rio.valid(email)
            telefone = rio.telefone(phone)
            score = rio.score(email)
            
            if score is True or score is None:
                from .models import Cliente
                # Verifica se o cliente já existe
                try:
                    cliente = Cliente.objects.get(email=email)
                    return JsonResponse({'success': False, 'message': 'Email já cadastrado'}, status=410)
                except Cliente.DoesNotExist:
                    # Cria novo cliente
                    Cliente.objects.create(nome=name, email=email, telefone=telefone)
                    hash_confirmacao = rio.encrypt(email) # Renomeei para clareza
                    rio.sender(email, name, hash_confirmacao)
                    return JsonResponse({'success': True, 'message': 'Cadastro realizado com sucesso! Por favor, verifique seu e-mail para confirmação.'})
            else:
                return JsonResponse({'success': False, 'message': 'Email com baixa reputação'}, status=400)
                
        except InvalidEmail:
            return JsonResponse({'success': False, 'message': 'Email inválido'}, status=400)
        except InvalidPhone:
            return JsonResponse({'success': False, 'message': 'Telefone inválido'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': 'Erro ao processar solicitação'}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método não permitido'}, status=405)

def verify(request, hash):
    """Verificação do link de email"""
    rio = RockValid()
    result = rio.decrypt(hash)
    if result:
        request.session["confirmed"] = True
        return redirect("sucesso")
    return render(request, "verificacao_invalida.html")  # Mostra página de link inválido em vez de redirecionar

def sucesso(request):
    """Página de confirmação bem-sucedida"""
    if request.session.get("confirmed"):
        return render(request, "sucesso.html")
    return redirect("index")

def envio_email_confirmation(request):
    """Página mostrada após o envio do formulário"""
    return render(request, 'envio_email_confirmation.html')

def confirmed_email(request):
    """Página de email confirmado (redundante com sucesso, mas mantida para compatibilidade)"""
    if request.session.get("confirmed"):
        return render(request, 'confirmed_email.html')
    return redirect("index")