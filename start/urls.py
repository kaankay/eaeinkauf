from django.urls import path

from . import views

urlpatterns = [
    # ex: 
    path("", views.homepage, name="homepage"),

    # ex: login/
    path("login/", views.login_view, name="login"),
    # ex: logout/
    path("logout/", views.logout_view, name="logout"),
    # ex: register/
    path("register/", views.register_view, name="register"),

    # ex: wind/
    path("go-to-wind/", views.go_to_wind, name="go_to_wind"),
    # ex: pv/
    path("go-to-pv/", views.go_to_pv, name="go_to_pv"),
]