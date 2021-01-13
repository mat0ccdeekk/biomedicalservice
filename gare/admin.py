from django.contrib import admin
from .models import GaraPubblica, AltriFile
# Register your models here.
#
class FileModelAdmin(admin.StackedInline):
    model = AltriFile

@admin.register(GaraPubblica)
class GaraPubblicaModelAdmin(admin.ModelAdmin):
    inlines = [FileModelAdmin]
    model = GaraPubblica
    list_display = ['idGara', 'ente', 'oggetto', 'scadenza', 'bando']
    search_fields = ['idGara', 'ente', 'oggetto', 'scadenza']

@admin.register(AltriFile)
class FileModelAdmin(admin.ModelAdmin):
    models = AltriFile
    list_display = ['file', 'gara']
    search_fields = ['file', 'gara']


# admin.site.register(GaraPubblica, GaraPubblicaModelAdmin)
# admin.site.register(AltriFile, FileModelAdmin)
