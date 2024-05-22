from django.http import HttpResponse
from django.shortcuts import render
import requests
import json

# Create your views here.

def home(request):
    return HttpResponse("Sucesso")



def send_message(request):
    link = "https://webhook.site/e035ba9f-7b42-4b57-a7f2-694e0a9a2f9c"
    dados = {
        'cliente': "Elicarlos Ferreira",
        'status': 'Ativo'
    }
    dados = json.dumps(dados)

    
    requests.post(link, data=dados)
    return HttpResponse('sucesso')
    
    
    
    