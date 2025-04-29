from django.contrib import admin
from django.urls import path
from .api import api
from . import views

urlpatterns = [
    path('private/', admin.site.urls),
    path("", views.index, name="index"),  # Sua página principal (index.html)
    path("f6b23ff5746966f4e5632af44a8e723e/", views.landing, name="landing"),
    path("api/", api.urls),
    path("verify/<str:hash>", views.verify),
    path("sucesso/", views.sucesso, name="sucesso"),
    
    # URLs adicionadas para as páginas HTML que você forneceu
    path('email-confirmed/', views.confirmed_email, name='confirmed_email'),
    path('email-confirmation/', views.envio_email_confirmation, name='envio_email_confirmation'),
    
    # Nova URL para processar o formulário via AJAX
    path('form-submit/', views.form_submit, name='form_submit'),
]