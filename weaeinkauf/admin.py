from django.contrib import admin

from .models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung, WeaPreis, PreisKondition, WeaFundament, WeaDetail

admin.site.register(Quelle)

admin.site.register(Vertrag)

admin.site.register(Schaetzung)

admin.site.register(Angebot)

admin.site.register(Indikation)

admin.site.register(QuelleDoc)

admin.site.register(ServicePreis)

admin.site.register(ServicePreisVerguetung)

admin.site.register(WeaPreis)

admin.site.register(PreisKondition)

admin.site.register(WeaFundament)

admin.site.register(WeaDetail)





