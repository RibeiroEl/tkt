from ninja import Schema

class ClienteCreate(Schema):
    nome: str
    email: str
    telefone: str

class FormularioSchema(Schema):
    name: str
    email: str
    phone: str
