from django.contrib import admin
from django.contrib.auth.models import Group
from .models import  Acquisti, Cliente,  Fattura,  Fornitore, Rapporti
from import_export.admin import  ImportExportModelAdmin
from .resources import   ClienteResource, FornitoreResource
from django.db.models import F
from copy import deepcopy
import datetime
from jet.admin import CompactInline
from django import forms
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, redirect
from django.forms import ModelForm, Textarea, Form
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.
admin.site.site_header = "Biomedical Service srl"
admin.site.register(User)

def msgRedirect(request, key, pagina, msg):
    messages.add_message(request, messages.ERROR, msg)
    return redirect('/main/'+pagina+'/'+key+'/change/')

def generaCodice(Modello, sigla):
    m = Modello.objects.all().last()
    year = str(datetime.date.today().year)[-2:]
    key = m.id
    if int(key) < 10:
        zeri = '000'
    elif int(key) < 100 and int(key) >= 10 :
        zeri = '00'
    elif int(key) < 1000 and int(key) >= 100 :
        zeri = '0'
    else:
        zeri = ''
    if sigla == 'C' or sigla == 'F':
        codice = sigla+' '+zeri+str(key)
    else:
        codice = sigla+' '+str(year)+' '+zeri+str(key)
    Modello.objects.filter(pk=str(key)).update(codiceID=codice)


class AcquistiModelForm(ModelForm):

    class Meta:
        model = Acquisti
        exclude = ['user', 'codiceID', 'flag']
        widgets = {
            'note': Textarea(attrs={'cols': 50, 'rows': 6}),
            }


@admin.register(Acquisti)
class AcquistiModelAdmin(admin.ModelAdmin):
    # inlines = [AddProdottiModelAdmin]
    model = Acquisti
    list_display = ['codiceID', 'fornitore', 'stato' , 'creato', 'prezzo', 'user']
    search_fields = ['codiceID', 'fornitore', 'stato' ,  'DDT', 'preventivo', 'fattura',
                     'track', 'creato', 'user' , 'note' ,'richiesta' , 'confermaOrdine', 'tipoPagamento']
    ordering = ('-creato',)
    fields = ['fornitore', 'stato' , 'note', 'fattura', 'DDT', 'track', 'confermaOrdine' ,'preventivoFile', 'richiestaFile', 'tipoPagamento', 'prezzo',]
    readonly_fields = ()
    form = AcquistiModelForm

    #Controllo sullo stato iniziale
    def response_add(self, request, obj, post_url_continue=None):
        msg = "Impossibile salvare l' acquisto , non hai inserito i campi  :"
        stati = ['ordinato', 'ricevuto', 'pagato', 'chiuso']

        if obj.stato in stati:

            if obj.confermaOrdine == '' and obj.stato in stati[:]:
                msg += ' Conferma ordine - '

            if obj.DDT == '' and obj.stato in stati[1:] :
                msg += ' DDT - '

            if obj.fattura == '' and obj.stato in stati[2:] :
                msg += ' fattura - '

            if obj.prezzo <= 0 and obj.stato in stati[2:] :
                msg += ' il prezzo non è valido - '

            if obj.tipoPagamento == None and obj.stato in stati[2:] :
                msg += 'seleziona un metodo di pagamento'

            if not msg.endswith(":"):
                Acquisti.objects.all().last().delete()
                messages.add_message(request, messages.ERROR, msg)
                # return redirect('/main/acquisti/'+str(obj.id)+'/change/')
                return redirect('/main/acquisti/add/')

        return redirect('/main/acquisti/')


    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = ()
        self.fields = ['fornitore', 'stato' , 'note', 'fattura', 'DDT', 'track', 'confermaOrdine' ,'preventivoFile', 'richiestaFile', 'tipoPagamento', 'prezzo',]
        orari = ['creatoIniziale', 'richiesta', 'preventivo', 'ordinato', 'spedito', 'ricevuto', 'pagato', 'chiuso']

        if obj != None:
            if obj.stato == 'chiuso':
                if request.user != 'admin':
                    self.readonly_fields = tuple(self.fields) + tuple(orari)
            # stato = obj.stato
            # i = orari.index('stato')
            # self.fields += orari[0:i+1]
            if obj.stato == "creatoIniziale":
                self.fields += orari[0:1]
            elif obj.stato == "richiesta":
                self.fields +=  orari[0:2]
            elif obj.stato == "preventivo":
                self.fields += orari[0:3]
            elif obj.stato == "ordinato":
                if obj.confermaOrdine == '':
                    self.fields +=  orari[0:3]
                else:
                    self.fields +=  orari[0:4]
            elif obj.stato == "spedito":
                self.fields +=  orari[0:5]
            elif obj.stato == "ricevuto":
                if obj.DDT == '':
                    self.fields +=  orari[0:5]
                else:
                    self.fields += orari[0:6]
            elif obj.stato == "pagato":
                if obj.fattura == '':
                    self.fields += orari[0:6]
                else:
                    self.fields += orari[0:7]
            elif obj.stato == "chiuso":
                if obj.prezzo <= 0:
                    self.fields += orari[0:7]
                else:
                    self.fields += orari[:]
        return super(AcquistiModelAdmin, self).get_form(request, obj=None, **kwargs)


    #Modifica stato e memorizza data
    @receiver(pre_save, sender=Acquisti)
    def cambioStato(sender, instance, **kwargs):
        current = instance
        current.flag = False
        if Acquisti.objects.filter(id=instance.id):
            previus = Acquisti.objects.get(id=instance.id)
            if previus.stato != current.stato:
                current.statoX = current.stato
                if current.stato == 'richiesta':
                    current.richiesta = datetime.datetime.today()
                    current.creato = datetime.datetime.today()
                if current.stato == 'preventivo':
                    current.creato = datetime.datetime.today()
                    current.preventivo = datetime.datetime.today()
                if current.stato == 'ordinato':
                    if current.confermaOrdine == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.ordinato = datetime.datetime.today()
                        current.creato = datetime.datetime.today()
                if current.stato == 'spedito':
                    current.spedito = datetime.datetime.today()
                    current.creato = datetime.datetime.today()

                if current.stato == 'ricevuto':
                    if current.DDT == '' or current.confermaOrdine == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.ricevuto = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'pagato':
                    if current.fattura == '' or current.prezzo <= 0 or current.DDT == '' or current.confermaOrdine == '' or current.tipoPagamento == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.pagato = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'chiuso':
                    if current.fattura == '' or current.prezzo <= 0 or current.DDT == '' or current.confermaOrdine == '' or current.tipoPagamento == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.chiuso = datetime.datetime.today()
                        current.creato = datetime.datetime.today()


    #Controllo errori in modifcica
    def response_change(self, request, obj):
        msg = 'Impossibile cambiare lo stato,  modifica i campi :'
        stati = ['ordinato', 'ricevuto', 'pagato', 'chiuso']
        k = str(obj.id)
        if obj.flag:
            if obj.statoX in stati:
                if obj.confermaOrdine == '' and obj.statoX in stati[:]:
                    msg += ' Conferma ordine - '

                if obj.DDT == '' and obj.statoX in stati[1:] :
                    msg += ' DDT - '

                if obj.fattura == '' and obj.statoX in stati[2:] :
                    msg += ' fattura - '

                if obj.prezzo <= 0 and obj.statoX in stati[2:] :
                    msg += ' il prezzo non è valido'

                if obj.tipoPagamento == None and obj.statoX in stati[2:] :
                    msg += 'seleziona un metodo di pagamento'

                if not msg.endswith(":"):
                    messages.add_message(request, messages.ERROR, msg)
                    return redirect('/main/acquisti/'+k+'/change/')
        return redirect('/main/acquisti/')


    #Prezzo totale
    def get_queryset(self, request):
        prezzoTot = 0
        acquisti = super(AcquistiModelAdmin, self).get_queryset(request)
        for a in acquisti.all():
            prezzoTot += a.prezzo
        return acquisti

    #Memorizza utente che apre la pratica
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
            if obj.stato == 'creatoIniziale':
                obj.creatoIniziale = datetime.datetime.today()
            if obj.stato == 'richiesta':
                obj.richiesta = datetime.datetime.today()
            if obj.stato == 'preventivo':
                obj.preventivo = datetime.datetime.today()
            if obj.stato == 'ordinato':
                obj.ordinato = datetime.datetime.today()
            if obj.stato == 'spedito':
                obj.spedito = datetime.datetime.today()
            if obj.stato == 'ricevuto':
                obj.ricevuto = datetime.datetime.today()
            if obj.stato == 'pagato':
                obj.pagato = datetime.datetime.today()
            if obj.stato == 'chiuso':
                obj.chiuso = datetime.datetime.today()
            obj.creato = datetime.datetime.today()
        obj.save()


    def save_related(self, request, form, formsets, change):
        generaCodice(Acquisti, "AQ")
        return super(AcquistiModelAdmin, self).save_related(request, form, formsets, change)


#Vendite
class VenditeModelForm(ModelForm):
    class Meta:
        model = Fattura
        exclude = ['user', 'codiceID', 'flag']
        widgets = {
            'note': Textarea(attrs={ 'cols': 50, 'rows': 6, } ),
   }

@admin.register(Fattura)
class FatturaModelAdmin(admin.ModelAdmin):
    model = Fattura
    list_display = ['codiceID', 'fornitore', 'cliente', 'stato', 'creato', 'prezzo', 'user']
    fields = ['cliente', 'stato' , 'note', 'richiestaFile' , 'preventivoFile' , 'confermaPreventivoFile' , 'acquisto' ,
                'ricevutaFile' , 'track', 'DDT', 'RIT', 'collaudoFile', 'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'prezzo']

    search_fields = [ 'cliente__denominazione', 'acquisto__codiceID',  'stato' , 'creato' , 'prezzo' , 'RIT' , 'DDT', 'preventivoFile', 'fatturaFile',
                     'richiestaFile', 'confermaPreventivoFile', 'ricevutaFile', 'collaudoFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'track', 'user']
    ordering = ('-creato',)
    form = VenditeModelForm
    readonly_fields = ()
    #Controllo sullo stato iniziale
    def response_add(self, request, obj, post_url_continue=None):
        msg = "Impossibile salvare la vendita , non hai inserito i campi  :"
        stati = ['preventivoI', 'preventivoA', 'attesaF', 'spedito', 'consegnato', 'installato', 'collaudato', 'fatturaEmessa', 'pagato', 'chiuso']

        if obj.stato in stati:
            if obj.preventivoFile == '' and obj.stato in stati[:]:
                msg += ' preventivo - '

            if obj.confermaPreventivoFile == '' and obj.stato in stati[1:] :
                msg += ' Conferma preventivo - '

            # if obj.attesaF == '' and obj.stato in stati[2:] :
            #     msg += ' ID Acquisti - '

            if obj.DDT == '' and obj.stato in stati[4:] :
                msg += ' DDT - '

            # if obj.RIT == '' and obj.stato in stati[5:] :
            #     msg += ' ID RIT - '

            if obj.collaudoFile == '' and obj.stato in stati[6:] :
                msg += ' Collaudo  - '

            if obj.fatturaFile == '' and obj.stato in stati[7:] :
                msg += ' Fattura - '

            if obj.ricevutaPagamentoFile == '' and obj.stato in stati[8:] :
                msg += ' Ricevuta pagamento - '

            if obj.prezzo <= 0 and obj.stato in stati[9:] :
                msg += ' il prezzo non è valido - '

            if obj.tipoPagamento == None and obj.stato in stati[9:] :
                msg += 'seleziona un metodo di pagamento'

            if not msg.endswith(":"):
                Fattura.objects.all().last().delete()
                messages.add_message(request, messages.ERROR, msg)
                return redirect('/main/fattura/add/')

        return redirect('/main/fattura/')


    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = ()
        self.fields = ['cliente', 'stato' , 'note', 'richiestaFile' , 'preventivoFile' , 'confermaPreventivoFile' , 'acquisto' , 'ricevutaFile' , 'track', 'DDT', 'RIT', 'collaudoFile', 'fatturaFile', 'ricevutaPagamentoFile', 'prezzo']

        orari = ['creatoIniziale','richiestaR', 'preventivoI', 'preventivoA','attesaF','spedito','consegnato','installato','collaudato', 'fatturaEmessa', 'pagato', 'chiuso']
        if obj != None:
            if obj.stato == 'chiuso':
                if request.user != 'admin':
                    self.readonly_fields = tuple(self.fields) + tuple(orari)
#
            if obj.stato == 'creatoIniziale':
                self.fields +=  orari[0:1]

            elif obj.stato == "richiestaR":
                self.fields +=  orari[0:2]

            elif obj.stato == "preventivoI":
                if obj.preventivoFile == '':
                    self.fields +=  orari[0:2]
                else:
                    self.fields += orari[0:3]
#
            elif obj.stato == "preventivoA":
                if obj.confermaPreventivoFile == '':
                    self.fields += orari[0:3]
                else:
                    self.fields += orari[0:4]

            elif obj.stato == "attesaF":
                if str(obj.acquisto) == 'main.Acquisti.None':
                    self.fields += orari[0:4]
                else:
                    self.fields += orari[0:5]

            elif obj.stato == "spedito":
                self.fields +=  orari[0:6]

            elif obj.stato == "consegnato":
                if obj.DDT == '':
                    self.fields += orari[0:6]
                else:
                    self.fields +=  orari[0:7]

            elif obj.stato == "installato":
                if obj.RIT == 'main.Rapporti.None':
                    self.fields +=  orari[0:7]
                else:
                    self.fields += orari[0:8]

            elif obj.stato == "collaudato":
                if obj.collaudoFile == '':
                    self.fields += orari[0:8]
                else:
                    self.fields +=  orari[0:9]

            elif obj.stato == "fatturaEmessa":
                if obj.fatturaFile == '':
                    self.fields +=  orari[0:9]
                else:
                    self.fields += orari[0:10]

            elif obj.stato == "pagato":
                if obj.ricevutaPagamentoFile == '':
                    self.fields +=  orari[0:10]
                else:
                    self.fields += orari[0:11]

            elif obj.stato == "chiuso":
                if obj.prezzo <= 0:
                    self.fields +=  orari[0:11]
                else:
                    self.fields +=  orari[:]

        return super(FatturaModelAdmin, self).get_form(request, obj=None, **kwargs)


    def get_queryset(self, request):
        prezzoTot = 0
        vendite = super(FatturaModelAdmin, self).get_queryset(request)
        for a in vendite.all():
            prezzoTot += a.prezzo
        return vendite


    #Modifica stato e memorizza data
    @receiver(pre_save, sender=Fattura)
    def cambioStato(sender, instance, **kwargs):
        current = instance
        current.flag = False
        if Fattura.objects.filter(id=instance.id):
            previus = Fattura.objects.get(id=instance.id)
            if previus.stato != current.stato:
                current.statoX = current.stato
                if current.stato == 'richiestaR':
                    current.richiestaR = datetime.datetime.today()
                    current.creato = datetime.datetime.today()

                if current.stato == 'preventivoI':
                    if current.preventivoFile == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.preventivoI = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'preventivoA':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.preventivoA = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                #A SEGUIRE AGGIUNGERE CONTROLLO SU SELEZIONE acuisto
                if current.stato == 'attesaF':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.attesaF = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'spedito':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.spedito = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'consegnato':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '' or current.DDT == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.consegnato = datetime.datetime.today()
                        current.creato = datetime.datetime.today()
                #A SEGUIRE AGGIUNGERE CONTROLLO SU ID Rapporti
                if current.stato == 'installato':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '' or current.DDT == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.installato = datetime.datetime.today()
                        current.creato = datetime.datetime.today()


                if current.stato == 'collaudato':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '' or current.DDT == '' or current.collaudoFile == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.collaudato = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'fatturaEmessa':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '' or current.DDT == '' or current.collaudoFile == '' or current.fatturaFile == '':
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.fatturaEmessa = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'pagato':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '' or current.DDT == '' or current.collaudoFile == '' or current.fatturaFile == '' or current.ricevutaPagamentoFile == '' or current.prezzo <= 0 or current.tipoPagamento == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.pagato = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

                if current.stato == 'chiuso':
                    if current.confermaPreventivoFile == '' or current.preventivoFile == '' or current.DDT == '' or current.collaudoFile == '' or current.fatturaFile == '' or current.ricevutaPagamentoFile == '' or current.prezzo <= 0 or current.tipoPagamento == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.chiuso = datetime.datetime.today()
                        current.creato = datetime.datetime.today()

            # current.statoX = current.stato


    #Memorizza utente che apre la pratica
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
            if obj.stato == 'creatoIniziale':
                obj.creatoIniziale = datetime.datetime.today()
            if obj.stato == 'richiestaR':
                obj.richiestaR = datetime.datetime.today()
            if obj.stato == 'preventivoI':
                obj.preventivoI = datetime.datetime.today()
            if obj.stato == 'preventivoA':
                obj.preventivoA = datetime.datetime.today()
            if obj.stato == 'attesaF':
                obj.attesaF = datetime.datetime.today()
            if obj.stato == 'spedito':
                obj.spedito = datetime.datetime.today()
            if obj.stato == 'consegnato':
                obj.consegnato = datetime.datetime.today()
            if obj.stato == 'installato':
                obj.installato = datetime.datetime.today()
            if obj.stato == 'collaudato':
                obj.collaudato = datetime.datetime.today()
            if obj.stato == 'fatturaEmessa':
                obj.fatturaEmessa = datetime.datetime.today()
            if obj.stato == 'pagato':
                obj.pagato = datetime.datetime.today()
            if obj.stato == 'chiuso':
                obj.chiuso = datetime.datetime.today()
            obj.creato = datetime.datetime.today()
        obj.save()


    def response_change(self, request, obj):
        msg = 'Impossibile cambiare lo stato,  modifica i campi :'
        stati = ['preventivoI', 'preventivoA', 'attesaF', 'spedito', 'consegnato', 'installato' , 'collaudato' , 'fatturaEmessa' ,'pagato', 'chiuso']
        k = str(obj.id)
        if obj.flag:
            if obj.statoX in stati:
                if obj.preventivoFile == '' and obj.statoX in stati[:]:
                    msg += ' preventivo - '

                if obj.confermaPreventivoFile == '' and obj.statoX in stati[1:] :
                    msg += ' Conferma preventivo - '

                # if obj.attesaF == '' and obj.stato in stati[2:] :
                #     msg += ' ID Acquisti - '

                if obj.DDT == '' and obj.statoX in stati[4:] :
                    msg += ' DDT - '

                # if obj.RIT == '' and obj.stato in stati[5:] :
                #     msg += ' ID RIT - '

                if obj.collaudoFile == '' and obj.statoX in stati[6:] :
                    msg += ' Collaudo  - '

                if obj.fatturaFile == '' and obj.statoX in stati[7:] :
                    msg += ' Fattura - '

                if obj.ricevutaPagamentoFile == '' and obj.statoX in stati[8:] :
                    msg += ' Ricevuta pagamento - '

                if obj.prezzo <= 0 and obj.statoX in stati[9:] :
                    msg += ' il prezzo non è valido'

                if obj.tipoPagamento == None and obj.statoX in stati[9:] :
                    msg += 'seleziona un metodo di pagamento'

                if not msg.endswith(":"):
                    messages.add_message(request, messages.ERROR, msg)
                    return redirect('/main/fattura/'+k+'/change/')

        return redirect('/main/fattura/')


    def save_related(self, request, form, formsets, change):
        generaCodice(Fattura, "VE")
        return super(FatturaModelAdmin, self).save_related(request, form, formsets, change)


#RAPPORTI
def generaCodiceRapporti(Modello):
    m = Modello.objects.all().last()
    key = m.id
    if m.codiceID == None:
        k = Modello.objects.count()
        year = str(datetime.date.today().year)
        if k < 10:
            zeri = '000'
        elif k < 100 and k >= 10 :
            zeri = '00'
        elif k < 1000 and k >= 100 :
            zeri = '0'
        else:
            zeri = ''
        codice = zeri+str(k)+' '+str(year)
        Modello.objects.filter(pk=str(key)).update(codiceID=codice)


@admin.register(Rapporti)
class RapportiModelAdmin(admin.ModelAdmin):
    model = Rapporti
    list_display = ['codiceID', 'cliente', 'dataModificabile', 'file_rit', 'richiestaID', 'dataUltimaModifica', 'user']
    search_fields = ['codiceID', 'cliente__denominazione', 'dataModificabile', 'richiestaID', 'dataUltimaModifica', 'user']
    fields = ['cliente', 'RIT', 'richiestaFile', 'richiestaID', 'tecnico', 'codiceID', 'dataModificabile',]

    #Memorizza utente che apre la pratica
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

    def save_related(self, request, form, formsets, change):
        generaCodiceRapporti(Rapporti)
        return super(RapportiModelAdmin, self).save_related(request, form, formsets, change)


#FORNITORI
@admin.register(Fornitore)
class FornitoreModelAdmin(ImportExportModelAdmin):
    model = Fornitore
    list_display = ['codiceID', 'denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'creato', 'user']
    fields = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'PEC', 'fatturaElettronica', 'referente',
              'emailReferente', 'telefonoReferente']
    search_fields = ['codiceID' ,'denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'PEC', 'fatturaElettronica', 'referente',
                  'emailReferente', 'telefonoReferente']
    resource_class = FornitoreResource
    list_per_page = 30


    def response_add(self, request, obj, post_url_continue=None):
        if obj.PEC == None and obj.fatturaElettronica == None:
            Fornitore.objects.filter(id=obj.id).delete()
            messages.add_message(request, messages.ERROR, 'ATTENZIONE : devi inserire la PEC o il Cod. UNIVOCO')
            return redirect('/main/fornitore/add/')

        return redirect('/main/fornitore/')



    def save_related(self, request, form, formsets, change):
        generaCodice(Fornitore, "F")
        return super(FornitoreModelAdmin, self).save_related(request, form, formsets, change)

    #Memorizza utente che apre la pratica
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()



#CLIENTI
@admin.register(Cliente)
class ClienteModelAdmin(ImportExportModelAdmin):
    model = Cliente
    list_display = ['codiceID','denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'creato', 'user']
    fields     = ['denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'PEC', 'fatturaElettronica', 'referente',
                  'emailReferente', 'telefonoReferente']
    search_fields = ['codiceID', 'denominazione', 'citta','provincia', 'picf', 'telefono', 'email', 'PEC', 'fatturaElettronica', 'referente',
                  'emailReferente', 'telefonoReferente']
    resource_class = ClienteResource
    list_per_page = 30


    def response_add(self, request, obj, post_url_continue=None):
        if obj.PEC == None and obj.fatturaElettronica == None:
            Cliente.objects.filter(id=obj.id).delete()
            messages.add_message(request, messages.ERROR, 'ATTENZIONE : devi inserire la PEC o il Cod. UNIVOCO')
            return redirect('/main/cliente/add/')

        return redirect('/main/cliente/')

    def save_related(self, request, form, formsets, change):
        generaCodice(Cliente, "C")
        return super(ClienteModelAdmin, self).save_related(request, form, formsets, change)

    #Memorizza utente che apre la pratica
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()
