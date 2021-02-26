from django.db import models
from azienda.models import CustomUser
from main.models import Cliente, Fattura, Fornitore
from azienda.models import CustomUser

# Create your models here.
class GaraPubblica(models.Model):
    stato_gara = [
                ('Creata', 'Creata'),
                ('Offerta', 'Offerta'),
                ('Compilata', 'Compilata'),
                ('Inviata','Inviata'),
                ('Aggiudicata','Aggiudicata'),
                ('Non aggiudicata','Non aggiudicata'),
            ]

    idGara = models.CharField(max_length=50, primary_key=True, verbose_name="RDO")
    amministrazione = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True,)
    oggetto = models.CharField(max_length=100)
    stato = models.CharField(choices=stato_gara, max_length=20, blank=True, null=True, default='Creata')
    importoLotti = models.PositiveIntegerField(default='0', verbose_name='Importo lotti',  blank=True, null=True,)
    vendita = models.OneToOneField(Fattura, on_delete =models.CASCADE , blank=True, null=True, verbose_name="Vendita")
    ultimaModifica = models.DateField(auto_now=True, verbose_name="Ultima moodifica")
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        return str(self.idGara)

    def LOTTI(self):
        return "\n, ".join([l.codiceLotto for l in self.lotti.all()])

    class Meta:
        verbose_name = "Gara Pubblica"
        verbose_name_plural = "Gare Pubbliche"


class Lotto(models.Model):
    codiceLotto = models.CharField(max_length=100, verbose_name="ID",  blank=True, null=True,)
    offerta = models.ManyToManyField(Fornitore, related_name='has_lotto', blank=True, verbose_name="Offerta")
    preventivoFile = models.FileField(verbose_name='Preventivo',  blank=True, null=True, upload_to="Preventivi_Lotti/%Y/%m/%d")
    importo = models.PositiveIntegerField(default='0', verbose_name='Importo',  blank=True, null=True,)
    gara = models.ForeignKey(GaraPubblica, related_name='has_lotto', on_delete=models.CASCADE, blank=True)
    file = models.FileField(verbose_name='Altri file',  blank=True, null=True, upload_to="File_lotto/%Y/%m/%d")


    def __str__(self):
        return str(self.codiceLotto)

    class Meta:
        verbose_name = "Lotto"
        verbose_name_plural = "Lotti"


class AltriFile(models.Model):
    file = models.FileField(upload_to="pdf_gare_/%Y/%m/%d", blank=True, null=True)
    gara = models.ForeignKey(GaraPubblica, on_delete=models.CASCADE)
