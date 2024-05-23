from django.db import models

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

 