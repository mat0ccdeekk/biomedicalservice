from django.contrib import admin
from django.contrib.auth.models import Group
from .models import  Acquisti, Cliente, Dispositivo, Fattura,  Fornitore, Prodotti
from import_export.admin import  ImportExportModelAdmin
from .resources import  DispositivoResource, ClienteResource, FornitoreResource
from django.db.models import F
from copy import deepcopy
import datetime
from jet.admin import CompactInline
from django import forms
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, redirect

# Register your models here.

admin.site.site_header = "Biomedical Service srl"
admin.site.unregister(Group)

def msgRedirect(request, key, msg):
    messages.add_message(request, messages.WARNING, msg)
    return redirect('/admin/main/acquisti/'+key+'/change/')

def generaCodice(Modello, sigla):
    m = Modello.objects.all().last()
    year = datetime.date.today().year
    key = m.id
    codice = str(key)+sigla+str(year)
    Modello.objects.filter(pk=str(key)).update(codiceID=codice)

# admin.TabularInline
# admin.StackedInline
@admin.register(Prodotti)
class ProdottiModelAdmin(admin.ModelAdmin):
    model = Prodotti

class AddProdottiModelAdmin(admin.TabularInline):
    model = Prodotti
    extra = 0

@admin.register(Acquisti)
class AcquistiModelAdmin(admin.ModelAdmin):
    inlines = [AddProdottiModelAdmin]
    model = Acquisti
    list_display = ['codiceID', 'fornitore', 'stato' , 'creato', 'prezzo', 'user']
    search_fields = ['codiceID', 'fornitore', 'stato' ,  'DDT', 'preventivo', 'fattura', 'track', 'creato', 'user']
    ordering = ('creato',)
    readonly_fields = [ 'codiceID', 'user', ]
    fields = ['fornitore', 'stato' , 'prezzo', 'track', 'preventivo', 'DDT', 'fattura','ordinato' , 'spedito' , 'ricevuto', 'pagato' , ]

    def get_queryset(self, request):
        prezzoTot = 0
        acquisti = super(AcquistiModelAdmin, self).get_queryset(request)
        for a in acquisti.all():
            prezzoTot += a.prezzo
        print("PREZZOOO "+str(prezzoTot))
        return acquisti


    #Modifica stato e memorizza data
    @receiver(pre_save, sender=Acquisti)
    def cambioStato(sender, instance, **kwargs):
        current = instance
        current.creato = datetime.datetime.today()
        if Acquisti.objects.filter(id=instance.id):
            previus = Acquisti.objects.get(id=instance.id)
            if previus.stato != current.stato:
                current.creato = datetime.datetime.today()
                if current.stato == 'ordinato':
                    current.ordinato = datetime.datetime.today()
                if current.stato == 'spedito':
                    current.spedito = datetime.datetime.today()
                if current.stato == 'ricevuto':
                    current.ricevuto = datetime.datetime.today()
                if current.stato == 'pagato':
                    current.pagato = datetime.datetime.today()
                if current.stato == 'chiuso':
                    current.chiuso = datetime.datetime.today()
        else:
            current.ordinato = datetime.datetime.today()


    def response_add(request, obj, post_url_continue=None):
        a = Acquisti.objects.all().last()
        if a.stato != 'ordinato':
            Acquisti.objects.all().last().delete()
            # messages.add_message(request, messages.WARNING, 'Attenzione hai appena creato una pratica e forse hai sbagliato stato iniziale !')
            return redirect('/admin/main/acquisti/add/HAI INSERITO UNO STATO INIZIALE SBAGLIATO')
        return redirect('/admin/main/acquisti/')

    #Memorizza utente che apre la pratica
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


    #Avviso di errori in caso di mancato / errato inserimento
    def response_change(self, request, obj):
        k = str(obj.id)
        if obj.stato == 'ordinato' and obj.preventivo == ''  :
            return msgRedirect(request, k, 'Inserisci preventivo')

        elif obj.stato == 'spedito' and obj.track == None :
            return msgRedirect(request, k, 'Inserire tracking')

        elif obj.stato == 'ricevuto' and obj.DDT == '' :
            return msgRedirect(request, k, 'Inserire il DDT')

        elif obj.stato == 'pagato' and obj.fattura == '' :
            return msgRedirect(request, k, 'Inserire la fattura')

        elif obj.stato == 'chiuso' and obj.prezzo <= 0 :
            return msgRedirect(request, k, 'Prezzo errato')

        return redirect('/admin/main/acquisti/')

    def save_related(self, request, form, formsets, change):
        # prezzoTot = 0
        # for inlines in formsets:
        #     for inline_form in inlines:
        #         fornitore = form.cleaned_data['fornitore']
        #         codiceProdotto = inline_form.cleaned_data['codiceProdotto']
        #         descrizione = inline_form.cleaned_data['descrizione']
        #         quantita = inline_form.cleaned_data['quantita']
        #         prezzo = inline_form.cleaned_data['prezzo']
        #         iva = inline_form.cleaned_data['iva']
        #         prezzoTot += quantita * prezzo
        #         print("CHANGE "+str(change))
        #         disp = Dispositivo(fornitore=fornitore, codiceProdotto=codiceProdotto, descrizione=descrizione, quantita=quantita, prezzo=prezzo, iva=iva)
        #         disp.save()
        #Update prezzo totale
        # k = Acquisti.objects.all().last()
        # Acquisti.objects.filter(pk=str(k)).update(prezzo=prezzoTot)
        generaCodice(Acquisti, "A")
        return super(AcquistiModelAdmin, self).save_related(request, form, formsets, change)

@admin.register(Fornitore)
class FornitoreModelAdmin(admin.ModelAdmin):
    model = Fornitore
    list_display = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'creato']
    search_fields = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'fatturaElettronica', 'nome', 'cognome', 'creato']
    resource_class = FornitoreResource

#Magazzino
@admin.register(Dispositivo)
class DispositivoModelAdmin(admin.ModelAdmin):
    model = Dispositivo
    list_display = ['codiceProdotto', 'descrizione', 'quantita' , 'fornitore', 'ultima_modifica']
    search_fields = ['fornitore__denominazione', 'codiceProdotto', 'descrizione',  'ultima_modifica']
    resource_class = DispositivoResource
    ordering = ('ultima_modifica',)

    def get_queryset(self, request):
        qs = super(DispositivoModelAdmin, self).get_queryset(request)
        return qs.filter(quantita__gte=1)

#Vendite
@admin.register(Fattura)
class FatturaModelAdmin(admin.ModelAdmin):
    model = Fattura
    list_display = ['codiceID', 'cliente', 'DDT', 'fattura', 'RIT', 'creato']
    search_fields = [ 'cliente__denominazione', 'dispositivo__codiceProdotto']
    readonly_fields = ['codiceID']
    ordering = ('creato',)

    def save_related(self, request, form, formsets, change):
        generaCodice(Fattura, "V")
        return super(FatturaModelAdmin, self).save_related(request, form, formsets, change)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if form.is_valid():
            merce = form.cleaned_data['dispositivo']
            key = merce.values_list('id', flat=True)
            for k in key:
                quantita = Dispositivo.objects.filter(pk=k).update(quantita=F('quantita') - 1)

        return super().save_model(request, obj, form, change)


@admin.register(Cliente)
class ClienteModelAdmin(ImportExportModelAdmin):
    model = Cliente
    list_display = ['codiceID','denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'creato']
    search_fields = ['codiceID', 'denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'fatturaElettronica', 'nome', 'cognome', 'creato']
    readonly_fields = ['codiceID']
    resource_class = ClienteResource

    def save_related(self, request, form, formsets, change):
        generaCodice(Cliente, "CL")
        return super(ClienteModelAdmin, self).save_related(request, form, formsets, change)

    # def save_model(self, request, obj, form, change):
    #     self.codiceID = str(obj.id) + 1
    #     print("yes")
    #     super(ClienteModelAdmin, self).save_model(request, obj, form, change)
