from django.db import models

# Create your models here.

class GaraPubblica(models.Model):
    idGara = models.CharField(max_length=50, primary_key=True)
    ente = models.CharField(max_length=100)
    scadenza = models.DateField()
    oggetto = models.CharField(max_length=100)
    bando = models.FileField(blank=True)


    def __str__(self):
        return self.idGara

    class Meta:
        verbose_name = "Gara Pubblica"
        verbose_name_plural = "Gare Pubbliche"

class AltriFile(models.Model):
    file = models.FileField(upload_to="pdf_gare_/%Y/%m/%d", blank=True, null=True)
    gara = models.ForeignKey(GaraPubblica, on_delete=models.CASCADE)
