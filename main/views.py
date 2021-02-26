from django.shortcuts import render, redirect
from .models import Cliente, Fornitore, Fattura
# from .forms import FormCliente
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
# # Create your views here.
#
#
def visualizzaCliente(request):
    clienti = Cliente.objects.all()

    context = {"clienti": clienti}
    return render(request, "main/module.html", context)
#
# def modificaCliente(request, id):
#     if request.method == "GET":
#         cliente = Cliente.objects.get(pk=id)
#         formCliente = FormCliente(instance=cliente)
#         return render(request, "main/aggiungiCliente.html", {'formCliente': formCliente})
#     else:
#         cliente = Cliente.objects.get(pk=id)
#         formCliente = FormCliente(request.POST, instance=cliente)
#         if formCliente.is_valid():
#             formCliente.save()
#             messages.add_message(request, messages.SUCCESS, 'Cliente aggiornato con successo')
#             return redirect('/clienti/visualizza/')
#         else:
#             messages.add_message(request, messages.SUCCESS, 'Dati errati o mancanti')
#
#
# def aggiungiCliente(request):
#     if request.method == "POST":
#         formCliente = FormCliente(request.POST)
#         if formCliente.is_valid():
#             formCliente.save()
#             messages.add_message(request, messages.SUCCESS, 'Cliente salvato con successo')
#             return redirect('/clienti/aggiungi/')
#         else:
#             messages.add_message(request, messages.WARNING, 'Dati errati o mancanti')
#
#     formCliente = FormCliente()
#     context = {"formCliente" : formCliente }
#     return render(request, "main/aggiungiCliente.html", context)
#
#
#
# def eliminaCliente(request, id):
#     cliente = Cliente.objects.get(pk=id)
#     cliente.delete()
#     return redirect('/clienti/visualizza/')
