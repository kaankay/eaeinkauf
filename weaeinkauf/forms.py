from django import forms
from .models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung, WeaPreis, PreisKondition, WeaFundament, WeaDetail
from django.forms import inlineformset_factory, modelformset_factory

class QuelleForm(forms.ModelForm):
    class Meta:
        model = Quelle
        fields = ['quellendatum','bemerkung']
        widgets = {
            'quellendatum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bemerkung': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VertragForm(forms.ModelForm):
    class Meta:
        model = Vertrag
        fields = [
            'bemerkung','vertragsart', 'vertragsbeginn', 'lieferzeit', 
            'wetterrisiko', 'vertragskennung'
        ]
        widgets = {
            'vertragsart': forms.TextInput(attrs={'class': 'form-control'}),
            'vertragsbeginn': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieferzeit': forms.TextInput(attrs={'class': 'form-control'}),
            'wetterrisiko': forms.TextInput(attrs={'class': 'form-control'}),
            'vertragskennung': forms.TextInput(attrs={'class': 'form-control'}),
            'bemerkung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SchaetzungForm(forms.ModelForm):
    class Meta:
        model = Schaetzung
        fields = ['bemerkung', 'schaetzer']
        widgets = {
            'schaetzer': forms.TextInput(attrs={'class': 'form-control'}),
            'bemerkung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AngebotForm(forms.ModelForm):
    class Meta:
        model = Angebot
        fields = ['bemerkung', 'wetterrisiko', 'angebotskennung']
        widgets = {
            'angebotskennung': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'wetterrisiko': forms.TextInput(attrs={'class': 'form-control'}),
            'bemerkung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class IndikationForm(forms.ModelForm):
    class Meta:
        model = Indikation
        fields = ['bemerkung']
        widgets = {
            'bemerkung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class QuelleDocForm(forms.ModelForm):
    class Meta:
        model = QuelleDoc
        fields = ['filename']
        widgets = {
            'filename': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class WeaPreisForm(forms.ModelForm):
    class Meta:
        model = WeaPreis
        fields = ['weaTyp_id','preis','transportkosten','waehrung','garantie_verfuegbarkeit','preis_w_fundament','gueltigkeit']
        widgets = {
            'weaTyp_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'preis': forms.NumberInput(attrs={'class': 'form-control'}),
            'transportkosten': forms.NumberInput(attrs={'class': 'form-control'}),
            'waehrung': forms.TextInput(attrs={'class': 'form-control'}),
            'garantie_verfuegbarkeit': forms.TextInput(attrs={'class': 'form-control'}),
            'preis_w_fundament': forms.NumberInput(attrs={'class': 'form-control'}),
            'gueltigkeit': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class KonditionForm(forms.ModelForm):
    class Meta:
        model = PreisKondition
        fields = ['land','wea_anzahl']
        widgets = {
            'land': forms.TextInput(attrs={'class': 'form-control'}),
            'wea_anzahl': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WeaDetailForm(forms.ModelForm):
    class Meta:
        model = WeaDetail
        fields = ['nabenhoehe','turmtyp', 'auslaufdatum', 'genehmigungsunterlagen', 'windklasse']
        widgets = {
            'nabenhoehe': forms.NumberInput(attrs={'class': 'form-control'}),
            'turmtyp': forms.TextInput(attrs={'class': 'form-control'}),
            'auslaufdatum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'genehmigungsunterlagen': forms.TextInput(attrs={'class': 'form-control'}),
            'windklasse': forms.TextInput(attrs={'class': 'form-control'}),
        }

#inlineformset ermöglicht die Bearbeitung von mehreren Modellen in einem einzigen Formular.
KonditionFormSet = inlineformset_factory(WeaPreis, PreisKondition, form=KonditionForm, extra=1, can_delete=True)
WeaDetailFormSet = inlineformset_factory(WeaPreis, WeaDetail, form=WeaDetailForm, extra=1, can_delete=True)
#QuelleDocFormSet = inlineformset_factory(Quelle, QuelleDoc, form=QuelleDocForm, extra=1, can_delete=True)

QuelleDocFormSet = modelformset_factory(QuelleDoc, form=QuelleDocForm, extra=0, can_delete=True)
KonditionFormSetEdit = modelformset_factory(PreisKondition, form=KonditionForm, extra=0, can_delete=True)
WeaDetailFormSetEdit = modelformset_factory(WeaDetail, form=WeaDetailForm, extra=0, can_delete=True)
