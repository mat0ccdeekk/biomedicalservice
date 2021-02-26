from django.contrib import admin
from django.urls import path, include
from .views import  visualizzaCliente

# aggiungiCliente, eliminaCliente, modificaCliente,

urlpatterns = [
    path('main/acquisti/', visualizzaCliente, name='visualizzaCliente'),
    # path('elimina/<int:id>', eliminaCliente, name='elimina_cliente'),
    # path('modifica/<int:id>', modificaCliente, name='modifica_cliente'),
    # path('aggiungi/', aggiungiCliente, name='aggiungi_cliente'),

]
