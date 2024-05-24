from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from . models import Cliente

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Logs, HookWhatsapp

logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
    clientes = Cliente.objects.all()
    context = {
        'clientes': clientes
    }
    
    return render(request, 'core/index.html', context)


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
            # c1.save()
            
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

@csrf_exempt
def webhook_verify(request):
    mode = request.GET.get('hub.mode')
    token = request.GET.get('hub.verify_token')
    challenge = request.GET.get('hub.challenge')

    if mode == 'subscribe' and token == WEBHOOK_VERIFY_TOKEN:
        return HttpResponse(challenge, status=200)
    else:
        return HttpResponse(status=403)
    

def create_result_object(entry):
    entity_id = entry.get('id')
    changes = entry.get('changes', [{}])[0].get('value', {})
    
    message_data = changes.get('messages', [{}])[0]
    statuses_data = changes.get('statuses', [{}])[0]
    
    message_id = statuses_data.get('id', message_data.get('id'))
    status = statuses_data.get('status')
    timestamp = statuses_data.get('timestamp', message_data.get('timestamp'))
    recipient_id = statuses_data.get('recipient_id')
    text = message_data.get('text', {}).get('body')
    
    contact_data = changes.get('contacts', [{}])[0]
    profile_name = contact_data.get('profile', {}).get('name')
    wa_id = contact_data.get('wa_id')
    
    timestamp = datetime.fromtimestamp(int(timestamp)) if timestamp else datetime.now()

    return {
        'entity_id': entity_id,
        'message_id': message_id,
        'timestamp': timestamp,
        'profile_name': profile_name,
        'wa_id': wa_id,
        'status': status,
        'message_text': text,
        'recipient_id': recipient_id,
    }

            
    
    
@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            if body:
                Logs.objects.create(log=json.dumps(body))

                entry = body.get('entry', [{}])[0]
                if not entry or not entry.get('changes'):
                    return JsonResponse({'erro': 'Entrada inválida'}, status=400)

                result = create_result_object(entry)
                HookWhatsapp.objects.create(**result)
                return JsonResponse({'resp': 'Dados armazenados com sucesso'})
            else:
                return JsonResponse({'erro': 'Corpo da requisição vazio'}, status=400)
        except Exception as error:
            logger.error(f"Error during the webhook: {error}")
            return JsonResponse({'erro': 'Não foi possível salvar JSON'}, status=500)
    return JsonResponse({'erro': 'Método não permitido'}, status=405)
    