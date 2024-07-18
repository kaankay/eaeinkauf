from django.urls import path

from . import views

urlpatterns = [
    # ex: 
    path("", views.pv_index, name="pv_index"),
    # ex: go-to-homepage/
    path("go-to-homepage", views.go_to_homepage, name="go_to_homepage"),
]