from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator
from azienda.models import CustomUser

# from assistenza.models import Rapporti

# Create your models here.

class Cliente(models.Model):
    codiceID = models.CharField(max_length=100, verbose_name="ID")
    denominazione = models.CharField(blank=True, max_length=150)
    citta = models.CharField(blank=True, null=True, max_length=100, verbose_name="città")
    provincia = models.CharField(blank=True, null=True, max_length=10)
    picf = models.CharField(blank=True, null=True, max_length=100, verbose_name='P.iva / CF')
    telefono = models.CharField(blank=True, null=True, max_length=100)
    email = models.CharField(blank=True, null=True, max_length=100)

    #Almeno uno dei due obbligatori
    PEC = models.CharField(blank=True, null=True, max_length=100)
    fatturaElettronica = models.CharField(blank=True, max_length=150, null=True, verbose_name='Cod. UNIVOCO')
    #referente
    referente = models.CharField(blank=True, null=True,  max_length=100, verbose_name='Referente')
    emailReferente = models.CharField(blank=True, null=True, max_length=100, verbose_name='Email referente')
    telefonoReferente = models.CharField(blank=True, null=True, max_length=100, verbose_name='Telefono referente')

    creato = models.DateField(auto_now_add=True, verbose_name="Data creazione")
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")


    def __str__(self):
        return self.denominazione

    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clienti"

class Fornitore(models.Model):
    codiceID = models.CharField(max_length=100, verbose_name="ID")
    denominazione = models.CharField(blank=True, max_length=150)
    citta = models.CharField(blank=True, null=True, max_length=100, verbose_name="Città")
    provincia = models.CharField(blank=True, null=True,  max_length=10)
    picf = models.CharField(blank=True, null=True,  max_length=100, verbose_name='P.iva / CF') #partita iva / codice fiscale
    telefono = models.CharField(blank=True, null=True,  max_length=100)
    email = models.CharField(blank=True, null=True,  max_length=100)

    #Almeno uno dei due obbligatori
    PEC = models.CharField(blank=True, null=True, max_length=100)
    fatturaElettronica = models.CharField(blank=True, null=True,  max_length=150, verbose_name='Cod. UNIVOCO')
    #referente
    referente = models.CharField(blank=True, null=True,  max_length=100, verbose_name='Referente')
    emailReferente = models.CharField(blank=True, null=True, max_length=100, verbose_name='Email referente')
    telefonoReferente = models.CharField(blank=True, null=True, max_length=100, verbose_name='Telefono referente')

    creato = models.DateField(auto_now_add=True, null=True,  verbose_name="Data creazione")
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")


    def __str__(self):
        return self.denominazione

    class Meta:
        verbose_name = "fornitore"
        verbose_name_plural = "fornitori"

class Rapporti(models.Model):
    codiceID = models.CharField(max_length=100, verbose_name="ID", blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,  related_name='rapporti_cliente',)
    dataModificabile = models.DateTimeField(verbose_name="Data", blank=True, null=True)
    dataUltimaModifica = models.DateTimeField(verbose_name="Ultima modifica", auto_now_add=True)
    RIT = models.FileField(upload_to="Rapporti_RIT/%Y/%m/%d", verbose_name="RIT")
    richiestaFile = models.FileField(null=True, blank=True, upload_to="Rapporti_richiesta/%Y/%m/%d", verbose_name="Richiesta File")
    richiestaID = models.CharField(max_length=100, verbose_name="Richiesta", null=True, blank=True,)
    tecnico = models.CharField(max_length=100, verbose_name="Tecnico", null=True, blank=True,)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")

    def file_rit(self):
        if self.RIT:
            return mark_safe('<a href="%s" target="_blank"><i class="bi bi-link"></i> Apri</a>' % (self.RIT.url,))
        else:
            return "No file"

    def __str__(self):
        return str(self.codiceID)

    class Meta:
        verbose_name = "Rapporto"
        verbose_name_plural = "Rapporti"



class Acquisti(models.Model):
    creatoIniziale = 'creatoIniziale'
    stato_acquisti =(
            (creatoIniziale, 'Creato'), #note
            ('richiesta', 'Richiesta'),   #richiesta
            ('preventivo','Preventivo'),  #preventivo
            ('ordinato', 'Ordinato'),     #confermaOrdine
            ('spedito','Spedito'),        #track
            ('ricevuto','Ricevuto'),      #ddt
            ('pagato','Pagato'),          #fattura
            ('chiuso','Conclusa'),        #prezzo
        )
    metodo_pagamento = (
            ('bonifico', 'bonifico'),
            ('assegno', 'assegno'),
            ('carta', 'carta'),
            ('paypal','paypal'),
            ('cassa','cassa'),
        )
    fornitore= models.ForeignKey(Fornitore, on_delete=models.CASCADE)
    stato = models.CharField(choices=stato_acquisti, max_length=20, blank=True, null=True, default=creatoIniziale)
    #dati da inserire
    note = models.CharField(max_length=300, blank=True, null=True, verbose_name='Note') #creato
    richiestaFile = models.FileField(verbose_name='Richiesta', blank=True, upload_to="Richiesta_Acquisti/%Y/%m/%d")   #richiesta
    confermaOrdine = models.FileField(verbose_name='Conferma ordine', blank=True, upload_to="Richiesta_Acquisti/%Y/%m/%d") #ordinato

    track = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tracking')
    preventivoFile = models.FileField(verbose_name='Preventivo', blank=True, upload_to="Preventivi_Acquisti/%Y/%m/%d")
    DDT = models.FileField(upload_to="DDT_Acquisti/%Y/%m/%d", blank=True)
    fattura = models.FileField(blank=True, upload_to="Fatture_Acquisti/%Y/%m/%d")
    prezzo = models.FloatField(default='0', blank=True, null=True, verbose_name='importo', validators=[MinValueValidator(0.0)])
    creato = models.DateTimeField(null=True, blank=True, verbose_name="Ultima moodifica")
    #orari
    creatoIniziale = models.DateTimeField(verbose_name="Creato", blank=True, null=True)
    richiesta = models.DateTimeField(verbose_name="Richiesta", blank=True, null=True)
    preventivo = models.DateTimeField(verbose_name="Preventivo", blank=True, null=True)
    ordinato = models.DateTimeField(verbose_name="Ordinato", blank=True, null=True)
    spedito = models.DateTimeField(verbose_name="Spedito", blank=True, null=True)
    ricevuto = models.DateTimeField(verbose_name="ricevuto", blank=True, null=True)

    pagato = models.DateTimeField(verbose_name="Pagato", blank=True, null=True)
    tipoPagamento = models.CharField(choices=metodo_pagamento, max_length=20, blank=True, null=True, verbose_name='Pagato con')

    chiuso = models.DateTimeField(verbose_name="Conclusa", blank=True, null=True)
    #campi non modificabili
    codiceID = models.CharField(max_length=100, verbose_name="ID", blank=True, null=True,)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")

    flag = models.BooleanField(default=False)
    statoX = models.CharField(max_length=20, null=True, blank=True, )

    def __str__(self):
        return str(self.codiceID) if self.codiceID else ''

    class Meta:
        verbose_name = "Acquisto"
        verbose_name_plural = "Acquisti"


#Vendite
class Fattura(models.Model):
    creatoIniziale = 'creatoIniziale'

    stato_vendite =(
        (creatoIniziale, 'Creato'),
        ('richiestaR', 'Richiesta'),
        ('preventivoI', 'Preventivo inviato'),
        ('preventivoA','Preventivo accettato'),
        ('attesaF','Attesa fornitore'),
        ('spedito','Spedito'),
        ('consegnato','Consegnato'),
        ('installato','Installato'),
        ('collaudato','Collaudato'),
        ('fatturaEmessa','Fattura emessa'),
        ('pagato','Pagato'),
        ('chiuso','Conclusa'),
    )
    metodo_pagamento = (
            ('bonifico', 'bonifico'),
            ('assegno', 'assegno'),
            ('carta', 'carta'),
            ('paypal','paypal'),
            ('cassa','cassa'),
        )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,  related_name='vendita_cliente',)
    stato = models.CharField(choices=stato_vendite, max_length=30, blank=True, null=True, default=creatoIniziale)
    creato = models.DateTimeField(verbose_name="Ultima moodifica")
    codiceID = models.CharField(max_length=100, verbose_name="ID")

    note = models.CharField(max_length=300, blank=True, null=True, verbose_name='Note') #creato

    richiestaFile = models.FileField(verbose_name='Richiesta', blank=True, upload_to="Richiesta_vendite/%Y/%m/%d")   #richiesta
    preventivoFile = models.FileField(verbose_name="Preventivo", blank=True, upload_to="Preventivi_vendite/%Y/%m/%d")
    confermaPreventivoFile = models.FileField(blank=True, upload_to="ConfermaPrev_vendite/%Y/%m/%d", verbose_name='Conferma preventivo')
    acquisto = models.ManyToManyField(Acquisti, related_name='vendita_acquisti', verbose_name="Fornitore", blank=True, limit_choices_to={'stato':'chiuso'})
    ricevutaFile = models.FileField(blank=True, upload_to="Preventivi_vendite/%Y/%m/%d", verbose_name='Ricevuta spedizione')
    track = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tracking')
    DDT = models.FileField(upload_to="DDT_vendite/%Y/%m/%d", blank=True)
    RIT = models.OneToOneField(Rapporti, on_delete =models.CASCADE , blank=True, null=True, verbose_name="ID rapporti")
    collaudoFile = models.FileField(blank=True, upload_to="Collaudi_vendite/%Y/%m/%d", verbose_name="Collaudo")
    fatturaFile = models.FileField(blank=True, upload_to="Fatture_vendite/%Y/%m/%d", verbose_name='Fattura')
    ricevutaPagamentoFile = models.FileField(blank=True, upload_to="Ricevute_vendite/%Y/%m/%d", verbose_name='Ricevuta pagamento')
    tipoPagamento = models.CharField(choices=metodo_pagamento, max_length=20, blank=True, null=True, verbose_name='Pagato con')
    prezzo = models.FloatField(default='0', blank=True, null=True, verbose_name='importo', validators=[MinValueValidator(0.0)])

    creatoIniziale = models.DateTimeField(verbose_name="Creato", blank=True, null=True)
    richiestaR = models.DateTimeField(verbose_name="Richiesta ricevuta", blank=True, null=True)
    preventivoI = models.DateTimeField(verbose_name="Preventivo inviato", blank=True, null=True)
    preventivoA = models.DateTimeField(verbose_name="Preventivo accettato", blank=True, null=True)
    attesaF = models.DateTimeField(verbose_name="Attesa fornitore", blank=True, null=True)
    spedito = models.DateTimeField(verbose_name="Spedito", blank=True, null=True)
    consegnato = models.DateTimeField(verbose_name="Consegnato", blank=True, null=True)

    installato = models.DateTimeField(verbose_name="Installato", blank=True, null=True)
    collaudato = models.DateTimeField(verbose_name="Collaudato", blank=True, null=True)
    fatturaEmessa = models.DateTimeField(verbose_name="Fattura emessa", blank=True, null=True)

    pagato = models.DateTimeField(verbose_name="Pagato", blank=True, null=True)
    chiuso = models.DateTimeField(verbose_name="Chiuso", blank=True, null=True)

    #campi non modificabili
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")

    #extra
    flag = models.BooleanField(default=False)
    statoX = models.CharField(max_length=20, null=True, blank=True, )



    def fornitore(self):
        return "\n, ".join([a.codiceID for a in self.acquisto.all()])

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Vendita"
        verbose_name_plural = "Vendite"
