from django import forms
from .models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung, WeaPreis, PreisKondition, WeaFundament, WeaDetail

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
            'angebotskennung': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
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



