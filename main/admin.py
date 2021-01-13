from django.contrib import admin
from django.contrib.auth.models import Group
from .models import  Acquisti, Cliente, Dispositivo, Fattura,  Fornitore, Installazioni
from import_export.admin import  ImportExportModelAdmin
from .resources import  DispositivoResource, ClienteResource, FornitoreResource
from django.db.models import F
from copy import deepcopy

from jet.admin import CompactInline

# Register your models here.

admin.site.site_header = "Biomedical Service srl"
admin.site.unregister(Group)

@admin.register(Acquisti)
class AcquistiModelAdmin(admin.ModelAdmin):
    model = Acquisti
    list_display = ['codiceProdotto', 'fornitore', 'prezzo', 'quantita', 'DDT', 'fattura', 'creato']
    search_fields = ['codiceProdotto', 'fornitore', 'prezzo', 'DDT', 'fattura', 'creato']
    ordering = ('creato',)
    list_editable = ['quantita']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        print(obj)
        new_instance = deepcopy(obj)
        new_instance.id = None
        new_instance.save()

        # str(Acquisti.objects.all()))
        if form.is_valid():
            codiceProdotto = form.cleaned_data['codiceProdotto']
            fornitore = form.cleaned_data['fornitore']
            prezzo = form.cleaned_data['prezzo']
            creato = form.cleaned_data['creato']
            quantita = form.cleaned_data['quantita']
            descrizione = form.cleaned_data['descrizione']
            d = Dispositivo(codiceProdotto=codiceProdotto, fornitore=fornitore, prezzo=prezzo, creato=creato, quantita=quantita, descrizione=descrizione)
            d.save()

            # key = merce.values_list('id', flat=True)
            # for k in key:
            #     quantita = Dispositivo.objects.filter(pk=k).update(quantita=F('quantita') - 1)

        super().save_model(request, obj, form, change)


# admin.TabularInline
# admin.StackedInline
class AddAcquistiModelAdmin(admin.TabularInline):
    model = Acquisti
    extra = 0


@admin.register(Fornitore)
class FornitoreModelAdmin(admin.ModelAdmin):
    inlines = [AddAcquistiModelAdmin]
    model = Fornitore
    list_display = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'creato']
    search_fields = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'fatturaElettronica', 'nome', 'cognome', 'creato']
    resource_class = FornitoreResource


#Magazzino
@admin.register(Dispositivo)
class DispositivoModelAdmin(admin.ModelAdmin):
    model = Dispositivo
    list_display = ['codiceProdotto', 'descrizione', 'quantita' , 'fornitore', 'creato']
    search_fields = ['fornitore__denominazione', 'codiceProdotto', 'descrizione',  'creato']
    resource_class = DispositivoResource
    list_editable = ['quantita']
    ordering = ('creato',)


    def get_queryset(self, request):
        qs = super(DispositivoModelAdmin, self).get_queryset(request)
        return qs.filter(quantita__gte=1)

#Vendite
@admin.register(Fattura)
class FatturaModelAdmin(admin.ModelAdmin):
    model = Fattura
    list_display = ['id','cliente', 'fattura', 'creato']
    search_fields = [ 'cliente__denominazione', 'dispositivo__codiceProdotto']
    ordering = ('creato',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if form.is_valid():
            merce = form.cleaned_data['dispositivo']
            key = merce.values_list('id', flat=True)
            for k in key:
                quantita = Dispositivo.objects.filter(pk=k).update(quantita=F('quantita') - 1)

        super().save_model(request, obj, form, change)


@admin.register(Installazioni)
class InstallazioniModelAdmin(admin.ModelAdmin):
    model = Installazioni
    list_display = ['dispVenduti', 'installato', 'doc', 'data']
    search_fields = ['dispVenduti', 'installato', 'doc', 'data']
    list_editable = ['installato']
    ordering = ('creato',)


@admin.register(Cliente)
class ClienteModelAdmin(ImportExportModelAdmin):
    model = Cliente
    list_display = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'creato']
    search_fields = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'fatturaElettronica', 'nome', 'cognome', 'creato']
    resource_class = ClienteResource
