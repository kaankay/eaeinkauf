from django.urls import path

from . import views

urlpatterns = [
    # ex: 
    path("", views.homepage, name="homepage"),
    # ex: wind/
    path("go-to-wind/", views.go_to_wind, name="go_to_wind"),
    # ex: pv/
    path("go-to-pv/", views.go_to_pv, name="go_to_pv"),
]