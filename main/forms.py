from django import forms
from .models import Cliente, Fornitore, Dispositivo

class FormCliente(forms.ModelForm):

    denominazione = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }), max_length=150, required=True)
    citta = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }), max_length=150, required=True, label="Città")
    provincia = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }), max_length=150, required=True)
    picf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }), max_length=150, required=True, label="P.Iva / CF") #partita iva / codice fiscale
    #ANAGRAFICA
    #dati non obbligatori
    telefono = forms.CharField(max_length=150, required=False)
    email = forms.CharField(max_length=150, required=False)
    fatturaElettronica = forms.CharField(max_length=150, required=False)
    #referente
    nome= forms.CharField(max_length=150, required=False)
    cognome = forms.CharField(max_length=150, required=False)
    creato = forms.DateTimeField(required=False)

    class Meta:
        model = Cliente
        fields = ['denominazione', 'citta', 'provincia', 'picf', 'telefono', 'email', 'fatturaElettronica', 'nome', 'cognome' ]
