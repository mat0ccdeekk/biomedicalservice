from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    #dati obbligatori
    codiceID = models.CharField(max_length=100, verbose_name="Codice")
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
    creato = models.DateField(auto_now_add=True, verbose_name="Data creazione")

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
    creato = models.DateField(auto_now_add=True, verbose_name="Data creazione")

    def __str__(self):
        return self.denominazione

    class Meta:
        verbose_name = "fornitore"
        verbose_name_plural = "fornitori"


class Acquisti(models.Model):
    stato_acquisti =(
            ('ordinato', 'Ordinato'),
            ('spedito','Spedito'),
            ('ricevuto','Ricevuto'),
            ('pagato','Pagato'),
            ('chiuso','Chiuso'),
        )

    fornitore= models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    stato = models.CharField(choices=stato_acquisti, max_length=20, blank=True, null=True)
    track = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tracking')
    preventivo = models.FileField(upload_to="Fattura_Acquisti/%Y/%m/%d")
    DDT = models.FileField(upload_to="DDT_Acquisti/%Y/%m/%d", blank=True)
    fattura = models.FileField(blank=True, upload_to="fatture_Acquisti/%Y/%m/%d")
    prezzo = models.IntegerField(default='0', blank=True, null=True, verbose_name='importo')
    creato = models.DateTimeField(verbose_name="Data")

    ordinato = models.DateTimeField(verbose_name="Ordinato", blank=True, null=True)
    spedito = models.DateTimeField(verbose_name="Spedito", blank=True, null=True)
    ricevuto = models.DateTimeField(verbose_name="ricevuto", blank=True, null=True)
    pagato = models.DateTimeField(verbose_name="pagato", blank=True, null=True)
    chiuso = models.DateTimeField(verbose_name="chiuso", blank=True, null=True)


    codiceID = models.CharField(max_length=100, verbose_name="ID")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Acquisto"
        verbose_name_plural = "Acquisti"

#Prodotto nascosto
class Prodotti(models.Model):
    acquisto= models.ForeignKey(Acquisti, on_delete=models.CASCADE, related_name="prodotti_acquistati")
    codiceProdotto = models.CharField(max_length=100, verbose_name="Codice prodotto") #aggiungere in caso primary_key=True
    descrizione = models.CharField(blank=True, max_length=200)
    quantita = models.IntegerField(blank=True, default="1", verbose_name="quantità")
    prezzo = models.IntegerField(default='0')
    iva = models.IntegerField(default='22')


    def __str__(self):
        return self.codiceProdotto

    class Meta:
        verbose_name = "Prodotto"
        verbose_name_plural = "Prodotti"

#Magazzino
class Dispositivo(models.Model):
    fornitore= models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    codiceProdotto = models.CharField(max_length=100, verbose_name="Codice prodotto") #aggiungere in caso primary_key=True
    descrizione = models.CharField(blank=True, max_length=200)
    quantita = models.IntegerField(blank=True, default="1", verbose_name="quantità")
    prezzo = models.IntegerField(default='0')
    iva = models.IntegerField(default='22')
    ultima_modifica = models.DateField(auto_now_add=True, verbose_name="Ultima modifica")

    def __str__(self):
        return self.codiceProdotto

    class Meta:
        verbose_name = "Merce"
        verbose_name_plural = "Merci"


#Vendite
class Fattura(models.Model):
    codiceID = models.CharField(max_length=100, verbose_name="Codice")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,  related_name='fattura_cliente',)
    dispositivo = models.ManyToManyField(Dispositivo,
                                        related_name='fattura_disp',
                                        default='0',
                                        limit_choices_to={'quantita__gte' : 1},
                                        verbose_name = "Merce"
                                    )
    DDT = models.FileField(upload_to="DDT_vendita/%Y/%m/%d")
    fattura = models.FileField(blank=True, upload_to="fatture_vendita/%Y/%m/%d")
    RIT = models.FileField(upload_to="RIT_vendita/%Y/%m/%d")
    creato = models.DateField(verbose_name="data vendita")
    autore = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    def merce(self):
        return "\n, ".join([p.codiceProdotto for p in self.dispositivo.all()])

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Vendita"
        verbose_name_plural = "Vendite"
