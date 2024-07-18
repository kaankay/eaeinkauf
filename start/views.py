from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.utils import timezone
from django.db.models.query import QuerySet

from weaeinkauf.models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung


def getAllQuelles():
    return Quelle.objects.all()

def homepage(request):
    latest_quellen_list = Quelle.objects.order_by("-created_at")[:5]
    context ={"latest_quellen_list": latest_quellen_list}
    return render(request, "start/homepage.html", context)

def go_to_wind(request):
    return redirect("wind_index") #Name der URL in App weaeinkauf

def go_to_pv(request):
    return redirect("pv_index") #Name der URL in App seaeinkauf



