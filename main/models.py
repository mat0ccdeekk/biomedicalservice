from django.db import models
# Create your models here.

# class FornitorePlus(models.Model):
#     fornitoreplus = models.OneToOneField(Fornitore, on_delete=models.CASCADE, verbose_name="Fornitore")
class Cliente(models.Model):

    #dati obbligatori
    denominazione = models.CharField(blank=True, max_length=150)
    citta = models.CharField(blank=True, max_length=100, verbose_name="città")
    provincia = models.CharField(blank=True, max_length=10)
    picf = models.CharField(blank=True, max_length=100, verbose_name='P.iva / CF') #partita iva / codice fiscale
    #ANAGRAFICA
    #dati non obbligatori
    telefono = models.CharField(blank=True, max_length=100)
    email = models.CharField(blank=True, max_length=100)
    fatturaElettronica = models.CharField(blank=True, max_length=150, verbose_name='Fattura elettronica')
    #referente
    nome= models.CharField(blank=True, max_length=100)
    cognome = models.CharField(blank=True, max_length=100)
    creato = models.DateTimeField(auto_now_add=True, verbose_name="Data creazione")

    def __str__(self):
        return self.denominazione

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clienti"


class Fornitore(models.Model):
    #dati obbligatori
    denominazione = models.CharField(blank=True, max_length=150)
    citta = models.CharField(blank=True, max_length=100, verbose_name="Città")
    provincia = models.CharField(blank=True, max_length=10)
    picf = models.CharField(blank=True, max_length=100, verbose_name='P.iva / CF') #partita iva / codice fiscale
    #dati non obbligatori
    telefono = models.CharField(blank=True, max_length=100)
    email = models.CharField(blank=True, max_length=100)
    fatturaElettronica = models.CharField(blank=True, max_length=150, verbose_name='Fattura elettronica')
    #referente
    nome= models.CharField(blank=True, max_length=100)
    cognome = models.CharField(blank=True, max_length=100)
    creato = models.DateTimeField(auto_now_add=True, verbose_name="Data creazione")

    def __str__(self):
        return self.denominazione

    class Meta:
        verbose_name = "fornitore"
        verbose_name_plural = "fornitori"




class Acquisti(models.Model):
    fornitore= models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    codiceProdotto = models.CharField(max_length=100, verbose_name="Codice prodotto") #aggiungere in caso primary_key=True
    descrizione = models.CharField(blank=True, max_length=200)
    DDT = models.FileField(upload_to="DDT_Acquisti/%Y/%m/%d")
    fattura = models.FileField(upload_to="Fattura_Acquisti/%Y/%m/%d")
    creato = models.DateField(verbose_name="Data acquisto")
    prezzo = models.IntegerField(default='0')
    quantita = models.IntegerField(blank=True, default="1", verbose_name="quantità")

    def __str__(self):
        return self.codiceProdotto

    class Meta:
        verbose_name = "Acquisto"
        verbose_name_plural = "Acquisti"

#Magazzino
class Dispositivo(models.Model):
    fornitore= models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    codiceProdotto = models.CharField(max_length=100, verbose_name="Codice prodotto") #aggiungere in caso primary_key=True
    descrizione = models.CharField(blank=True, max_length=200)
    creato = models.DateTimeField(auto_now_add=True, verbose_name="data creazione")
    prezzo = models.IntegerField(default='0')
    quantita = models.IntegerField(blank=True, default="1", verbose_name="quantità")

    def __str__(self):
        return self.codiceProdotto

    class Meta:
        verbose_name = "Merce"
        verbose_name_plural = "Merci"

class Installazioni(models.Model):
    dispVenduti = models.OneToOneField(Dispositivo, on_delete=models.CASCADE, verbose_name='Dispositivo')
    installato = models.BooleanField(default=True)
    doc = models.FileField(blank=True, null=True, upload_to="installazioni/%Y/%m/%d")
    data = models.DateField(blank=True, null=True, verbose_name='Data installazione')
    creato = models.DateTimeField(auto_now_add=True, verbose_name="data creazione")

#Vendite
class Fattura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,  related_name='fattura_cliente',)
    dispositivo = models.ManyToManyField(Dispositivo,
                                        related_name='fattura_disp',
                                        default='0',
                                        limit_choices_to={'quantita__gte' : 1},
                                        verbose_name = "Merce"
                                    )
    fattura = models.FileField(blank=True, upload_to="fatture_vendita/%Y/%m/%d")
    DDT = models.FileField(upload_to="DDT_vendita/%Y/%m/%d")
    creato = models.DateField(verbose_name="data vendita")

    def merce(self):
        return "\n, ".join([p.codiceProdotto for p in self.dispositivo.all()])

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Vendita"
        verbose_name_plural = "Vendite"
