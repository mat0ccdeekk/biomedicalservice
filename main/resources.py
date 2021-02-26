from import_export import resources
from .models import  Cliente, Fornitore


# class DispositivoResource(resources.ModelResource):
#     class Meta:
#         model = Dispositivo


class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente
        skip_unchanged = True
        report_skipped = True
        exclude = ('id','telefono','email','fatturaElettronica','nome','cognome','creato','user')
        import_id_fields = ['codiceID', 'denominazione', 'citta', 'provincia', 'picf']

class FornitoreResource(resources.ModelResource):
    class Meta:
        model = Fornitore
        skip_unchanged = True
        report_skipped = True
        exclude = ('id','telefono','email','fatturaElettronica','nome','cognome','creato','user')
        import_id_fields = ['codiceID', 'denominazione', 'citta', 'provincia', 'picf']
