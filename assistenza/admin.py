from django.contrib import admin
from django.forms import ModelForm, Textarea, Form
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from assistenza.models import Verifica, Riparazione, Prodotti, normativaCodice
from main.models import Rapporti
from django.shortcuts import redirect, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib import messages
import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from import_export.admin import  ImportExportModelAdmin
from .resources import  ProdottiResource, VerificaResource
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here.

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
    codice = sigla+' '+str(year)+' '+zeri+str(key)
    Modello.objects.filter(pk=str(key)).update(codiceID=codice)

def months(d1, d2):
    return d1.month - d2.month + 12*(d1.year - d2.year)

#VERIFICA
class VerificaModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(VerificaModelForm, self).__init__(*args, **kwargs)
        #visualizza solo i RIT non usati
        self.fields['RIT'].queryset = Rapporti.objects.filter(Q(verifica__isnull=True)|Q(verifica=self.instance))

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            if int(kwargs['instance'].stato) < 8 :
                self.fields['stato'].choices = Verifica.stato_verifica
            else:
                self.fields['stato'].choices = Verifica.stato_scadenza
                self.fields['stato'].disabled = True
        else:
            self.fields['stato'].choices = Verifica.stato_verifica

    stato = forms.ChoiceField(choices=(), required=True, )
    verificaElettrica = forms.IntegerField(required=False, label='Verifica elettrica', min_value=0, )
    verificaFunzionale = forms.IntegerField(required=False, label='Verifica funzionale', min_value=0, )
    dataVerifica = forms.DateField(required=False, label='Data verifica', widget=AdminDateWidget)

    class Meta:
        model = Verifica
        exclude = []
        widgets = {
                'noteIniziali': Textarea(attrs={'cols': 50, 'rows': 6}),
                'noteFinali': Textarea(attrs={'cols': 50, 'rows': 6}),
        }

    def save(self, commit=True):
        instance = super(VerificaModelForm, self).save(commit=False)
        instance.ultimaModifica = datetime.datetime.today()

        if instance.stato == '0' and not instance.creatoIniziale:
            instance.creatoIniziale = datetime.datetime.today()
        if instance.stato == '1' and not instance.richiesta:
            instance.richiesta = datetime.datetime.today()
        if instance.stato == '2' and not instance.preventivo:
            instance.preventivo = datetime.datetime.today()
        if instance.stato == '3' and not instance.eseguita:
            instance.eseguita = datetime.datetime.today()
        if instance.stato == '4' and not instance.elaborazione:
            instance.elaborazione = datetime.datetime.today()
        if instance.stato == '5' and not instance.inviata:
            instance.inviata = datetime.datetime.today()
        if instance.stato == '6' and not instance.pagato:
            instance.pagato = datetime.datetime.today()
        if instance.stato == '7' and not instance.consegnato:
            instance.consegnato = datetime.datetime.today()
        if instance.stato == '8' and not instance.chiuso:
            instance.chiuso = datetime.datetime.today()

        if commit:
            instance.save()
        return instance

    def clean_richiestaFile(self):
        index = int(self.cleaned_data['stato'])
        if index == 0 and self.cleaned_data['richiestaFile']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo,  modifica i dati')
        return self.cleaned_data['richiestaFile']

    def clean_preventivoFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 2 and self.cleaned_data['preventivoFile']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        return self.cleaned_data['preventivoFile']

    def clean_verificaElettrica(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['verificaElettrica']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['verificaElettrica']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['verificaElettrica']

    def clean_verificaFunzionale(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['verificaFunzionale']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        return self.cleaned_data['verificaFunzionale']

    def clean_RIT(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['RIT']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['RIT']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['RIT']

    def clean_dataVerifica(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['dataVerifica']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['dataVerifica']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['dataVerifica']

    def clean_cei(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['cei']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['cei']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        elif len(self.cleaned_data['cei']) >= 3:
            raise forms.ValidationError('Non si possono selezionare più di 2 codici')
        return self.cleaned_data['cei']

    def clean_outputStrumentoFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 4 and self.cleaned_data['outputStrumentoFile']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 4 and not self.cleaned_data['outputStrumentoFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['outputStrumentoFile']

    def clean_schedaFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 5 and self.cleaned_data['schedaFile']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 5 and not self.cleaned_data['schedaFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['schedaFile']

    def clean_fatturaFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 5 and self.cleaned_data['fatturaFile']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 5 and not self.cleaned_data['fatturaFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['fatturaFile']


    def clean_ricevutaPagamentoFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 6 and self.cleaned_data['ricevutaPagamentoFile']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 6 and not self.cleaned_data['ricevutaPagamentoFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['ricevutaPagamentoFile']


    def clean_tipoPagamento(self):
        index = int(self.cleaned_data['stato'])
        if index < 6 and self.cleaned_data['tipoPagamento']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 6 and not self.cleaned_data['tipoPagamento']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['tipoPagamento']


    def clean_prezzo(self):
        index = int(self.cleaned_data['stato'])
        if index < 6 and self.cleaned_data['prezzo']:
            raise forms.ValidationError('Lo stato '+self.fields['stato'].choices[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 6 and not self.cleaned_data['prezzo']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+self.fields['stato'].choices[index][1])
        return self.cleaned_data['prezzo']


    def clean_noteFinali(self):
        index = int(self.cleaned_data['stato'])
        if index < 7 and self.cleaned_data['noteFinali']:
            raise forms.ValidationError('Ancora non dovresti mettere le note finali')
        return self.cleaned_data['noteFinali']


class VerificaModelAdmin(ImportExportModelAdmin):
    resource_class = VerificaResource
    model = Verifica
    form = VerificaModelForm
    readonly_fields = ()
    ordering = ('-ultimaModifica',)
    fields = ['cliente', 'stato', 'noteIniziali', 'richiestaFile', 'preventivoFile', 'prodotti' ,'RIT', 'dataVerifica', 'verificaElettrica', 'verificaFunzionale',
               'cei', 'outputStrumentoFile',  'schedaFile', 'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'prezzo', 'noteFinali']
    list_display = ['codiceID', 'cliente', 'STATO', 'dataVerifica', 'verificaElettrica', 'verificaFunzionale', 'CEI',
                    'RIT', 'prezzo', 'ultimaModifica', 'user']
    search_fields = ['codiceID', 'cliente__denominazione', 'dataVerifica','stato', 'verificaElettrica', 'verificaFunzionale',
                    'cei__choice', 'RIT__codiceID', 'RIT__RIT', 'user__username', 'user__email', 'prezzo','noteIniziali', 'richiestaFile', 'preventivoFile', 'outputStrumentoFile',
                     'schedaFile', 'fatturaFile', 'ricevutaPagamentoFile', 'noteFinali', 'tipoPagamento']


    #genera codice
    def save_related(self, request, form, formsets, change):
        generaCodice(Verifica, "AT")
        return super(VerificaModelAdmin, self).save_related(request, form, formsets, change)

    # Memorizza utente che apre la pratica
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

    #Aggiunta orari
    def get_form(self, request, obj=None, **kwargs):
        orari = ['creatoIniziale', 'richiesta', 'preventivo', 'eseguita', 'elaborazione', 'inviata', 'pagato', 'consegnato', 'chiuso']
        self.fields = ['cliente', 'stato', 'noteIniziali', 'richiestaFile', 'preventivoFile', 'prodotti' ,'RIT', 'dataVerifica', 'verificaElettrica', 'verificaFunzionale',
                   'cei', 'outputStrumentoFile',  'schedaFile', 'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'prezzo', 'noteFinali']

        if obj != None:
            if obj.stato == '8':
                if str(request.user) != 'admin':
                    self.readonly_fields = tuple(self.fields) + tuple(orari)
            if obj.stato == "0":
                self.fields += orari[0:1]
            elif obj.stato == "1":
                self.fields +=  orari[0:2]
            elif obj.stato == "2":
                self.fields += orari[0:3]
            elif obj.stato == "3":
                self.fields +=  orari[0:4]
            elif obj.stato == "4":
                self.fields +=  orari[0:5]
            elif obj.stato == "5":
                self.fields += orari[0:6]
            elif obj.stato == "6":
                self.fields += orari[0:7]
            elif obj.stato == "7":
                self.fields += orari[0:8]
            elif obj.stato == "8":
                self.fields += orari[:]
            elif obj.stato == "9":
                self.fields += orari[:]
            elif obj.stato == "10":
                self.fields += orari[:]
            elif obj.stato == "11":
                self.fields += orari[:]
        return super(VerificaModelAdmin, self).get_form(request, obj=None, **kwargs)


    #Prezzo totale
    def get_queryset(self, request):
        prezzoTot = 0
        verifica = super(VerificaModelAdmin, self).get_queryset(request)
        querySet = verifica.filter(Q(stato='8') | Q(stato='9') | Q(stato = '10') | Q(stato = '11'))
        stato_verifica =[
                ('0', 'Pratica creata'),
                ('1', 'Richiesta'),
                ('2', 'Preventivo'),
                ('3','Eseguito'),
                ('4','Elaborazione'),
                ('5','Inviate'),
                ('6','Pagato'),
                ('7','Consegnato'),
                ('8','Chiuso')
            ]
        durata = 24
        for sq in querySet:
            # print("STATO query set "+str(sq.stato)+" data "+str(sq.dataVerifica))
            dToday = datetime.date.today()
            dVerifica = sq.dataVerifica
            mesi = months(dToday, dVerifica)
            gToday = str(dToday)[-2:]
            gVerifica = str(dVerifica)[-2:]
            giorni = int(gVerifica) - int(gToday)
            for c in sq.cei.all():
                if '62-5' in str(c)  or '62-13' in str(c):
                    durata = 12
            t = durata - mesi
            if t < 0 or ( t == 0 and giorni <= 0):
                statoScadenza = 11
            elif 0 < t <= 2 or ( t == 0 and giorni > 0):
                statoScadenza = 10
            else:
                statoScadenza = 9
            # sq.stato = statoScadenza
            # Verifica.stato_verifica.append((statoScadenza,statoScadenza))
            # print("nuovo stato "+str(statoScadenza)+" tempo "+str(t)+" tempo cei "+str(durata))
            verifica.filter(id=sq.id).update(stato=statoScadenza)
            # sq.save()
        return verifica

    #Controllo sullo stato iniziale
    # def response_add(self, request, obj, post_url_continue=None):
        # return redirect('/assistenza/verifica/')

    #Controllo errori in modifcica
    # def response_change(self, request, obj):
    #     if obj.tornaIndietro:
    #         messages.error(request, mark_safe("Non puoi tornare in uno stato precedente"))
    #         return redirect('/assistenza/verifica/'+str(obj.id)+'/change/')
    #     return redirect('/assistenza/verifica/')


    #Modifica stato e memorizza data
    # @receiver(pre_save, sender=Verifica)
    # def cambioStato(sender, instance, **kwargs):
    #     statiAll = ['creatoIniziale', 'richiesta', 'preventivo', 'eseguita', 'elaborazione', 'inviata', 'pagato', 'consegnato' , 'chiuso']
    #     current = instance
    #     current.tornaIndietro = False
    #     verifica = Verifica.objects.filter(id=instance.id)
    #
    #     if Verifica.objects.filter(id=instance.id):
    #         previus = Verifica.objects.get(id=instance.id)
    #
    #         if previus.stato != current.stato:
    #             #tornare in uno stato precedente
    #             i = statiAll.index(previus.stato)
    #             for x in range(0, i):
    #                 if current.stato == statiAll[x]:
    #                     current.tornaIndietro = True
    #                     current.stato = previus.stato



#RIPARAZIONI
class RiparazioneModelForm(ModelForm):

    class Meta:
        model = Riparazione
        exclude = []
        widgets = {
                'noteIniziali': Textarea(attrs={'cols': 50, 'rows': 6}),
                'noteFinali': Textarea(attrs={'cols': 50, 'rows': 6}),
                 }

class RiparazioneModelAdmin(admin.ModelAdmin):
    model = Riparazione
    form = RiparazioneModelForm
    readonly_fields = ()
    ordering = ('-ultimaModifica',)
    list_display = ['codiceID', 'cliente', 'get_stato_display', 'ultimaModifica' , 'prezzo', 'user',]
    search_fields = ['codiceID', 'cliente__denominazione', 'stato', 'prezzo', 'user', 'noteIniziali', 'richiestaFile'
                    'preventivoFile', 'autorizzazioneFile', 'RIT', 'verifica', 'fatturaFile', 'ricevutaPagamentoFile']

    fields = ['cliente', 'stato', 'noteIniziali', 'richiestaFile', 'preventivoFile', 'autorizzazioneFile',
              'RIT', 'verifica', 'fatturaFile', 'ricevutaPagamentoFile', 'prezzo']


    #Controllo sullo stato iniziale
    def response_add(self, request, obj, post_url_continue=None):
        msg = 'Impossibile salvare la verifica , non hai inserito i campi :'
        msg1 = 'Impossibile salvare la verifica , lo stato '+obj.stato+' non prevede i campi :'
        stati = ['eseguita', 'verifiche', 'fatturaEmessa', 'pagato' , 'chiuso']

        statiAll = ['creatoIniziale', 'richiesta', 'preventivo', 'autorizzazione', 'eseguita', 'verifiche',
                    'fatturaEmessa', ['pagato' , 'chiuso']]
        nome = ['Richiesta', 'Preventivo', 'Autorizzazione', 'ID rapporti', 'ID Verifiche', 'Fattura','Ricevuta pagamento',
                'Tipo pagamento', 'Prezzo']
        campi = [[obj.richiestaFile], [obj.preventivoFile], [obj.autorizzazioneFile], [obj.RIT], [obj.verifiche],
                 [obj.fatturaFile], [obj.ricevutaPagamentoFile], [obj.tipoPagamento], [obj.prezzo]]

        z = 0

        for x in range(len(campi)):
            for y in range(len(campi[x])):
                if y > 0:
                    z += 1
                if campi[x][y] != None and campi[x][y] != '' and  campi[x][y] != 0:
                    if obj.stato in statiAll[:x+1]:
                        msg1 += ' '+nome[z]+' - '
            z += 1

        if not msg1.endswith(":"):
            Riparazione.objects.filter(id=obj.id).delete()
            messages.add_message(request, messages.ERROR, msg1)
            return redirect('/assistenza/riparazione/add/')

        if obj.stato in stati:

            if obj.RIT == None and obj.stato in stati[:]:
                msg += ' ID RIT - '

            if obj.verifica == None and obj.stato in stati[1:]:
                msg += ' ID verifiche - '

            if obj.fatturaFile == None and obj.stato in stati[2:] :
                msg += ' Fattura - '

            if obj.prezzo <= 0 and obj.stato in stati[3:] :
                msg += ' Importo - '

            if obj.tipoPagamento == None and obj.stato in stati[3:] :
                msg += ' seleziona il tipo di pagamento'

        if not msg.endswith(":"):
            Riparazione.objects.filter(id=obj.id).delete()
            messages.add_message(request, messages.ERROR, msg)
            return redirect('/assistenza/riparazione/add/')

        return redirect('/assistenza/riparazione/')


    #Aggiunta orari
    def get_form(self, request, obj=None, **kwargs):
        self.readonly_fields = ()
        self.fields = ['cliente', 'stato', 'noteIniziali', 'richiestaFile', 'preventivoFile', 'autorizzazioneFile',
                        'RIT', 'verifica', 'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'prezzo']
        orari = ['creatoIniziale', 'richiesta', 'preventivo', 'autorizzazione', 'eseguita', 'verifiche', 'fatturaEmessa', 'pagato', 'chiuso']

        if obj != None:
            if obj.stato == 'chiuso':
                if request.user != 'admin':
                    self.readonly_fields = tuple(self.fields) + tuple(orari)
            if obj.stato == "creatoIniziale":
                self.fields += orari[0:1]
            elif obj.stato == "richiesta":
                self.fields +=  orari[0:2]
            elif obj.stato == "preventivo":
                self.fields += orari[0:3]
            elif obj.stato == "autorizzazione":
                self.fields +=  orari[0:4]
            elif obj.stato == "eseguita":
                self.fields +=  orari[0:5]
            elif obj.stato == "verifiche":
                self.fields += orari[0:6]
            elif obj.stato == "fatturaEmessa":
                self.fields += orari[0:7]
            elif obj.stato == "pagato":
                self.fields += orari[0:7]
            elif obj.stato == "chiuso":
                self.fields += orari[:]
        return super(RiparazioneModelAdmin, self).get_form(request, obj=None, **kwargs)


    #Modifica stato e memorizza data
    @receiver(pre_save, sender=Riparazione)
    def cambioStato(sender, instance, **kwargs):
        current = instance
        current.flag = False

        if Riparazione.objects.filter(id=instance.id):
            previus = Riparazione.objects.get(id=instance.id)
            if previus.stato != current.stato:
                current.statoX = current.stato

                if current.stato == 'richiesta':
                    current.richiesta = datetime.datetime.today()
                    current.ultimaModifica = datetime.datetime.today()

                if current.stato == 'preventivo':
                    current.preventivo = datetime.datetime.today()

                if current.stato == 'autorizzazione':
                    current.autorizzazione = datetime.datetime.today()

                if current.stato == 'eseguita':
                    if current.RIT == None :
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.eseguita = datetime.datetime.today()
                        current.ultimaModifica = datetime.datetime.today()


                if current.stato == 'verifiche':
                    if current.RIT == None or current.verifica == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.elaborazione = datetime.datetime.today()
                        current.ultimaModifica = datetime.datetime.today()


                if current.stato == 'fatturaEmessa':
                    if current.RIT == None or current.verifica == None or current.fatturaFile == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.inviata = datetime.datetime.today()
                        current.ultimaModifica = datetime.datetime.today()


                if current.stato == 'pagato':
                    if current.RIT == None or current.verifica == None or current.fatturaFile == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.pagato = datetime.datetime.today()
                        current.ultimaModifica = datetime.datetime.today()


                if current.stato == 'chiuso':
                    if current.RIT == None or current.verifica == None or current.fatturaFile == None:
                        current.flag = True
                        current.stato = previus.stato
                    else:
                        current.chiuso = datetime.datetime.today()
                        current.ultimaModifica = datetime.datetime.today()


    #Controllo errori in modifcica
    def response_change(self, request, obj):
        msg = 'Impossibile salvare la verifica , non hai inserito i campi :'
        msg1 = 'Impossibile salvare la verifica , lo stato '+obj.stato+' non prevede i campi :'
        stati = ['eseguita', 'verifiche', 'fatturaEmessa', 'pagato' , 'chiuso']

        statiAll = ['creatoIniziale', 'richiesta', 'preventivo', 'autorizzazione', 'eseguita', 'verifiche',
                    'fatturaEmessa', ['pagato' , 'chiuso']]
        nome = ['Richiesta', 'Preventivo', 'Autorizzazione', 'ID rapporti', 'ID Verifiche', 'Fattura','Ricevuta pagamento',
                'Tipo pagamento', 'Prezzo']
        campi = [[obj.richiestaFile], [obj.preventivoFile], [obj.autorizzazioneFile], [obj.RIT], [obj.verifiche],
                 [obj.fatturaFile], [obj.ricevutaPagamentoFile], [obj.tipoPagamento], [obj.prezzo]]

        z = 0

        for x in range(len(campi)):
            for y in range(len(campi[x])):
                if y > 0:
                    z += 1
                if campi[x][y] != None and campi[x][y] != '' and  campi[x][y] != 0:
                    if obj.stato in statiAll[:x+1]:
                        msg1 += ' '+nome[z]+' - '
            z += 1

        if not msg1.endswith(":"):
            Riparazione.objects.filter(id=obj.id).delete()
            messages.add_message(request, messages.ERROR, msg1)
            return redirect('/assistenza/riparazione/add/')

        if obj.flag:

            if obj.statoX in stati:

                if obj.RIT == None and obj.statoX in stati[:]:
                    msg += ' ID RIT - '

                if obj.verifica == None and obj.statoX in stati[1:]:
                    msg += ' ID verifiche - '

                if obj.fatturaFile == None and obj.statoX in stati[2:] :
                    msg += ' Fattura - '

                if obj.prezzo <= 0 and obj.statoX in stati[3:] :
                    msg += ' Importo '

                if obj.tipoPagamento == None and obj.statoX in stati[3:] :
                    msg += ' seleziona il tipo di pagamento'

            if not msg.endswith(":"):
                messages.add_message(request, messages.ERROR, msg)
                return redirect('/assistenza/riparazione/'+str(obj.id)+'/change/')

        return redirect('/assistenza/riparazione/')



    #Prezzo totale
    def get_queryset(self, request):
        prezzoTot = 0
        riparazione = super(RiparazioneModelAdmin, self).get_queryset(request)
        for a in riparazione.all():
            prezzoTot += a.prezzo
        return riparazione

    #Memorizza utente che apre la pratica e orario del primo stato
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
            if obj.stato == 'creatoIniziale':
                obj.creatoIniziale = datetime.datetime.today()
            if obj.stato == 'richiesta':
                obj.richiesta = datetime.datetime.today()
            if obj.stato == 'preventivo':
                obj.preventivo = datetime.datetime.today()
            if obj.stato == 'autorizzazione':
                obj.autorizzazione = datetime.datetime.today()
            if obj.stato == 'eseguita':
                obj.eseguita = datetime.datetime.today()
            if obj.stato == 'verifiche':
                obj.verifiche = datetime.datetime.today()
            if obj.stato == 'fatturaEmessa':
                obj.fatturaEmessa = datetime.datetime.today()
            if obj.stato == 'pagato':
                obj.pagato = datetime.datetime.today()
            if obj.stato == 'chiuso':
                obj.chiuso = datetime.datetime.today()
        obj.ultimaModifica = datetime.datetime.today()
        obj.save()

    #genera codice
    def save_related(self, request, form, formsets, change):
        generaCodice(Riparazione, "AR")
        return super(RiparazioneModelAdmin, self).save_related(request, form, formsets, change)


#PRODOTTI

def generaCodiceProdotto(Modello, sigla):
    m = Modello.objects.all().last()
    key = m.id
    if int(key) < 10:
        zeri = '000'
    elif int(key) < 100 and int(key) >= 10 :
        zeri = '00'
    elif int(key) < 1000 and int(key) >= 100 :
        zeri = '0'
    else:
        zeri = ''
    codice = sigla+' '+zeri+str(key)
    Modello.objects.filter(pk=str(key)).update(codiceProdotto=codice)

class ProdottiModelAdmin(ImportExportModelAdmin):
    resource_class = ProdottiResource
    model = Prodotti
    list_display = ['codiceProdotto', 'cliente', 'tipo','costruttore', 'modello', 'numeroSerie', 'classe',  'creato']
    search_fields = ['cliente__denominazione', 'fornitore__denominazione','codiceProdotto', 'tipo','costruttore',
                     'modello', 'numeroSerie', 'classe', 'cliente__denominazione', 'creato', 'normativa', 'inventario']
    fields = ['cliente', 'fornitore', 'tipo','costruttore', 'modello', 'numeroSerie', 'classe', 'normativa', 'inventario']

    def save_related(self, request, form, formsets, change):
        generaCodiceProdotto(Prodotti, "ST")
        return super(ProdottiModelAdmin, self).save_related(request, form, formsets, change)

admin.site.register(Verifica, VerificaModelAdmin)
admin.site.register(Riparazione, RiparazioneModelAdmin)
admin.site.register(Prodotti, ProdottiModelAdmin)
