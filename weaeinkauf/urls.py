from django.urls import path

from . import views

urlpatterns = [
    # ex: 
    path("", views.index, name="index"),
    # ex: /quellenanzeigen/
    path("quellenanzeigen/", views.quellenAnzeigen, name="quellenAnzeigen"),
    # ex: /quelleneintragen/
    path("quelleneintragen/", views.quellenEintragen, name="quellenEintragen"),
     # ex: /weapreishinzufuegen/
    path("weapreishinzufuegen/", views.weapreisHinzufuegen, name="weapreisHinzufuegen"),
    # ex: /servicepreishinzufuegen/
    path("servicepreishinzufuegen/", views.servicepreisHinzufuegen, name="servicepreisHinzufuegen"),
    # ex: /quellendetailsanzeigen/
    path("quellendetailsanzeigen/", views.quellenDetailsAnzeigen, name="quellenDetailsAnzeigen"),
    # ex: /quellendetailsbearbeiten/
    path("quellendetailsbearbeiten/", views.quellenDetailsBearbeiten, name="quellenDetailsBearbeiten"),
]