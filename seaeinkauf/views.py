from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from django.db.models.query import QuerySet

from .models import Quelle, Datenblatt, Angebot, QuelleDoc
from django.contrib.auth.decorators import login_required, user_passes_test

# Funktion zur Überprüfung der Gruppenzugehörigkeit
def group_check(user):
    return user.groups.filter(name__in=['Einkauf PV', 'Projektsteuerung', 'Admin']).exists()

def getAllQuelles():
    return Quelle.objects.all()

@login_required(login_url="/login/")
@user_passes_test(group_check, login_url="/")
def pv_index(request):
    latest_quellen_list = Quelle.objects.order_by("-created_at")[:5]
    context ={"latest_quellen_list": latest_quellen_list}
    return render(request, "seaeinkauf/index.html", context)

def go_to_homepage(request):
    return redirect("homepage")



