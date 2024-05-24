from django.db import models
from django.utils import timezone

# Create your models here.

#Exemplo
#{'nome': 'Neela', 'email': 'Murali2014@yahoo.edu', 'status': 'recusado', 'valor': 650, 'forma_pagamento': 'pix', 'parcelas': 2}

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    status = models.CharField(max_length=100)
    valor = models.CharField(max_length=100)
    forma_pagamento = models.CharField(max_length=100)
    parcelas = models.IntegerField()
    
    def __str__(self):
        return self.nome
    
    
class Logs(models.Model):
    log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class HookWhatsapp(models.Model):
    entity_id = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    profile_name = models.CharField(max_length=255, null=True)
    wa_id = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50, null=True)
    message_text = models.TextField(null=True)
    recipient_id = models.CharField(max_length=255, null=True)
    

 