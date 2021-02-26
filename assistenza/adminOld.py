from django.contrib import admin
from django.forms import ModelForm, Textarea, Form
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from assistenza.models import Verifica, Riparazione, Prodotti, normativaCodice
from django.shortcuts import redirect, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.db.models import Q
from django.contrib import messages
import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from import_export.admin import  ImportExportModelAdmin
from .resources import  ProdottiResource
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

    # def clean(self):
    #     cleaned_data = super(VerificaModelForm, self).clean()
    #     # if cleaned_data['richiestaFile']:
    #         # print("Abbiamo ancora il file "+str(cleaned_data['richiestaFile']))
    #     return cleaned_data

    def clean_richiestaFile(self):
        index = int(self.cleaned_data['stato'])
        if index == 0 and self.cleaned_data['richiestaFile']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo,  modifica i dati')
        return self.cleaned_data['richiestaFile']

    def clean_preventivoFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 2 and self.cleaned_data['preventivoFile']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        return self.cleaned_data['preventivoFile']

    def clean_verificaElettrica(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['verificaElettrica']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['verificaElettrica']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['verificaElettrica']

    def clean_verificaFunzionale(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['verificaFunzionale']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        return self.cleaned_data['verificaFunzionale']


    def clean_RIT(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['RIT']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['RIT']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['RIT']

    def clean_dataVerifica(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['dataVerifica']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['dataVerifica']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['dataVerifica']

    def clean_cei(self):
        index = int(self.cleaned_data['stato'])
        if index < 3 and self.cleaned_data['cei']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 3 and not self.cleaned_data['cei']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        elif len(self.cleaned_data['cei']) > 3:
            raise forms.ValidationError('Non si possono selezionare più di 2 codici')
        return self.cleaned_data['cei']

    def clean_outputStrumentoFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 4 and self.cleaned_data['outputStrumentoFile']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 4 and not self.cleaned_data['outputStrumentoFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['outputStrumentoFile']

    def clean_schedaFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 5 and self.cleaned_data['schedaFile']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 5 and not self.cleaned_data['schedaFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['schedaFile']

    def clean_fatturaFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 5 and self.cleaned_data['fatturaFile']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 5 and not self.cleaned_data['fatturaFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['fatturaFile']


    def clean_ricevutaPagamentoFile(self):
        index = int(self.cleaned_data['stato'])
        if index < 6 and self.cleaned_data['ricevutaPagamentoFile']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 6 and not self.cleaned_data['ricevutaPagamentoFile']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['ricevutaPagamentoFile']


    def clean_tipoPagamento(self):
        index = int(self.cleaned_data['stato'])
        if index < 6 and self.cleaned_data['tipoPagamento']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 6 and not self.cleaned_data['tipoPagamento']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['tipoPagamento']


    def clean_prezzo(self):
        index = int(self.cleaned_data['stato'])
        if index < 6 and self.cleaned_data['prezzo']:
            raise forms.ValidationError('Lo stato '+Verifica.stato_verifica[index][1]+' non prevede questo campo, modifica i dati')
        elif index >= 6 and not self.cleaned_data['prezzo']:
            raise forms.ValidationError('Campo obbligatorio per lo stato '+Verifica.stato_verifica[index][1])
        return self.cleaned_data['prezzo']


    def clean_noteFinali(self):
        index = int(self.cleaned_data['stato'])
        if index < 7 and self.cleaned_data['noteFinali']:
            raise forms.ValidationError('Ancora non dovresti mettere le note finali')
        return self.cleaned_data['noteFinali']



class VerificaModelAdmin(admin.ModelAdmin):
    model = Verifica
    form = VerificaModelForm
    readonly_fields = ()
    ordering = ('-ultimaModifica',)
    fields = ['cliente', 'stato', 'noteIniziali', 'richiestaFile', 'preventivoFile', 'prodotti' ,'RIT', 'dataVerifica', 'verificaElettrica', 'verificaFunzionale',
               'cei', 'outputStrumentoFile',  'schedaFile', 'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'prezzo', 'noteFinali']
    list_display = ['codiceID', 'cliente', 'stato', 'dataVerifica', 'verificaElettrica', 'verificaFunzionale',
                    'RIT', 'prezzo', 'ultimaModifica', 'user']
    search_fields = ['codiceID', 'cliente__denominazione', 'dataVerifica','stato', 'verificaElettrica', 'verificaFunzionale', 'cei',
                     'RIT', 'prezzo', 'user', 'noteIniziali', 'richiestaFile', 'preventivoFile', 'outputStrumentoFile',
                     'schedaFile', 'fatturaFile', 'ricevutaPagamentoFile', 'noteFinali', 'tipoPagamento']


    #Aggiunta orari
    def get_form(self, request, obj=None, **kwargs):
        orari = ['creatoIniziale', 'richiesta', 'preventivo', 'eseguita', 'elaborazione', 'inviata', 'pagato', 'consegnato', 'chiuso']
        self.fields = ['cliente', 'stato', 'noteIniziali', 'richiestaFile', 'preventivoFile', 'prodotti' ,'RIT', 'dataVerifica', 'verificaElettrica', 'verificaFunzionale',
                   'cei', 'outputStrumentoFile',  'schedaFile', 'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'prezzo', 'noteFinali']

        if obj != None:
            if obj.stato == '8':
                if request.user != 'admin':
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
                self.fields += orari[0:7]
            elif obj.stato == "8":
                self.fields += orari[:]
        return super(VerificaModelAdmin, self).get_form(request, obj=None, **kwargs)

    #Controllo sullo stato iniziale
    # def response_add(self, request, obj, post_url_continue=None):
        # msg = 'Impossibile salvare la verifica , non hai inserito i campi :'
        # msg1 = 'Impossibile salvare la verifica , lo stato '+obj.stato+' non prevede i campi :'
        # stati = ['eseguita', 'elaborazione', 'inviata', 'pagato', 'consegnato' , 'chiuso']
        #
        # statiAllPlus = ['creatoIniziale', 'richiesta', 'preventivo', 'preventivo', 'preventivo', 'preventivo', 'preventivo', 'eseguita',
        #                 'elaborazione', 'elaborazione', 'inviata', 'inviata', 'inviata', 'inviata']
        # nome = [' Richiesta -', ' Preventivo -', ' RIT -',  ' Data verifica -', ' Verifica elettrica -', ' Verifica funzionale -', ' Output strumento -',
        #             ' Scheda -', ' Fattura -', ' Ricevuta pagamento -', ' Tipo pagamento -', ' Note finali -', ' Prezzo -']
        # campi = ['richiestaFile', 'preventivoFile', 'RIT_id', 'dataVerifica',  'verificaElettrica',  'verificaFunzionale',  'outputStrumentoFile', 'schedaFile',
        #           'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento', 'noteFinali', 'prezzo']
        #
        # verifica = Verifica.objects.filter(id=obj.id)
        # for v in verifica :
        #     cei = v.cei.all()
        #
        # dato = Verifica.objects.filter(id=obj.id).values()
        # x = 1
        # for el in campi:
        #     if dato[0][el] != '' and dato[0][el] != None and dato[0][el] != 0 and dato[0]['stato'] in statiAllPlus[0:x]:
        #         msg1 += nome[x-1]
        #     x = x+1
        #
        # if cei and obj.stato in statiAllPlus[0:3]:
        #     v.cei.clear()
        #     msg1 += ' CEI -'
        #
        # if not msg1.endswith(":"):
        #     Verifica.objects.filter(id=obj.id).delete()
        #     messages.add_message(request, messages.ERROR, msg1)
        #     return redirect('/assistenza/verifica/add/')
        #
        # if obj.stato in stati:
        #
        #     if obj.RIT == None and obj.stato in stati[:]:
        #         msg += ' RIT - '
        #
        #     if not cei and obj.stato in stati[:]:
        #         msg += ' CEI - '
        #
        #     if obj.dataVerifica == None and obj.stato in stati[:]:
        #         msg += ' data verifica - '
        #
        #     if obj.verificaElettrica == 0 and obj.stato in stati[:] :
        #         msg += ' Verifiche elettriche - '
        #
        #     if obj.outputStrumentoFile == None and obj.stato in stati[1:] :
        #         msg += ' Output strumento - '
        #
        #     if obj.schedaFile == None and obj.stato in stati[2:] :
        #         msg += ' Scheda file - '
        #
        #     if obj.fatturaFile == None and obj.stato in stati[2:] :
        #         msg += ' Fattura - '
        #
        #     if obj.prezzo <= 0 and obj.stato in stati[2:] :
        #         msg += ' Importo '
        #
        #     if obj.tipoPagamento == None and obj.stato in stati[2:] :
        #         msg += ' seleziona il tipo di pagamento'
        #
        # if not msg.endswith(":"):
        #     Verifica.objects.filter(id=obj.id).delete()
        #     messages.add_message(request, messages.ERROR, msg)
        #     return redirect('/assistenza/verifica/add/')

        # return redirect('/assistenza/verifica/')



    #Modifica stato e memorizza data
    # @receiver(pre_save, sender=Verifica)
    # def cambioStato(sender, instance, **kwargs):
    #     statiAll = ['creatoIniziale', 'richiesta', 'preventivo', 'eseguita', 'elaborazione', 'inviata', 'pagato', 'consegnato' , 'chiuso']
    #     current = instance
    #     current.flag = False
    #     current.tornaIndietro = False
    #     verifica = Verifica.objects.filter(id=instance.id)
    #     for v in verifica :
    #         cei = v.cei.all()
    #
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
    #             print("previus "+str(previus.stato))
    #             print("current "+str(current.stato))
    #             if not current.tornaIndietro:
    #                 current.statoX = current.stato
    #
    #                 if current.stato == 'richiesta':
    #                     current.richiesta = datetime.datetime.today()
    #                     current.ultimaModifica = datetime.datetime.today()
    #
    #                 if current.stato == 'preventivo':
    #                     current.preventivo = datetime.datetime.today()
    #
    #                 if current.stato == 'eseguita':
    #                     if current.RIT == '' or current.verificaElettrica == 0  or current.dataVerifica == None:
    #
    #                         current.flag = True
    #                         current.stato = previus.stato
    #                     else:
    #                         current.eseguita = datetime.datetime.today()
    #                         current.ultimaModifica = datetime.datetime.today()
    #
    #                 if current.stato == 'elaborazione':
    #                     if current.RIT == '' or current.verificaElettrica == 0  or current.outputStrumentoFile == '' or current.dataVerifica == None:
    #                         current.flag = True
    #                         current.stato = previus.stato
    #                     else:
    #                         current.elaborazione = datetime.datetime.today()
    #                         current.ultimaModifica = datetime.datetime.today()
    #
    #
    #                 if current.stato == 'inviata':
    #                     print("inviata pre")
    #                     if current.RIT == '' or current.verificaElettrica == 0 or current.outputStrumentoFile == '' or current.schedaFile == '' or current.fatturaFile == '' or current.dataVerifica == None:
    #                     # current.schedaFile == '' or current.fatturaFile == '':
    #                         current.flag = True
    #                         current.stato = previus.stato
    #                         print("inviata  ")
    #                     else:
    #                         current.inviata = datetime.datetime.today()
    #                         current.ultimaModifica = datetime.datetime.today()
    #
    #
    #                 if current.stato == 'pagato':
    #                     if current.RIT == '' or current.verificaElettrica == 0 or current.outputStrumentoFile == '' or current.schedaFile == '' or current.fatturaFile == '' or current.prezzo == 0 or current.dataVerifica == None or current.tipoPagamento == None:
    #                         current.flag = True
    #                         current.stato = previus.stato
    #                     else:
    #                         current.pagato = datetime.datetime.today()
    #                         current.ultimaModifica = datetime.datetime.today()
    #
    #
    #                 if current.stato == 'consegnato':
    #                     if current.RIT == '' or current.verificaElettrica == 0  or current.outputStrumentoFile == '' or current.schedaFile == '' or current.fatturaFile == '' or current.prezzo == 0 or current.dataVerifica == None or current.tipoPagamento == None:
    #                         current.flag = True
    #                         current.stato = previus.stato
    #                     else:
    #                         current.consegnato = datetime.datetime.today()
    #                         current.ultimaModifica = datetime.datetime.today()
    #
    #                 if current.stato == 'chiuso':
    #                     if current.RIT == '' or current.verificaElettrica == 0  or current.outputStrumentoFile == '' or current.schedaFile == '' or current.fatturaFile == '' or current.prezzo == 0 or current.dataVerifica == None or current.tipoPagamento == None:
    #                         current.flag = True
    #                         current.stato = previus.stato
    #                     else:
    #                         current.chiuso = datetime.datetime.today()
    #                         current.ultimaModifica = datetime.datetime.today()
    #                         # ('attivo','Attivo'),
    #                         # ('in scadenza','In scadenza'),
    #                          # ('scaduto','Scaduto'),
    #                         durata = 24
    #                         if current.stato == 'chiuso' and cei and current.dataVerifica != None:
    #                             dToday = datetime.date.today()
    #                             dVerifica = current.dataVerifica
    #                             mesi = months(dToday, dVerifica)
    #                             gToday = str(dToday)[-2:]
    #                             gVerifica = str(dVerifica)[-2:]
    #                             giorni = int(gVerifica) - int(gToday)
    #                             for c in cei:
    #                                 if str(c) == '62-5' or str(c) == '62-13':
    #                                     durata = 12
    #                             t = durata - mesi
    #
    #                             if t < 0 or ( t == 0 and giorni <= 0):
    #                                 statoScadenza = 'scaduto'
    #                             elif 0 < t <= 2 or ( t == 0 and giorni > 0):
    #                                 statoScadenza = 'in scadenza'
    #                             else:
    #                                 statoScadenza = 'attivo'
    #                             Verifica.stato_verifica.append((statoScadenza,statoScadenza))
    #                             current.stato = statoScadenza


    #Controllo errori in modifcica
    # def response_change(self, request, obj):
        # msg = 'Impossibile cambiare lo stato,  completa i campi :'
        # msg1 = 'Impossibile salvare la verifica , lo stato '+str(obj.stato)+' non prevede i campi :'
        # msg2 = '<br>Non puoi tornare in uno stato precedente'
        # stati = ['eseguita', 'elaborazione', 'inviata', 'pagato', 'consegnato' , 'chiuso']
        # statiAll = ['creatoIniziale', 'richiesta', 'preventivo', 'eseguita', 'elaborazione', 'inviata', 'pagato', 'consegnato' , 'chiuso']
        #
        # verifica = Verifica.objects.filter(id=obj.id)
        #
        # for v in verifica :
        #     cei = v.cei.all()
        #     prodotti = v.prodotti.all()
        #
        # if not obj.flag:
        #
        #     for v1 in verifica:
        #
        #         if v1.richiestaFile != '' and v1.stato in statiAll[0:1] :
        #             v1.richiestaFile = ''
        #             msg1 += ' Richiesta - '
        #         if v1.preventivoFile != '' and v1.stato in statiAll[0:2] :
        #             v1.preventivoFile = ''
        #             msg1 += ' Preventivo - '
        #         if v1.RIT  and v1.stato in statiAll[0:3] :
        #             v1.RIT = None
        #             msg1 += ' RIT -'
        #         if cei and v1.stato in statiAll[0:3]:
        #             v1.cei.clear()
        #             msg1 += ' CEI -'
        #         if v1.dataVerifica  and v1.stato in statiAll[0:3] :
        #             v1.dataVerifica = None
        #             msg1 += ' Data verifica -'
        #         if v1.verificaElettrica  and v1.stato in statiAll[0:3] :
        #             v1.verificaElettrica = 0
        #             msg1 += ' Verifica elettrica -'
        #
        #         if v1.verificaFunzionale  and v1.stato in statiAll[0:3] :
        #             v1.verificaFunzionale = 0
        #             msg1 += 'Verifica funzionale -'
        #
        #         if v1.outputStrumentoFile != '' and v1.stato in statiAll[0:4] :
        #             v1.outputStrumentoFile = ''
        #             msg1 += ' Output strumento -'
        #
        #         if v1.schedaFile != '' and v1.stato in statiAll[0:5] :
        #             v1.schedaFile = ''
        #             msg1 += ' Scheda -'
        #
        #         if  v1.fatturaFile != '' and v1.stato in statiAll[0:5] :
        #             v1.fatturaFile = ''
        #             msg1 += ' Fattura -'
        #
        #         if v1.ricevutaPagamentoFile != '' and v1.stato in statiAll[0:6] :
        #             v1.ricevutaPagamentoFile = ''
        #             msg1 += ' Ricevuta pagamento-'
        #
        #         if v1.tipoPagamento != None  and v1.stato in statiAll[0:6] :
        #             v1.tipoPagamento = None
        #             msg1 += ' Tipo pagamento -'
        #
        #         if v1.noteFinali != None and v1.stato in statiAll[0:6] :
        #             v1.noteFinali = None
        #             msg1 += ' Note finali non ammesse -'
        #
        #         if v1.prezzo != 0  and v1.stato in statiAll[0:6] :
        #             v1.prezzo = 0
        #             msg1 += ' Prezzo '
        #
        #         v1.save()
        #
        #
        # if not msg1.endswith(":"):
        #     if obj.tornaIndietro:
        #         msg1 += msg2
        #     messages.error(request, mark_safe(msg1))
        #     return redirect('/assistenza/verifica/'+str(obj.id)+'/change/')
        #
        # if obj.flag:
        #
        #     if obj.statoX in stati:
        #
        #         if obj.RIT == None and obj.statoX in stati[:]:
        #
        #             msg += ' RIT - '
        #
        #         if obj.dataVerifica == None and obj.statoX in stati[:] :
        #             msg += ' Data verifica - '
        #
        #         if obj.verificaElettrica == 0 and obj.statoX in stati[:] :
        #             msg += ' Verifiche elettriche - '
        #
        #         if obj.outputStrumentoFile == '' and obj.statoX in stati[1:] :
        #             msg += ' Output strumento - '
        #
        #         if obj.schedaFile == '' and obj.statoX in stati[2:] :
        #             msg += ' Scheda file - '
        #
        #         if obj.fatturaFile == '' and obj.statoX in stati[2:] :
        #             msg += ' Fattura - '
        #
        #         if obj.prezzo <= 0 and obj.statoX in stati[3:] :
        #             msg += ' Importo '
        #
        #         if obj.tipoPagamento == None and obj.statoX in stati[3:] :
        #             msg += ' - seleziona il tipo di pagamento'
        #
        # if not cei and obj.stato in stati[:]:
        #     msg += ' - CEI - '
        #
        # if not msg.endswith(":"):
        #     if obj.tornaIndietro:
        #         msg += msg2
        #     messages.error(request, mark_safe(msg))
        #     return redirect('/assistenza/verifica/'+str(obj.id)+'/change/')
        #
        # if obj.tornaIndietro:
        #     messages.error(request, mark_safe(msg2))
        #     return redirect('/assistenza/verifica/'+str(obj.id)+'/change/')
        #
        # return redirect('/assistenza/verifica/')


    #Prezzo totale
    # def get_queryset(self, request):
    #     prezzoTot = 0
    #     verifica = super(VerificaModelAdmin, self).get_queryset(request)
    #     querySet = verifica.filter(Q(stato='attivo') | Q(stato = 'in scadenza'))
    #
    #     durata = 24
    #     for sq in querySet:
    #         dToday = datetime.date.today()
    #         dVerifica = sq.dataVerifica
    #         mesi = months(dToday, dVerifica)
    #         gToday = str(dToday)[-2:]
    #         gVerifica = str(dVerifica)[-2:]
    #         giorni = int(gVerifica) - int(gToday)
    #         for c in sq.cei.all():
    #             if str(c) == '62-5' or str(c) == '62-13':
    #                 durata = 12
    #         t = durata - mesi
    #         if t < 0 or ( t == 0 and giorni <= 0):
    #             statoScadenza = 'scaduto'
    #         elif 0 < t <= 2 or ( t == 0 and giorni > 0):
    #             statoScadenza = 'in scadenza'
    #         else:
    #             statoScadenza = 'attivo'
    #         Verifica.stato_verifica.pop()
    #         Verifica.stato_verifica.append(statoScadenza,statoScadenza)
    #         qs.stato = statoScadenza
    #
    #     for a in verifica.all():
    #         prezzoTot += a.prezzo
    #     return verifica

    #Memorizza utente che apre la pratica e orario del primo stato
    # def save_model(self, request, obj, form, change):
    #     if not obj.user:
    #         obj.user = request.user
    #         if obj.stato == 'creatoIniziale':
    #             obj.creatoIniziale = datetime.datetime.today()
    #         if obj.stato == 'richiesta':
    #             obj.richiesta = datetime.datetime.today()
    #         if obj.stato == 'preventivo':
    #             obj.preventivo = datetime.datetime.today()
    #         if obj.stato == 'ordinato':
    #             obj.ordinato = datetime.datetime.today()
    #         if obj.stato == 'spedito':
    #             obj.spedito = datetime.datetime.today()
    #         if obj.stato == 'ricevuto':
    #             obj.ricevuto = datetime.datetime.today()
    #         if obj.stato == 'pagato':
    #             obj.pagato = datetime.datetime.today()
    #         if obj.stato == 'chiuso':
    #             obj.chiuso = datetime.datetime.today()
    #     obj.ultimaModifica = datetime.datetime.today()
    #     obj.save()

    #genera codice
    def save_related(self, request, form, formsets, change):
        generaCodice(Verifica, "AT")
        return super(VerificaModelAdmin, self).save_related(request, form, formsets, change)


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
    list_display = ['codiceID', 'cliente', 'stato', 'ultimaModifica' , 'prezzo', 'user',]
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
