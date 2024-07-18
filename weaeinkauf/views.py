from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.forms import modelformset_factory

from .models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung, WeaPreis, PreisKondition, WeaFundament, WeaDetail
from .forms import QuelleForm, VertragForm, SchaetzungForm, AngebotForm, IndikationForm, QuelleDocForm


def getAllQuelles():
    return Quelle.objects.all()

def combined_list(request):
    allQuelle = Quelle.objects.all()
    allQuelleDoc = QuelleDoc.objects.all()
    combined = zip(allQuelle, allQuelleDoc)
    return list(combined)

def wind_index(request):
    latest_quellen_list = Quelle.objects.order_by("-created_at")[:5]
    context ={"latest_quellen_list": latest_quellen_list}
    return render(request, "weaeinkauf/index.html", context)

def go_to_homepage(request):
    return redirect ("homepage")

def quellenAnzeigen(request):
    quellen_anzeigen_list =getAllQuelles()
    combined_data = combined_list(request)  # combined_list aufrufen und die kombinierten Daten erhalten

    # Anzahl der Elemente pro Seite festlegen
    paginator = Paginator(combined_data, 10)  # 10 Elemente pro Seite

    # Aktuelle Seitenzahl aus der URL holen
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={"quellen_anzeigen_list": quellen_anzeigen_list, "quellen_count": len(quellen_anzeigen_list), "page_obj": page_obj}
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

def quellenDetailsAnzeigen(request, pk):
    quelleDetail = get_object_or_404(Quelle, pk=pk)
    angebote = Angebot.objects.filter(quelle=quelleDetail)
    vertraege = Vertrag.objects.filter(quelle=quelleDetail)
    schaetzungen = Schaetzung.objects.filter(quelle=quelleDetail)
    indikationen = Indikation.objects.filter(quelle=quelleDetail)
    weaPreise = WeaPreis.objects.filter(quelle=quelleDetail)

    #Das sind die Tabellen, die dazwischen keine direkte Beziehung haben.
    weaDetails = WeaDetail.objects.filter(weaPreis__quelle=quelleDetail)
    
    quelleDocs = QuelleDoc.objects.filter(quelle=quelleDetail)
    servicePreise = ServicePreis.objects.filter(quelle=quelleDetail)

    context={"quelleDetail": quelleDetail,
             "angebote": angebote,
             "vertraege": vertraege,
             "schaetzungen": schaetzungen,
             "indikationen": indikationen,
             "weaPreise": weaPreise,
             "weaDetails": weaDetails,
             "quelleDocs": quelleDocs,
             "servicePreise": servicePreise}
    
    return render(request, "weaeinkauf/quellenDetailsAnzeigen.html", context)

def quellenDetailsBearbeiten(request, pk):
    quelleDetail = get_object_or_404(Quelle, pk=pk)

    # Formulare und Formsets initialisieren
    QuelleDocFormSet = modelformset_factory(QuelleDoc, form=QuelleDocForm, extra=0, can_delete=True)

    # Alle relevanten Daten für die Quelle abrufen
    angebote = Angebot.objects.filter(quelle=quelleDetail)
    vertraege = Vertrag.objects.filter(quelle=quelleDetail)
    schaetzungen = Schaetzung.objects.filter(quelle=quelleDetail)
    indikationen = Indikation.objects.filter(quelle=quelleDetail)
    weaPreise = WeaPreis.objects.filter(quelle=quelleDetail)

    #Das sind die Tabellen, die dazwischen keine direkte Beziehung haben.
    weaDetails = WeaDetail.objects.filter(weaPreis__quelle=quelleDetail)
    
    quelleDocs = QuelleDoc.objects.filter(quelle=quelleDetail)
    servicePreise = ServicePreis.objects.filter(quelle=quelleDetail)
    
    # Formulare je nach Quellenart initialisieren
    if quelleDetail.quellenart == "Angebot":
        quellenart_form = AngebotForm(instance=angebote.first())
    elif quelleDetail.quellenart == "Vertrag":
        quellenart_form = VertragForm(instance=vertraege.first())
    elif quelleDetail.quellenart == "Indikation":
        quellenart_form = IndikationForm(instance=indikationen.first())
    elif quelleDetail.quellenart == "Schätzung":
        quellenart_form = SchaetzungForm(instance=schaetzungen.first())
    else:
        quellenart_form = None

    # Initialdaten für das Hauptformular setzen
    initial_data = {
        'quellendatum': quelleDetail.quellendatum,
        'bemerkung': quelleDetail.bemerkung,
    }
    form = QuelleForm(instance=quelleDetail, initial=initial_data)

    # Formsets initialisieren
    quelleDocs = QuelleDoc.objects.filter(quelle=quelleDetail)
    quelleDoc_formset = QuelleDocFormSet(queryset=quelleDocs)

    if request.method == "POST":
        form = QuelleForm(request.POST, instance=quelleDetail)
        quelleDoc_formset = QuelleDocFormSet(request.POST, queryset=quelleDocs)

        if form.is_valid() and quelleDoc_formset.is_valid():
            form.save()
            quelleDoc_formset.save()

            # Je nach Quellenart entsprechendes Formular speichern
            if quelleDetail.quellenart == "Angebot":
                quellenart_form = AngebotForm(request.POST, instance=angebote.first())

            elif quelleDetail.quellenart == "Vertrag":
                quellenart_form = VertragForm(request.POST, instance=vertraege.first())
                
            elif quelleDetail.quellenart == "Indikation":
                quellenart_form = IndikationForm(request.POST, instance=indikationen.first())
                
            elif quelleDetail.quellenart == "Schätzung":
                quellenart_form = SchaetzungForm(request.POST, instance=schaetzungen.first())
                
            if quellenart_form and quellenart_form.is_valid():
                quellenart_form.save()

            return redirect("quellenDetailsAnzeigen", pk=quelleDetail.pk)

    context={
        "quelleDetail": quelleDetail,
        "angebote": angebote,
        "vertraege": vertraege,
        "schaetzungen": schaetzungen,
        "indikationen": indikationen,
        "weaPreise": weaPreise,
        "weaDetails": weaDetails,
        "quelleDocs": quelleDocs,
        "servicePreise": servicePreise,
        "form": form,
        "quellenart_form": quellenart_form,
        "quelleDoc_formset": quelleDoc_formset}
    
    return render(request, "weaeinkauf/quellenDetailsBearbeiten.html", context)

def quellenDetailsLoeschen(request, pk):
    quelleDetail = get_object_or_404(Quelle, pk=pk)
    quelleDetail.delete()
    return redirect("quellenAnzeigen", pk=quelleDetail.pk)



