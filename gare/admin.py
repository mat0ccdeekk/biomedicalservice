from django.contrib import admin
from .models import GaraPubblica, AltriFile, Lotto
from django.forms import ModelForm, Textarea, Form
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
# Register your models here.
#
class LottoModelForm(ModelForm):
    class Meta:
        model = Lotto
        exclude = []
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label= ("Aggiungi file multipli"),
        required=False,
    )

class LottoModelAdmin(admin.StackedInline):
    model = Lotto
    form = LottoModelForm
    # formset = RequiredInlineFormSet
    extra = 0

class FileModelAdmin(admin.StackedInline):
    model = AltriFile
    extra = 0

@admin.register(GaraPubblica)
class GaraPubblicaModelAdmin(admin.ModelAdmin):
    inlines = [ FileModelAdmin, LottoModelAdmin]
    model = GaraPubblica
    list_display = ['idGara', 'amministrazione', 'oggetto',  'stato', 'importoLotti', 'vendita', 'ultimaModifica' ,'user']
    fields = ['idGara', 'amministrazione', 'oggetto', 'stato', 'vendita',]
    search_fields = ['idGara', 'amministrazione__denominazione', 'oggetto',  'stato', 'importoLotti',
                    'vendita', 'ultimaModifica' ,'user__username', 'user__email']


# @admin.register(Lotto)
# class LottoModelAdmin(admin.ModelAdmin):
#     models = Lotto
#     form = LottoModelForm
#     fields = ['codiceLotto', 'offerta', 'preventivoFile', 'importo', 'file']
#     search_fields = ['codiceLotto', 'importo']
#     form = LottoModelForm
#
#     def save_model(self, request, obj, form, change):
#         files = request.FILES.getlist('file')
#         for f in files:
#             instance=File(files=f)
#             instance.save()
#         return super(LottoModelAdmin, self).save_model(request, obj, form, change)
