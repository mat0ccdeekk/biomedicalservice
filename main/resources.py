from import_export import resources
from .models import Dispositivo, Cliente, Fornitore


class DispositivoResource(resources.ModelResource):
    class Meta:
        model = Dispositivo


class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente

class FornitoreResource(resources.ModelResource):
    class Meta:
        model = Fornitore
