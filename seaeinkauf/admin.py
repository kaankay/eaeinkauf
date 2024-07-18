from django.contrib import admin

from .models import Quelle, QuelleDoc, PvModule, Wechselrichter, Unterkonstruktion, Nennleistung, Preis, Anzahl, Garantie, Technologie, Hersteller, Angebot, Datenblatt 

admin.site.register(Quelle)

admin.site.register(QuelleDoc)

admin.site.register(PvModule)

admin.site.register(Wechselrichter)

admin.site.register(Unterkonstruktion)

admin.site.register(Nennleistung)

admin.site.register(Preis)

admin.site.register(Anzahl)

admin.site.register(Garantie)

admin.site.register(Technologie)

admin.site.register(Hersteller)

admin.site.register(Angebot)

admin.site.register(Datenblatt)
