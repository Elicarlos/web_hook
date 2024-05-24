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
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            nome = data.get('nome')
            email = data.get('email')
            status = data.get('status')
            valor = data.get('valor')
            forma_pagamento = data.get('forma_pagamento')
            parcelas = data.get('parcelas')
            
            # Criação do cliente
            c1 = Cliente(
                nome=nome, 
                email=email, 
                status=status, 
                valor=valor, 
                forma_pagamento=forma_pagamento, 
                parcelas=parcelas
            )
            c1.save()
            
            # Obtenção do cliente
            cliente = Cliente.objects.get(email=email)
            dados = {
                "nome": cliente.nome, 
                "email": cliente.email,  
                "status": cliente.status,  
                "valor": cliente.valor,
                "forma_pagamento": cliente.forma_pagamento,
                "parcelas": cliente.parcelas
            }
            dado = json.dumps(dados)
            
            link = "https://webhook.site/e035ba9f-7b42-4b57-a7f2-694e0a9a2f9c"
            
            # Envio dos dados como JSON
            headers = {'Content-Type': 'application/json'}
            requests.post(link, data=dado, headers=headers)
            
        except Exception as e:
            print(f"Erro: {e}")
            return HttpResponse("Erro no processamento dos dados", status=500)
        
    else:
        print(request.body)
    
    return HttpResponse("Sucesso")

 
 
# def webhook_whatsapp(request):
#     if request.method == "GET":
#         if request.args.get('hub.verify_token') == VERIFY_TOKEN:
#             return request.args.get('hub.challenge')
        
#         return "Authentication failed. invalid Tokem"
    
    
#     client = WhatsAppWrapper()
    
#     response = client.process_webhook_notification(request.get_json())
    
#     return jsonify("status": "success")


# def process_webhook_notification(self, data):
#     response  = []
    
    
#     for entry in data["entry"]:
#         for change in entry["changes"]:
#             response.append(
#                 {
#                     "type": change["field"],
#                     "from": change["value"]["metadata"]["display_phone_number"],
#                 }
#             )
            
#     return response


WEBHOOK_VERIFY_TOKEN = 'meutoken'

def webhook_verify(request):
    mode = request.GET.get('hub.mode')
    
    token = request.GET.get('hub.verify_token')
    
    challenge = request.GET.get('hub.chanllege')
    
    if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        return HttpResponse(challenge)
    
    else:
        return HttpResponse(status=403)
            
    
    
def webhook(request):
    pass
    
    