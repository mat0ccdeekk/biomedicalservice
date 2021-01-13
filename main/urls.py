from django.contrib import admin
from django.urls import path, include
from .views import aggiungiCliente, eliminaCliente, modificaCliente, visualizzaCliente

urlpatterns = [
    path('visualizza/', visualizzaCliente, name='visualizzaCliente'),
    path('elimina/<int:id>', eliminaCliente, name='elimina_cliente'),
    path('modifica/<int:id>', modificaCliente, name='modifica_cliente'),
    path('aggiungi/', aggiungiCliente, name='aggiungi_cliente'),

]
