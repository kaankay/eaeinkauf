from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.db.models.query import QuerySet

from .models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung


def getAllQuelles():
    return Quelle.objects.all()

def index(request):
    latest_quellen_list = Quelle.objects.order_by("-created_at")[:5]
    context ={"latest_quellen_list": latest_quellen_list}
    return render(request, "weaeinkauf/index.html", context)

def quellenAnzeigen(request):
    quellen_anzeigen_list =getAllQuelles()
    context={"quellen_anzeigen_list": quellen_anzeigen_list, "quellen_count": len(quellen_anzeigen_list)}
    return render(request, "weaeinkauf/quellenAnzeigen.html", context)

def quellenEintragen(request):
    quellen_anzeigen_list = Quelle.objects.all()
    context={"quellen_anzeigen_list": quellen_anzeigen_list}
    return render(request, "weaeinkauf/quellenEintragen.html", context)

def weapreisHinzufuegen(request):
    quellen_anzeigen_list = Quelle.objects.all()
    context={"quellen_anzeigen_list": quellen_anzeigen_list}
    return render(request, "weaeinkauf/weapreisHinzufuegen.html", context)

def servicepreisHinzufuegen(request):
    quellen_anzeigen_list = Quelle.objects.all()
    context={"quellen_anzeigen_list": quellen_anzeigen_list}
    return render(request, "weaeinkauf/servicepreisHinzufuegen.html", context)

def quellenDetailsAnzeigen(request):
    quellen_anzeigen_list = Quelle.objects.all()
    context={"quellen_anzeigen_list": quellen_anzeigen_list}
    return render(request, "weaeinkauf/quellenDetailsAnzeigen.html", context)

def quellenDetailsBearbeiten(request):
    quellen_anzeigen_list = Quelle.objects.all()
    context={"quellen_anzeigen_list": quellen_anzeigen_list}
    return render(request, "weaeinkauf/quellenDetailsBearbeiten.html", context)



