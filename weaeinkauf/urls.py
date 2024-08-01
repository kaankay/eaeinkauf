from django.urls import path

from . import views

urlpatterns = [
    # ex: 
    path("", views.wind_index, name="wind_index"),
    # ex: go-to-homepage
    path("go-to-homepage", views.go_to_homepage, name="go_to_homepage"),
    # ex: wind/quellenanzeigen/
    path("quellenanzeigen/", views.quellenAnzeigen, name="quellenAnzeigen"),
    # ex: wind/quellendetailsanzeigen/895/
    path("quellendetailsanzeigen/<int:pk>/", views.quellenDetailsAnzeigen, name="quellenDetailsAnzeigen"),
    # ex: wind/quellendetailsanzeigen/895/bearbeiten/
    path("quellendetailsanzeigen/<int:pk>/bearbeiten/", views.quellenDetailsBearbeiten, name="quellenDetailsBearbeiten"),
    # ex: wind/quellendetailsanzeigen/895/bearbeiten/loeschen/
    path("quellendetailsanzeigen/<int:pk>/bearbeiten/loeschen/", views.quellenDetailsLoeschen, name="quellenDetailsLoeschen"),
    # ex: wind/quelleneintragen/
    path("quelleneintragen/", views.quellenEintragen, name="quellenEintragen"),
    # ex: wind/schaetzungeintragen/
    path("schaetzungeintragen/", views.schaetzungEintragen, name="schaetzungEintragen"),
    # ex: wind/indikationeintragen/
    path("indikationeintragen/", views.indikationEintragen, name="indikationEintragen"),
    # ex: wind/angeboteintragen/
    path("angeboteintragen/", views.angebotEintragen, name="angebotEintragen"),
    # ex: wind/vertrageintragen/
    path("vertrageintragen/", views.vertragEintragen, name="vertragEintragen"),
    # ex: wind/weapreiseanzeigen/
    path("weapreiseanzeigen/", views.weapreiseAnzeigen, name="weapreiseAnzeigen"),
    # ex: wind/weapreisdetailsanzeigen/895/
    path("weapreisdetailsanzeigen/<int:pk>/", views.weapreisDetailsAnzeigen, name="weapreisDetailsAnzeigen"),
    # ex: weapreisdetailsanzeigen/<int:pk>/bearbeiten/
    path("weapreisdetailsanzeigen/<int:pk>/bearbeiten/", views.weapreisDetailsBearbeiten, name="weapreisDetailsBearbeiten"),
    # ex: weapreisdetailsanzeigen/<int:pk>/bearbeiten/loeschen/
    path("weapreisdetailsanzeigen/<int:pk>/bearbeiten/loeschen/", views.weapreisDetailsLoeschen, name="weapreisDetailsLoeschen"),
    # ex: wind/weapreishinzufuegen/895/
    path("weapreishinzufuegen/<int:pk>/", views.weapreisHinzufuegen, name="weapreisHinzufuegen"),
    # ex: wind/servicepreiseanzeigen/
    path("servicepreiseanzeigen/", views.servicepreiseAnzeigen, name="servicepreiseAnzeigen"),
    # ex: wind/servicepreishinzufuegen/
    path("servicepreishinzufuegen/", views.servicepreisHinzufuegen, name="servicepreisHinzufuegen"),
    
]