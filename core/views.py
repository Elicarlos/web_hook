from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

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
        print(request.body)
        return HttpResponse("Sucesso")

    
    
    
    