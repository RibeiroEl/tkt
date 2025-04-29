from django.db import models

class Cliente(models.Model):
    class StatusEmail(models.TextChoices):
        PENDENTE = 'PE', 'Pendente'
        CONFIRMADO = 'OK', 'Confirmado'
    
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    last_email_sent = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, default=StatusEmail.PENDENTE, choices=StatusEmail.choices)

    def __str__(self):
        return self.email
    
class Codigo(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=255)
    header = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.host