from import_export import resources
from .models import  Prodotti, Verifica


class ProdottiResource(resources.ModelResource):
    class Meta:
        model = Prodotti
        skip_unchanged = True
        report_skipped = True
        exclude = ('id',)
        import_id_fields = ['codiceProdotto', 'tipo', 'costruttore', 'modello', 'numeroSerie', 'classe']

class VerificaResource(resources.ModelResource):
    class Meta:
        model = Verifica
        skip_unchanged = True
        report_skipped = True
        exclude = ('id', 'flag', 'statoX','tornaIndietro')
        import_id_fields = ['codiceID', 'cliente__denominazione', 'stato', 'ultimaModifica', 'prodotti', 'noteIniziali',
                            'richiestaFile', 'preventivoFile', 'RIT', 'dataVerifica', 'verificaElettrica', 'verificaFunzionale',
                            'cei', 'outputStrumentoFile', 'schedaFile', 'fatturaFile', 'ricevutaPagamentoFile', 'tipoPagamento',
                            'prezzo', 'noteFinali', 'creatoIniziale',
                            'richiesta' ,'preventivo' ,'eseguita','elaborazione','inviata','pagato','consegnato','chiuso','user']
