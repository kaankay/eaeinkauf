from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.db.models.query import QuerySet

from .models import Quelle, Datenblatt, Angebot, QuelleDoc


def getAllQuelles():
    return Quelle.objects.all()

def pv_index(request):
    latest_quellen_list = Quelle.objects.order_by("-created_at")[:5]
    context ={"latest_quellen_list": latest_quellen_list}
    return render(request, "seaeinkauf/index.html", context)

def go_to_homepage(request):
    return redirect("homepage")



