from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Quelle, Vertrag, Schaetzung, Angebot, Indikation, QuelleDoc, ServicePreis, ServicePreisVerguetung, WeaPreis, PreisKondition, WeaFundament, WeaDetail
from .forms import QuelleForm, VertragForm, SchaetzungForm, AngebotForm, IndikationForm, QuelleDocForm, WeaPreisForm, KonditionForm, WeaDetailForm, KonditionFormSet, WeaDetailFormSet, QuelleDocFormSet, KonditionFormSetEdit, WeaDetailFormSetEdit

import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

# Funktion zur Überprüfung der Gruppenzugehörigkeit Einkauf Wind oder Projektsteuerung
def group_check(user):
    return user.groups.filter(name__in=['Einkauf Wind', 'Projektsteuerung', 'Admin']).exists()

# Funktion zur Überprüfung der Gruppenzugehörigkeit nur Einkauf Wind
def group_check_edit(user):
    return user.groups.filter(name__in=['Einkauf Wind', 'Admin']).exists()

def getAllQuelles(quellenart, search_query):
    qs = Quelle.objects.all()
    if quellenart:
        quellenart = quellenart.strip()
        qs.filter(quellenart=quellenart) # eger quellenart bilgisi varsa sonuclari filtrele
    if search_query:
        search_query = search_query.strip()
        qs.filter(Q(created_by__icontains=search_query))
    return qs

def getAllWeapreise():
    return WeaPreis.objects.all()

def getAllServicepreise():
    return ServicePreis.objects.all()

def combined_list(request, quellenart, search_query):
    qs = Quelle.objects.all()
    if quellenart:
        quellenart = quellenart.strip()
        qs = qs.filter(quellenart=quellenart) # eger quellenart bilgisi varsa sonuclari filtrele
    if search_query:
        search_query = search_query.strip()
        qs = qs.filter(Q(created_by__icontains=search_query) | Q(quellenart__icontains=search_query)) # createdby veya quellenart a uyuyorsa filtreler

    allQuelle = qs
    quelDoc = []

    for quel in allQuelle:
        doc = QuelleDoc.objects.filter(quelle=quel)
        quelDoc += doc

    allQuelleDoc = quelDoc

    #allQuelleDoc = QuelleDoc.objects.all()   # !!! allQuelleDoc filtrelenmedi
    combined = zip(allQuelle, allQuelleDoc)
    return list(combined)

def combined_list_weapreise(request):
    #allQuelle = Quelle.objects.all()
    allWeapreise = WeaPreis.objects.all()
    allWeaDetails = WeaDetail.objects.all()
    allPreisKonditionen = PreisKondition.objects.all()
    combined = zip(allWeapreise, allWeaDetails, allPreisKonditionen)
    return list(combined)

def combined_list_servicepreise(request):
    allServicepreise = ServicePreis.objects.all()
    allServicepreiseVerguetung = ServicePreisVerguetung.objects.all()
    combined = zip(allServicepreise, allServicepreiseVerguetung)
    return list(combined)

@login_required(login_url="/login/")
@user_passes_test(group_check, login_url="/")
def wind_index(request):
    latest_quellen_list = Quelle.objects.order_by("-created_at")[:5]
    context ={"latest_quellen_list": latest_quellen_list}
    return render(request, "weaeinkauf/index.html", context)

def go_to_homepage(request):
    return redirect ("homepage")

@login_required(login_url="/login/")
@user_passes_test(group_check, login_url="/")
def quellenAnzeigen(request):
    param = "" # Diese Variable wird erstellt um den Filter in quellenAnzeigen.html nicht zu verlieren, und sie wurde am Ende der Paginierungs-URLs im HTML-Abschnitt hinzugefügt.
    quellenart = request.GET.get("quellenart") # nimm von requestten die Daten, welche Quellanrt ausgwählt wurde.
    search_query = request.GET.get("search") 
    export = request.POST.get('export') 
    if quellenart:
        param = param + f"&quellenart={quellenart}" 
    if search_query:
        param = param + f"&search={search_query}" 
    quellen_anzeigen_list =getAllQuelles(quellenart, search_query) 

    combined_data = combined_list(request, quellenart, search_query)  # combined_list aufrufen und die kombinierten Daten erhalten
    
    if export:
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="quelle.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow(['Quelle ID', 'Quellendatum', 'Bemerkung', 'Erstellt von', 'Erstellt am', 'Projekte', 'Quellenart']) # header von csv
        for quelle, quelleDoc in combined_data:
            writer.writerow([quelle.id, quelle.quellendatum, quelle.bemerkung, quelle.created_by, quelle.created_at, '', quelle.quellenart]) # daten für csv

        return response

    # Anzahl der Elemente pro Seite festlegen
    paginator = Paginator(combined_data, 10)  # 10 Elemente pro Seite

    # Aktuelle Seitenzahl aus der URL holen
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={"quellen_anzeigen_list": quellen_anzeigen_list, "quellen_count": len(quellen_anzeigen_list), "page_obj": page_obj, "param": param, "search_query": search_query}
    return render(request, "weaeinkauf/quellenAnzeigen.html", context)

@user_passes_test(group_check, login_url="/")
@login_required(login_url="/login/")
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

@user_passes_test(group_check_edit, login_url="/")
@login_required(login_url="/login/")
def quellenDetailsBearbeiten(request, pk):
    quelleDetail = get_object_or_404(Quelle, pk=pk)

    # Formulare und Formsets initialisieren
    # QuelleDocFormSet = modelformset_factory(QuelleDoc, form=QuelleDocForm, extra=0, can_delete=True)

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
    # quelleDocs = QuelleDoc.objects.filter(quelle=quelleDetail)
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

@user_passes_test(group_check_edit, login_url="/")
def quellenDetailsLoeschen(request, pk):
    quelleDetail = get_object_or_404(Quelle, pk=pk)
    quelleDetail.delete()
    return redirect("quellenAnzeigen", pk=quelleDetail.pk)

@login_required(login_url="/login/")
@user_passes_test(group_check_edit, login_url="/")
def quellenEintragen(request):
    quellen_anzeigen_list = Quelle.objects.all()
    context={"quellen_anzeigen_list": quellen_anzeigen_list}
    return render(request, "weaeinkauf/quellenEintragen.html", context)

@login_required(login_url="/login/")
@user_passes_test(group_check_edit, login_url="/")
def schaetzungEintragen(request):

    if request.method == 'POST':
        quelle_form = QuelleForm(request.POST)
        schaetzung_form = SchaetzungForm(request.POST)
        quelledoc_form = QuelleDocForm(request.POST, request.FILES)
        if quelle_form.is_valid() and schaetzung_form.is_valid() and quelledoc_form.is_valid():
            quelle = quelle_form.save()
            schaetzung = schaetzung_form.save(commit=False)
            schaetzung.quelle = quelle
            schaetzung.save()
            quelledoc = quelledoc_form.save(commit=False)
            quelledoc.quelle = quelle
            quelledoc.save()
            return redirect("quellenAnzeigen")  # Eine URL zu Ihrer Erfolgsmeldung
    else:
        quelle_form = QuelleForm()
        schaetzung_form = SchaetzungForm()
        quelledoc_form = QuelleDocForm()

    context = {
        'quelle_form': quelle_form,
        'schaetzung_form': schaetzung_form,
        'quelledoc_form': quelledoc_form,
    }

    return render(request, 'weaeinkauf/schaetzungEintragen.html', context)

@login_required(login_url="/login/")
@user_passes_test(group_check_edit, login_url="/")
def indikationEintragen(request):

    if request.method == 'POST':
        quelle_form = QuelleForm(request.POST)
        indikation_form = IndikationForm(request.POST)
        quelledoc_form = QuelleDocForm(request.POST, request.FILES)
        if quelle_form.is_valid() and indikation_form.is_valid() and quelledoc_form.is_valid():
            quelle = quelle_form.save()
            indikation = indikation_form.save(commit=False)
            indikation.quelle = quelle
            indikation.save()
            quelledoc = quelledoc_form.save(commit=False)
            quelledoc.quelle = quelle
            quelledoc.save()
            return redirect("quellenAnzeigen")  # Eine URL zu Ihrer Erfolgsmeldung
    else:
        quelle_form = QuelleForm()
        indikation_form = IndikationForm()
        quelledoc_form = QuelleDocForm()

    context = {
        'quelle_form': quelle_form,
        'indikation_form': indikation_form,
        'quelledoc_form': quelledoc_form,
    }

    return render(request, 'weaeinkauf/indikationEintragen.html', context)

@login_required(login_url="/login/")
@user_passes_test(group_check_edit, login_url="/")
def angebotEintragen(request):

    if request.method == 'POST':
        quelle_form = QuelleForm(request.POST)
        angebot_form = AngebotForm(request.POST)
        quelledoc_form = QuelleDocForm(request.POST, request.FILES)
        if quelle_form.is_valid() and angebot_form.is_valid() and quelledoc_form.is_valid():
            quelle = quelle_form.save()
            angebot = angebot_form.save(commit=False)
            angebot.quelle = quelle
            angebot.save()
            quelledoc = quelledoc_form.save(commit=False)
            quelledoc.quelle = quelle
            quelledoc.save()
            return redirect("quellenAnzeigen")  # Eine URL zu Ihrer Erfolgsmeldung
    else:
        quelle_form = QuelleForm()
        angebot_form = AngebotForm()
        quelledoc_form = QuelleDocForm()

    context = {
        'quelle_form': quelle_form,
        'angebot_form': angebot_form,
        'quelledoc_form': quelledoc_form,
    }

    return render(request, 'weaeinkauf/angebotEintragen.html', context)

@login_required(login_url="/login/")
@user_passes_test(group_check_edit, login_url="/")
def vertragEintragen(request):

    if request.method == 'POST':
        quelle_form = QuelleForm(request.POST)
        vertrag_form = VertragForm(request.POST)
        quelledoc_form = QuelleDocForm(request.POST, request.FILES)
        if quelle_form.is_valid() and vertrag_form.is_valid() and quelledoc_form.is_valid():
            quelle = quelle_form.save()
            vertrag = vertrag_form.save(commit=False)
            vertrag.quelle = quelle
            vertrag.save()
            quelledoc = quelledoc_form.save(commit=False)
            quelledoc.quelle = quelle
            quelledoc.save()
            return redirect("quellenAnzeigen")  # Eine URL zu Ihrer Erfolgsmeldung
    else:
        quelle_form = QuelleForm()
        vertrag_form = VertragForm()
        quelledoc_form = QuelleDocForm()

    context = {
        'quelle_form': quelle_form,
        'vertrag_form': vertrag_form,
        'quelledoc_form': quelledoc_form,
    }

    return render(request, 'weaeinkauf/vertragEintragen.html', context)

@login_required(login_url="/login/")
@user_passes_test(group_check, login_url="/")
def weapreiseAnzeigen(request):
    weapreise_anzeigen_list =getAllWeapreise()
    combined_data_weapreise = combined_list_weapreise(request)  # combined_list aufrufen und die kombinierten Daten erhalten

    # Anzahl der Elemente pro Seite festlegen
    paginator = Paginator(combined_data_weapreise, 10)  # 10 Elemente pro Seite

    # Aktuelle Seitenzahl aus der URL holen
    page_number = request.GET.get('page')
    page_obj_weapreise = paginator.get_page(page_number)

    context={"weapreise_anzeigen_list": weapreise_anzeigen_list, "weapreise_count": len(weapreise_anzeigen_list), "page_obj_weapreise": page_obj_weapreise}
    return render(request, "weaeinkauf/weapreiseAnzeigen.html", context)

@login_required(login_url="/login/")
@user_passes_test(group_check, login_url="/")
def weapreisDetailsAnzeigen(request, pk):
    weaPreisDetail = get_object_or_404(WeaPreis, pk=pk)
    quelle = weaPreisDetail.quelle

    weaDetail = WeaDetail.objects.filter(weaPreis=weaPreisDetail)
    kondition = PreisKondition.objects.filter(weaPreis=weaPreisDetail)
    fundament = WeaFundament.objects.filter(weaPreis=weaPreisDetail)

    angebote = Angebot.objects.filter(quelle=quelle)
    vertraege = Vertrag.objects.filter(quelle=quelle)
    schaetzungen = Schaetzung.objects.filter(quelle=quelle)
    indikationen = Indikation.objects.filter(quelle=quelle)
    quelleDocs = QuelleDoc.objects.filter(quelle=quelle)

    context={"weaPreisDetail": weaPreisDetail,
             "weaDetail": weaDetail,
             "kondition": kondition,
             "fundament": fundament,
             "angebote": angebote,
             "vertraege": vertraege,
             "schaetzungen": schaetzungen,
             "indikationen": indikationen,
             "quelleDocs": quelleDocs,
             "quelle": quelle,
             }
    
    return render(request, "weaeinkauf/weapreisDetailsAnzeigen.html", context)

@login_required(login_url="/login/")
@user_passes_test(group_check_edit, login_url="/")
def weapreisDetailsBearbeiten(request, pk):
    weaPreisDetail = get_object_or_404(WeaPreis, pk=pk)
    quelle = weaPreisDetail.quelle

    weaDetail = WeaDetail.objects.filter(weaPreis=weaPreisDetail)
    kondition = PreisKondition.objects.filter(weaPreis=weaPreisDetail)
    #fundament = WeaFundament.objects.filter(weaPreis=weaPreisDetail)

    angebote = Angebot.objects.filter(quelle=quelle)
    vertraege = Vertrag.objects.filter(quelle=quelle)
    schaetzungen = Schaetzung.objects.filter(quelle=quelle)
    indikationen = Indikation.objects.filter(quelle=quelle)
    quelleDocs = QuelleDoc.objects.filter(quelle=quelle)

    # Initialdaten für das Hauptformular setzen
    initial_data = {
        'weaTyp_id': weaPreisDetail.weaTyp_id,
        'preis': weaPreisDetail.preis,
        'transportkosten': weaPreisDetail.transportkosten,
        'waehrung': weaPreisDetail.waehrung,
        'garantie_verfuegbarkeit': weaPreisDetail.garantie_verfuegbarkeit,
        'preis_w_fundament': weaPreisDetail.preis_w_fundament,
        'gueltigkeit': weaPreisDetail.gueltigkeit,
                }
    weaPreis_form = WeaPreisForm(instance=weaPreisDetail, initial=initial_data)

    # Formsets initialisieren
    kondition_formset = KonditionFormSetEdit(queryset=kondition)
    weaDetail_formset = WeaDetailFormSetEdit(queryset=weaDetail)
    
    if request.method == "POST":
        weaPreis_form = WeaPreisForm(request.POST, instance=weaPreisDetail)
        kondition_formset = KonditionFormSetEdit(request.POST, queryset=kondition)
        weaDetail_formset = WeaDetailFormSetEdit(request.POST, queryset=weaDetail)
        if weaPreis_form.is_valid() and kondition_formset.is_valid() and weaDetail_formset.is_valid():
            weaPreis_form.save()
            kondition_formset.save()
            weaDetail_formset.save()
            return redirect("weapreisDetailsAnzeigen", pk=quelle.pk)  # Anpassen an die richtige URL
    else:
        weaPreis_form = WeaPreisForm(instance=weaPreisDetail)
        kondition_formset = KonditionFormSet(instance=weaPreisDetail)
        weaDetail_formset = WeaDetailFormSet(instance=weaPreisDetail)

    context = {
        'weaPreis_form': weaPreis_form,
        'kondition_formset': kondition_formset,
        'weaDetail_formset': weaDetail_formset,
        'weaPreisDetail': weaPreisDetail,
        'quelle': quelle,
        'angebote': angebote,
        'vertraege': vertraege,
        'schaetzungen': schaetzungen,
        'indikationen': indikationen,
        'quelleDocs': quelleDocs,
    }

    return render(request, "weaeinkauf/weapreisDetailsBearbeiten.html", context)


@user_passes_test(group_check_edit, login_url="/")
def weapreisDetailsLoeschen(request, pk):
    weaPreisDetail = get_object_or_404(WeaPreis, pk=pk)
    weaPreisDetail.delete()
    return redirect("weapreiseAnzeigen", pk=weaPreisDetail.pk)

@user_passes_test(group_check_edit, login_url="/")
@login_required(login_url="/login/")
def weapreisHinzufuegen(request, pk):
    quelle = get_object_or_404(Quelle, pk=pk)
    angebote = Angebot.objects.filter(quelle=quelle)
    vertraege = Vertrag.objects.filter(quelle=quelle)
    schaetzungen = Schaetzung.objects.filter(quelle=quelle)
    indikationen = Indikation.objects.filter(quelle=quelle)
    quelleDocs = QuelleDoc.objects.filter(quelle=quelle)
    
    if request.method == "POST":
        weaPreis_form = WeaPreisForm(request.POST)
        kondition_formset = KonditionFormSet(request.POST)
        weaDetail_formset = WeaDetailFormSet(request.POST)
        if weaPreis_form.is_valid() and kondition_formset.is_valid() and weaDetail_formset.is_valid():
            weapreis = weaPreis_form.save(commit=False)
            weapreis.quelle = quelle
            weapreis.save()
            kondition_formset.instance = weapreis
            kondition_formset.save()
            weaDetail_formset.instance = weapreis
            weaDetail_formset.save()
            return redirect("quellenDetailsAnzeigen", pk=quelle.pk)  # Anpassen an die richtige URL
    else:
        weaPreis_form = WeaPreisForm()
        kondition_formset = KonditionFormSet()
        weaDetail_formset = WeaDetailFormSet()

    context = {
        'weaPreis_form': weaPreis_form,
        'kondition_formset': kondition_formset,
        'weaDetail_formset': weaDetail_formset,
        'quelle': quelle,
        'angebote': angebote,
        'vertraege': vertraege,
        'schaetzungen': schaetzungen,
        'indikationen': indikationen,
        'quelleDocs': quelleDocs,
    }
    return render(request, "weaeinkauf/weapreisHinzufuegen.html", context)

@user_passes_test(group_check_edit, login_url="/")
@login_required(login_url="/login/")
def servicepreisHinzufuegen(request):
    quellen_anzeigen_list = Quelle.objects.all()
    context={"quellen_anzeigen_list": quellen_anzeigen_list}
    return render(request, "weaeinkauf/servicepreisHinzufuegen.html", context)

@login_required(login_url="/login/")
@user_passes_test(group_check, login_url="/")
def servicepreiseAnzeigen(request):
    servicepreise_anzeigen_list =getAllServicepreise()
    combined_data_servicepreise = combined_list_servicepreise(request)  # combined_list aufrufen und die kombinierten Daten erhalten

    # Anzahl der Elemente pro Seite festlegen
    paginator = Paginator(combined_data_servicepreise, 10)  # 10 Elemente pro Seite

    # Aktuelle Seitenzahl aus der URL holen
    page_number = request.GET.get('page')
    page_obj_servicepreise = paginator.get_page(page_number)

    context={"servicepreise_anzeigen_list": servicepreise_anzeigen_list, "servicepreise_count": len(servicepreise_anzeigen_list), "page_obj_servicepreise": page_obj_servicepreise}
    return render(request, "weaeinkauf/servicepreiseAnzeigen.html", context)



