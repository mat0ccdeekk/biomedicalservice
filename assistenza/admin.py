from django.contrib import admin
from assistenza.models import Verifica, Riparazione, Prodotti
# Register your models here.

class VerificaModelAdmin(admin.ModelAdmin):
    model = Verifica
    list_display = ['id', 'cliente', 'dispositivi', 'verificaElettrica', 'verificaFunzionale', 'dataVerifica']
    search_fields = ['cliente__denominazione', 'dispositivo__codiceProdotto','dataVerifica']

class RiparazioneModelAdmin(admin.ModelAdmin):
    model = Riparazione
    list_display = ['id', 'cliente', 'dataRiparazione']
    search_fields = ['cliente__denominazione', 'dispositivo__codiceProdotto', 'dataRiparazione']

class ProdottiModelAdmin(admin.ModelAdmin):
    model = Prodotti
    list_display = ['codiceProdotto', 'cliente', 'tipo','costruttore', 'modello', 'numeroSerie', 'classe',  'creato']
    search_fields = ['cliente__denominazione', 'fornitore__denominazione','codiceProdotto', 'tipo','costruttore', 'modello', 'numeroSerie', 'classe', 'cliente__denominazione', 'creato']

admin.site.register(Verifica, VerificaModelAdmin)
admin.site.register(Riparazione, RiparazioneModelAdmin)
admin.site.register(Prodotti, ProdottiModelAdmin)
