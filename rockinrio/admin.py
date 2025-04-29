from .models import *
from django.contrib import admin

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "telefone", "status",)
    readonly_fields = ("nome", "email", "telefone", "status",)

admin.site.register(Codigo)