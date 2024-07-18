import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class Quelle(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quellendatum = models.DateField()
    bemerkung = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Name: {self.name} / Quellendatum: {self.quellendatum} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Angebot(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    quellendatum = models.DateField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    created_by =models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at} "
    
class Datenblatt(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    quellendatum = models.DateField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Quellendatum: {self.quellendatum} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at}"

class QuelleDoc(models.Model):
    name = models.TextField(null=True, blank=True)
    filename = models.TextField(null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    created_by =models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Filename: {self.filename} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Wechselrichter(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    created_by =models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Name: {self.name} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class PvModule(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    abmessung = models.FloatField(null=True, blank=True)
    wirkungsgrad = models.FloatField(null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    created_by =models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Name: {self.name} / Abmessung: {self.abmessung} mm / Wirkungsgrad: {self.wirkungsgrad} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Unterkonstruktion(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    tischvariante = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    created_by =models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Name: {self.name} / Bezeichnung der Tischvariante: {self.tischvariante} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Anzahl(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    anzahlproPalette = models.IntegerField(null=True, blank=True)   
    anzahlproContainer = models.IntegerField(null=True, blank=True)   
    bemerkung = models.TextField(null=True, blank=True)
    pvModule = models.ForeignKey(PvModule, on_delete = models.CASCADE)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Anzahl pro Palette: {self.anzahlproPalette} / Anzahl pro 40 Container : {self.anzahlproContainer} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Nennleistung(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    leistung = models.FloatField(null=True, blank=True)
    einheit = models.CharField(max_length=200, null=True, blank=True)
    pvModule = models.ForeignKey(PvModule, on_delete = models.CASCADE)
    wechselrichter = models.ForeignKey(Wechselrichter, on_delete = models.CASCADE)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Nennleistung: {self.leistung} {self.einheit} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Hersteller(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    pvModule = models.ForeignKey(PvModule, on_delete = models.CASCADE)
    wechselrichter = models.ForeignKey(Wechselrichter, on_delete = models.CASCADE)
    unterkonstruktion = models.ForeignKey(Unterkonstruktion, on_delete = models.CASCADE)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Name: {self.name} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Garantie(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    degradation = models.FloatField(null=True, blank=True)
    leistungsgarantie = models.IntegerField(null=True, blank=True)   
    performancegarantie = models.IntegerField(null=True, blank=True)   
    pvModule = models.ForeignKey(PvModule, on_delete = models.CASCADE)
    created_by =models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Jährliche Degradation: {self.degradation} % / Dauer der Leistungsgarantie: {self.leistungsgarantie} / Dauer der Performancegarantie: {self.performancegarantie} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Technologie(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    art = models.CharField(max_length=200, null=True, blank=True)
    pvModule = models.ForeignKey(PvModule, on_delete = models.CASCADE)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Art von Technologie: {self.art} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class Preis(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    preis = models.IntegerField(null=True, blank=True)
    waehrung = models.CharField(max_length=200, null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    pvModule = models.ForeignKey(PvModule, on_delete = models.CASCADE)
    wechselrichter = models.ForeignKey(Wechselrichter, on_delete = models.CASCADE)
    unterkonstruktion = models.ForeignKey(Unterkonstruktion, on_delete = models.CASCADE)
    created_by = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Preis: {self.preis} {self.waehrung} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at}"