from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from . models import Cliente

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    return HttpResponse("Sucesso")


@csrf_exempt  # Adicione esta linha
def send_message(request):
    link = "http://127.0.0.1:8000/send_message/"
    dados = {
        'cliente': "Elicarlos Ferreira",
        'status': 'Ativo'
    }
    dados = json.dumps(dados)

    
    requests.post(link, data=dados)
    return HttpResponse('sucesso')


@csrf_exempt
def hook_receiver_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        nome = data.get('nome')
        email = data.get('email')
        status = data.get('status')
        valor = data.get('valor')
        forma_pagamento = data.get('forma_pagamento')
        parcelas = data.get('parcelas')
        
        
        Cliente.save(nome, email, status, valor, forma_pagamento, parcelas)
        cliente = Cliente.objects.get(email=email).first()
        dados = {
                "nome": cliente.nome, 
                "email": cliente.email,  
                "status": cliente.status,  
                "valor": cliente.valor,
                "forma_pagamento":  cliente.forma_pagamento,
                "parcelas": cliente.parcelas
        }
        dado = json.dumps(dados)
            
            
        link = "https://webhook.site/e035ba9f-7b42-4b57-a7f2-694e0a9a2f9c"
            
        requests.post(link, data=dado)     

        
    else:
        print(request.body)
    
    return HttpResponse("Sucesso")

    
    
    
    