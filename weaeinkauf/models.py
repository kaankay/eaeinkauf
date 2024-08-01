import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


quellenartOption = (
    ("Vertrag", "Vertrag"),
    ("Schätzung", "Schätzung"),
    ("Indikation", "Indikation"),
    ("Angebot", "Angebot"),
)


class Quelle(models.Model):
    alt_id= models.IntegerField(default=0)
    name = models.CharField(max_length=200, null=True, blank=True)
    quellendatum = models.DateField()
    bemerkung = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=200, default="null")

    quellenart = models.CharField(max_length=200, choices= quellenartOption, default= "Angebot")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Quellendatum: {self.quellendatum} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at}"

class Vertrag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    bemerkung = models.TextField(null=True, blank=True)
    quellendatum = models.DateField(null=True, blank=True)
    vertragsart = models.CharField(max_length=200, null=True, blank=True)
    vertragsbeginn = models.DateField(null=True, blank=True)
    lieferzeit =models.CharField(max_length=200, null=True, blank=True)
    wetterrisiko = models.CharField(max_length=200, null=True, blank=True)
    vertragskennung = models.CharField(max_length=200, null=True, blank=True)
    sonderkuendigungsrecht = models.CharField(max_length=500, null=True, blank=True)
    quellen_id = models.IntegerField(default=0)
    created_by =models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Quellendatum: {self.quellendatum} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at} / Vertragskennung: {self.vertragskennung} / Vertragsart: {self.vertragsart}"

class Schaetzung(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    quellendatum = models.DateField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    schaetzer =models.CharField(max_length=200, null=True, blank=True)
    quellen_id = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Quellendatum: {self.quellendatum} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at} / Schätzer: {self.schaetzer}"

class Angebot(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    quellendatum = models.DateField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    wetterrisiko =models.CharField(max_length=200, null=True, blank=True)
    angebotskennung =models.TextField(null=True, blank=True)
    quellen_id = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Quelle_ID: {self.quellen_id} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at} / Wetterrisiko: {self.wetterrisiko} / Angebotskennung: {self.angebotskennung}"

class Indikation(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    quellendatum = models.DateField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    quellen_id = models.IntegerField(default=0)
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
    quellen_id = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Filename: {self.filename} / Created_by: {self.created_by} / Created_at: {self.created_at}"

class ServicePreis(models.Model):
    alt_id= models.IntegerField(default=0)
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    laufzeit = models.IntegerField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    basisjahr = models.IntegerField(null=True, blank=True)
    grenzwert = models.FloatField(null=True, blank=True)
    kuendigungsrecht = models.TextField(null=True, blank=True)
    quellen_id = models.IntegerField(default=0)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Name: {self.name} / Laufzeit: {self.laufzeit} / Bemerkung: {self.bemerkung} / Created_by: {self.created_by} / Created_at: {self.created_at}"

class ServicePreisVerguetung(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    servicePreis = models.ForeignKey(ServicePreis, on_delete = models.CASCADE)
    jahr = models.IntegerField(null=True, blank=True)
    indexierung = models.IntegerField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    var = models.FloatField(null=True, blank=True)
    fix = models.FloatField(null=True, blank=True)
    minPreis = models.FloatField(null=True, blank=True)
    servicePreisID = models.IntegerField(default=0)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Service-Preis ID: {self.servicePreis} / Bemerkung: {self.bemerkung} / Var: {self.var} / Fix: {self.fix} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class WeaPreis(models.Model):
    alt_id= models.IntegerField(default=0)
    name = models.CharField(max_length=200, null=True, blank=True)
    quelle = models.ForeignKey(Quelle, on_delete = models.CASCADE)
    weaTyp_id = models.IntegerField(default=0)
    preis = models.FloatField(null=True, blank=True)
    waehrung = models.CharField(max_length=200, null=True, blank=True)
    transportkosten = models.IntegerField(null=True, blank=True)
    gueltigkeit = models.DateField(null=True, blank=True)
    garantie_verfuegbarkeit = models.CharField(max_length=200, null=True, blank=True)
    quellen_id = models.IntegerField(default=0)
    preis_w_fundament = models.FloatField(null=True, blank=True)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Preis: {self.preis} {self.waehrung} / Garantie: {self.garantie_verfuegbarkeit} / Preis(WEA Fundament): {self.preis_w_fundament} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class PreisKondition(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    land = models.CharField(max_length=200, null=True, blank=True)
    wea_anzahl = models.CharField(max_length=200, null=True, blank=True)
    weaPreis = models.OneToOneField(WeaPreis, on_delete = models.CASCADE)
    weaPreisID = models.IntegerField(default=0)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Anzahl(WEA): {self.wea_anzahl} {self.land} / WEA-Preis ID: {self.weaPreisID} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class WeaFundament(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    weaPreis = models.OneToOneField(WeaPreis, on_delete = models.CASCADE)
    fundament_preis = models.IntegerField(null=True, blank=True)
    weaPreisID = models.IntegerField(default=0)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Fundament-Preis: {self.fundament_preis} / WEA-Preis ID: {self.weaPreisID} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
class WeaDetail(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    weaPreis = models.OneToOneField(WeaPreis, on_delete = models.CASCADE)
    nabenhoehe = models.FloatField(null=True, blank=True)
    turmtyp = models.CharField(max_length=200, null=True, blank=True)
    auslaufdatum = models.DateField(null=True, blank=True)
    genehmigungsunterlagen = models.CharField(max_length=200, null=True, blank=True)
    windklasse = models.CharField(max_length=200, null=True, blank=True)
    weaPreisID = models.IntegerField(default=0)
    gesamthoehe = models.FloatField(null=True, blank=True)
    created_by =models.CharField(max_length=200, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} / Nabenhoehe: {self.nabenhoehe} / Gesamthoehe: {self.gesamthoehe} / WEA-Preis ID: {self.weaPreisID} / Created_by: {self.created_by} / Created_at: {self.created_at}"
    
# class Projekt(models.Model):
#     alt_id= models.IntegerField(default=0)
#     kurzName = models.CharField(max_length=200, null=True, blank=True)
#     langName = models.CharField(max_length=200, null=True, blank=True)
#     quelle = models.ManyToManyField(Quelle, on_delete = models.CASCADE)
#     servicePreis = models.ManyToManyField(ServicePreis, on_delete = models.CASCADE)
#     servicePreisID = models.IntegerField(default=0)
#     quellen_id = models.IntegerField(default=0)