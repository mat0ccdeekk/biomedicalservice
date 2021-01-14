from django.contrib import admin
from django.contrib.auth.models import Group
from .models import  Acquisti, Cliente, Dispositivo, Fattura,  Fornitore, Prodotti
from import_export.admin import  ImportExportModelAdmin
from .resources import  DispositivoResource, ClienteResource, FornitoreResource
from django.db.models import F
from copy import deepcopy
import datetime
from jet.admin import CompactInline

# Register your models here.

admin.site.site_header = "Biomedical Service srl"
admin.site.unregister(Group)

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
    list_display = ['codiceID', 'fornitore', 'creato', 'pagamento']
    search_fields = ['id', 'fornitore', 'DDT', 'RIT', 'fattura', 'creato']
    ordering = ('creato',)
    list_editable = ['pagamento']
    readonly_fields = ['codiceID']

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
        generaCodice(Acquisti, "AC")
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
        generaCodice(Fattura, "VE")
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
