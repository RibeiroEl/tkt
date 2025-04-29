from cryptography.fernet import Fernet, InvalidToken
from django.template.loader import get_template
from django.conf import settings
from .models import Cliente
import requests
import re

fernet = Fernet(settings.KEY_MAIL)

class EmailError(Exception):
    def __init__(self, message="Problema ao enviar e-mail", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class InvalidEmail(Exception):
    def __init__(self, message="E-mail inválido", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class InvalidPhone(Exception):
    def __init__(self, message="Telefone inválido", *args, **kwargs):
        super().__init__(message, *args, **kwargs)

class RockValid:
    def valid(self, email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(re.fullmatch(regex, email)):
            return True
        raise InvalidEmail()

    def telefone(self, telefone):
        telefone = "".join([d for d in telefone if d.isdigit()])
        regex = re.compile(r'^(?:[1-9][1-9])9[6-9]\d{3}\d{4}$')
        match = regex.match(telefone)
        if match: return telefone
        raise InvalidPhone()
    
    def decrypt(self, hash):
        try:
            email = fernet.decrypt(hash).decode()
            try:
                cliente = Cliente.objects.get(email=email)
                if cliente.status == Cliente.StatusEmail.PENDENTE:
                    cliente.status = Cliente.StatusEmail.CONFIRMADO
                    cliente.save()
                    return True
                return None
            except Cliente.DoesNotExist:
                return None
        except InvalidToken:
            return None
        except ValueError:
            return None
        except Exception as e:
            return None

    def encrypt(self, email):
        return fernet.encrypt(bytes(email, "utf-8")).decode()

    def score(self, email):
        API_KEY_SCORE = settings.API_KEY_SCORE 
        for _ in range(2):
            try:
                response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY_SCORE}&email={email}")
                print(response.json(), response.status_code)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("deliverability") == "DELIVERABLE": 
                        return True
                    return False
            except:
                pass
        return None

    def sender(self, email, nome, hash):
        api_key = settings.MAIL_GUN
        domain = settings.DOMAIN_EMAIL

        link = f"{settings.DOMAIN_NAME}/verify/{hash}"
        design = get_template("email/validar.html")
        html = design.render({"nome": nome.title(), "link": link})

        for _ in range(3):
            try:
                response = requests.post(
                    f"https://api.mailgun.net/v3/{domain}/messages",
                    auth=("api", api_key),
                    data={"from": f'Rock in Rio <ticket@{domain}>',
                        "to": email,
                        "subject": "Você está a um passo do seu convite exclusivo",
                        "html": html})
                if response.status_code == 200: 
                    return True
            except:
                continue
        raise EmailError()