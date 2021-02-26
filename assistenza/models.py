from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
# from main.models import  Dispositivo
from main.models import Cliente, Fornitore, Rapporti
from django.core.validators import MinValueValidator
from azienda.models import CustomUser
from model_utils.fields import MonitorField, StatusField, SplitField
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _

class normativaCodice(models.Model):
    choice = models.CharField(max_length=154)

    def __str__(self):
        return str(self.choice)

# Create your models here.
class Prodotti(models.Model):

    #dati obbligatori
    codiceProdotto = models.CharField(max_length=100, verbose_name="Codice prodotto") #aggiungere in caso primary_key=True
    tipo = models.CharField(blank=True, null=True, max_length=100)
    #dati non obbligatori
    costruttore = models.CharField(blank=True, null=True, max_length=100)
    modello = models.CharField(blank=True, null=True, max_length=100)
    numeroSerie = models.CharField(blank=True, null=True, max_length=100, verbose_name="Numero serie")
    classe = models.CharField(blank=True, null=True, max_length=100)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    #relazione many-to-one
    fornitore = models.ForeignKey(Fornitore, on_delete=models.CASCADE, null=True, blank=True)
    creato = models.DateTimeField(auto_now_add=True, verbose_name='Data creazione')
    normativa = models.ManyToManyField(normativaCodice)
    inventario = models.CharField(max_length=50, verbose_name="Inventario", null=True)

    def __str__(self):
        return self.codiceProdotto

    class Meta:
        verbose_name = "Strumento"
        verbose_name_plural = "Strumenti"

class Verifica(models.Model):

    stato_verifica = [
            ('0', 'Pratica creata'),
            ('1', 'Richiesta'),
            ('2', 'Preventivo'),
            ('3','Eseguito'),
            ('4','Elaborazione'),
            ('5','Inviate'),
            ('6','Pagato'),
            ('7','Consegnato'),
            ('8','Chiuso'),
        ]

    stato_scadenza = [
            ('9', 'Attivo'),
            ('10', 'In scadenza'),
            ('11','Scaduto')
    ]
    metodo_pagamento = (
            ('bonifico', 'bonifico'),
            ('assegno', 'assegno'),
            ('carta', 'carta'),
            ('paypal','paypal'),
            ('cassa','cassa'),
        )
    cei_multiple = (
    ('66-5', '66-5'),
    ('62-5', '62-5'),
    ('62-13', '62-13'),
    ('14175', '14175'),
    ('12469', '12469'),
    )

    codiceID = models.CharField(max_length=100, verbose_name="ID",  blank=True, null=True,)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    stato = models.CharField( max_length=20, blank=True, null=True, default='0')
    ultimaModifica = models.DateTimeField(null=True, blank=True, verbose_name="Ultima moodifica")
    prodotti = models.ManyToManyField(Prodotti, related_name='verifica_related', blank=True, verbose_name="Strumenti")
    #creatoIniziale
    noteIniziali = models.CharField(max_length=300, blank=True, null=True, verbose_name='Note iniziali')
    #richiesta
    richiestaFile = models.FileField(verbose_name='Richiesta',  blank=True, null=True, upload_to="Richiesta_Verifica/%Y/%m/%d")
    #preventivo
    preventivoFile = models.FileField(verbose_name='Preventivo',  blank=True, null=True, upload_to="Preventivi_Verifica/%Y/%m/%d")
    #eseguita
    RIT = models.OneToOneField(Rapporti, on_delete =models.CASCADE , blank=True, null=True, verbose_name="RIT")
    dataVerifica = models.DateField(verbose_name="Data verifica", blank=True, null=True)
    verificaElettrica = models.IntegerField(default='0', verbose_name='V.E.',  blank=True, null=True,)
    verificaFunzionale = models.PositiveIntegerField(default='0', verbose_name='V.F.',  blank=True, null=True,)
    cei = models.ManyToManyField(normativaCodice, related_name='has_verifica', blank=True, verbose_name = 'CEI', )
    #elaborazione
    outputStrumentoFile = models.FileField(verbose_name='Output strumento',  blank=True, null=True, upload_to="Output_strumento/%Y/%m/%d")
    #inviata
    schedaFile = models.FileField(verbose_name='Scheda',  blank=True, null=True, upload_to="Scheda_Verifica/%Y/%m/%d")
    fatturaFile = models.FileField(verbose_name='Fattura',  blank=True, null=True, upload_to="Fattura_Verifica/%Y/%m/%d")
    #pagato
    ricevutaPagamentoFile = models.FileField(verbose_name='Ricevuta',  blank=True, null=True, upload_to="Ricevuta_Verifica/%Y/%m/%d")
    tipoPagamento = models.CharField(choices=metodo_pagamento, max_length=20, blank=True, null=True, verbose_name='Pagato con')
    prezzo = models.FloatField(default='0', blank=True, null=True, verbose_name='importo', validators=[MinValueValidator(0.0)])
    #consegnato
    noteFinali = models.CharField(max_length=300, blank=True, null=True, verbose_name='Note finali')

    creatoIniziale = models.DateTimeField(verbose_name="Creato", blank=True, null=True)
    richiesta = models.DateTimeField(verbose_name="Richiesta", blank=True, null=True)
    preventivo = models.DateTimeField(verbose_name="Preventivo", blank=True, null=True)
    eseguita = models.DateTimeField(verbose_name="Eseguita", blank=True, null=True)
    elaborazione = models.DateTimeField(verbose_name="Elaborazione", blank=True, null=True)
    inviata = models.DateTimeField(verbose_name="Inviata", blank=True, null=True)
    pagato = models.DateTimeField(verbose_name="Pagato", blank=True, null=True)
    consegnato = models.DateTimeField(verbose_name="Consegnato", blank=True, null=True)
    chiuso = models.DateTimeField(verbose_name="Chiuso", blank=True, null=True)

    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")
    #extra
    flag = models.BooleanField(default=False)
    statoX = models.CharField(max_length=20, null=True, blank=True, )
    tornaIndietro = models.BooleanField(default=False)

    def CEI(self):
        return "\n, ".join([a.choice for a in self.cei.all()])

    def STATO(self):
        s = ''
        for stato in self.stato_scadenza:
            if self.stato == stato[0]:
                s = stato[1]
        if not s:
            for stato in self.stato_verifica:
                if self.stato == stato[0]:
                    s = stato[1]
        return s


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Verifica"
        verbose_name_plural = "Verifiche"

    def dispositivi(self):
        return "\n, ".join([p.codiceProdotto for p in self.dispositivo.all()])


class Riparazione(models.Model):
    creatoIniziale = 'creatoIniziale'
    stato_verifica =(
            (creatoIniziale, 'Pratica creata'),
            ('richiesta', 'Richiesta'),
            ('preventivo', 'Preventivo'),
            ('autorizzazione','Autorizzazione'),
            ('eseguita','Eseguita'),
            ('verifiche','Verifiche'),
            ('fatturaEmessa','Fattura emessa'),
            ('pagato','pagato'),
            ('chiuso','chiuso'),
        )
    metodo_pagamento = (
            ('bonifico', 'bonifico'),
            ('assegno', 'assegno'),
            ('carta', 'carta'),
            ('paypal','paypal'),
            ('cassa','cassa'),
        )

    codiceID = models.CharField(max_length=100, verbose_name="ID")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    stato = models.CharField(choices=stato_verifica, max_length=20, blank=True, null=True, default=creatoIniziale)
    ultimaModifica = models.DateTimeField(null=True, blank=True, verbose_name="Ultima moodifica")

    #creatoIniziale
    noteIniziali = models.CharField(max_length=300, blank=True, null=True, verbose_name='Note')
    #richiesta
    richiestaFile = models.FileField(verbose_name='Richiesta', blank=True, upload_to="Richiesta_Riparazione/%Y/%m/%d")
    #preventivo
    preventivoFile = models.FileField(verbose_name='Preventivo', blank=True, upload_to="Preventivi_Riparazione/%Y/%m/%d")
    #Autorizzazione
    autorizzazioneFile = models.FileField(verbose_name='Autorizzazione', blank=True, upload_to="Autorizzazione_Riparazione/%Y/%m/%d")
    #eseguita
    RIT = models.OneToOneField(Rapporti, on_delete =models.CASCADE , blank=True, null=True, verbose_name="RIT")
    #verifiche
    verifica = models.ManyToManyField(Verifica, related_name='riparazione', verbose_name="Verifiche", blank=True)
    #fattura emessa
    fatturaFile = models.FileField(verbose_name='Fattura', blank=True, null=True, upload_to="Fattura_riparazione/%Y/%m/%d")
    #pagato
    ricevutaPagamentoFile = models.FileField(verbose_name='Ricevuta', blank=True, null=True, upload_to="Ricevuta_riparazione/%Y/%m/%d")
    tipoPagamento = models.CharField(choices=metodo_pagamento, max_length=20, blank=True, null=True, verbose_name='Pagato con')
    prezzo = models.FloatField(default='0', blank=True, null=True, verbose_name='importo', validators=[MinValueValidator(0.0)])

    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")
    #extra
    flag = models.BooleanField(default=False)
    statoX = models.CharField(max_length=20, null=True, blank=True, )

    creatoIniziale = models.DateTimeField(verbose_name="Creato", blank=True, null=True)
    richiesta = models.DateTimeField(verbose_name="Richiesta", blank=True, null=True)
    preventivo = models.DateTimeField(verbose_name="Preventivo", blank=True, null=True)
    autorizzazione = models.DateTimeField(verbose_name="Autorizzazione", blank=True, null=True)
    eseguita = models.DateTimeField(verbose_name="Eseguita", blank=True, null=True)
    verifiche = models.DateTimeField(verbose_name="Verifiche", blank=True, null=True)
    fatturaEmessa = models.DateTimeField(verbose_name="Fattura emessa", blank=True, null=True)
    pagato = models.DateTimeField(verbose_name="Pagato", blank=True, null=True)
    chiuso = models.DateTimeField(verbose_name="Chiuso", blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Riparazione"
        verbose_name_plural = "Riparazioni"
