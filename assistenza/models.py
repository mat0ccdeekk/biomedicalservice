from django.db import models
from main.models import  Dispositivo
from main.models import Cliente, Fornitore

# Create your models here.
class Prodotti(models.Model):
    #dati obbligatori
    codiceProdotto = models.CharField(max_length=100, verbose_name="Codice prodotto") #aggiungere in caso primary_key=True
    tipo = models.CharField(blank=True, max_length=100)
    #dati non obbligatori
    costruttore = models.CharField(blank=True, max_length=100)
    modello = models.CharField(blank=True, max_length=100)
    numeroSerie = models.CharField(blank=True, max_length=100, verbose_name="Numero serie")
    classe = models.CharField(blank=True, max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    #relazione many-to-one
    fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE, null=True, blank=True)
    creato = models.DateTimeField(auto_now_add=True, verbose_name='Data creazione')

    def __str__(self):
        return self.codiceProdotto

    class Meta:
        verbose_name = "Dispositivo"
        verbose_name_plural = "Dispositivi"

class Verifica(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    dispositivo = models.ManyToManyField(Prodotti, related_name='verifiche')
    verificaElettrica = models.BooleanField(verbose_name='Verifica elettrica')
    verificaFunzionale = models.BooleanField(verbose_name='Verifica funzionale')
    dataVerifica = models.DateField(verbose_name='Data verifica')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Verifica"
        verbose_name_plural = "Verifiche"

    def dispositivi(self):
        return "\n, ".join([p.codiceProdotto for p in self.dispositivo.all()])


class Riparazione(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    dispositivo = models.ManyToManyField(Prodotti, related_name='riparazioni')
    dataRiparazione = models.DateField(verbose_name='Data riparazione')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Riparazione"
        verbose_name_plural = "Riparazioni"
