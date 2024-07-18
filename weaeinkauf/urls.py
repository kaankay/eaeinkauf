from django.urls import path

from . import views

urlpatterns = [
    # ex: 
    path("", views.wind_index, name="wind_index"),
    # ex: go-to-homepage
    path("go-to-homepage", views.go_to_homepage, name="go_to_homepage"),
    # ex: wind/quellenanzeigen/
    path("quellenanzeigen/", views.quellenAnzeigen, name="quellenAnzeigen"),
    # ex: wind/quelleneintragen/
    path("quelleneintragen/", views.quellenEintragen, name="quellenEintragen"),
     # ex: wind/weapreishinzufuegen/
    path("weapreishinzufuegen/", views.weapreisHinzufuegen, name="weapreisHinzufuegen"),
    # ex: wind/servicepreishinzufuegen/
    path("servicepreishinzufuegen/", views.servicepreisHinzufuegen, name="servicepreisHinzufuegen"),
    # ex: wind/quellendetailsanzeigen/895/
    path("quellendetailsanzeigen/<int:pk>/", views.quellenDetailsAnzeigen, name="quellenDetailsAnzeigen"),
    # ex: wind/quellendetailsanzeigen/895/bearbeiten/
    path("quellendetailsanzeigen/<int:pk>/bearbeiten/", views.quellenDetailsBearbeiten, name="quellenDetailsBearbeiten"),
    # ex: wind/quellendetailsanzeigen/895/bearbeiten/loeschen/
    path("quellendetailsanzeigen/<int:pk>/bearbeiten/loeschen/", views.quellenDetailsLoeschen, name="quellenDetailsLoeschen"),
]