from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from weaeinkauf.models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung


def getAllQuelles():
    return Quelle.objects.all()

@login_required(login_url="/login/")
def homepage(request):
    authorized_pv = request.user.groups.filter(name__in=['Einkauf PV', 'Projektsteuerung']).exists()
    authorized_wind = request.user.groups.filter(name__in=['Einkauf Wind', 'Projektsteuerung']).exists()
    latest_quellen_list = Quelle.objects.order_by("-created_at")[:5]
    context ={"latest_quellen_list": latest_quellen_list, "authorized_pv": authorized_pv, "authorized_wind": authorized_wind}
    return render(request, "start/homepage.html", context)

@login_required(login_url="/login/")
def go_to_wind(request):
    return redirect("wind_index") #Name der URL in App weaeinkauf

@login_required(login_url="/login/")
def go_to_pv(request):
    return redirect("pv_index") #Name der URL in App seaeinkauf

def login_view(request):
    context = {}
    if request.user.is_authenticated:

        return redirect("/")
    else:
        post = request.POST

        if post:
            username = post.get("username")
            password = post.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context.update({"error": "Falsche Anmeldeinformationen!"})

    return render(request, "start/login.html", context)

def logout_view(request):
    logout(request)

    return HttpResponseRedirect("/login/")

def register_view(request):
    context = {}
    if request.user.is_authenticated:

        return redirect("/")
    else:
        post = request.POST

        if post:
            username = post.get("username")
            password = post.get("password")
            password2 = post.get("password2")
            email = post.get('email')
            if User.objects.filter(username=username).exists():
                context.update({"error": "Benutzername ist bereits vorhanden."})
                return render(request, "start/register.html", context)
            if User.objects.filter(email=email).exists():
                context.update({"error": "E-Mail ist bereits vorhanden."})
                return render(request, "start/register.html", context)
            if password != password2:
                context.update({"error": "Passwörter stimmen nicht überein."})
                return render(request, "start/register.html", context)

            user = User.objects.create_user(username=username, password=password, email=email)

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")

    return render(request, "start/register.html", context)


