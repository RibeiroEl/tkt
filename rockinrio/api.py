from django.db import IntegrityError
from .rio import *
from .models import Cliente
from ninja.errors import HttpError
from ninja import NinjaAPI
from .schemas import ClienteCreate
from datetime import timedelta
from django.utils import timezone

api = NinjaAPI(docs_url=None)
rio = RockValid()

@api.post("/client")
def cliente(request, data: ClienteCreate):
    try:
        email = data.email.lower()
        nome = data.nome
        rio.valid(email)
        telefone = rio.telefone(data.telefone)
        score = rio.score(email)
        if score is True or score is None:
            Cliente.objects.create(nome=nome, email=email, telefone=telefone)
            hash = rio.encrypt(email)
            rio.sender(email, nome, hash)
        return 200
    except InvalidEmail:
        raise HttpError(400, "Invalid e-mail")
    except InvalidPhone:
        raise HttpError(400, "Invalid phone")
    except IntegrityError:
        raise HttpError(410, "User exist")
    except Exception as e:
        print(e)
        raise HttpError(500, "Error undefined")

@api.get("/email/{email}")
def email(request, email: str):
    try:
        rio.valid(email)
        cliente = Cliente.objects.get(email=email)
        hash = rio.encrypt(email)

        current_time = timezone.now()
        if cliente.last_email_sent and current_time - cliente.last_email_sent < timedelta(minutes=2):
            raise HttpError(403, "Operation not unsuccessful")
        
        rio.sender(email, cliente.nome, hash)
        cliente.last_email_sent = current_time
        cliente.save()
        return 200
        
    except Cliente.DoesNotExist: 
        raise HttpError(403, "Operation not unsuccessful")
    except InvalidEmail:
        raise HttpError(500, "Invalid e-mail")
    except EmailError:
        raise HttpError(500, "API error")

# Nova rota adicionada para formulário do front-end
from .schemas import ClienteCreate, FormularioSchema  # <--- import aqui!

@api.post("/submit-form/")
def submit_form(request, data: FormularioSchema):
    try:
        nome = data.name
        email = data.email.lower()
        telefone = data.phone

        rio.valid(email)
        telefone_validado = rio.telefone(telefone)
        score = rio.score(email)

        if score is True or score is None:
            Cliente.objects.create(nome=nome, email=email, telefone=telefone_validado)
            hash = rio.encrypt(email)
            rio.sender(email, nome, hash)

        return {"success": True}

    except InvalidEmail:
        raise HttpError(400, "Invalid e-mail")
    except InvalidPhone:
        raise HttpError(400, "Invalid phone")
    except IntegrityError:
        raise HttpError(410, "User already exists")
    except Exception as e:
        print(e)
        raise HttpError(500, "Undefined error")
