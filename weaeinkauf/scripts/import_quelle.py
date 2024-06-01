from datetime import datetime
from wea.settings import BASE_DIR
from weaeinkauf.models import Quelle, Vertrag, Angebot, Indikation, Schaetzung, QuelleDoc, ServicePreis, ServicePreisVerguetung, WeaPreis, PreisKondition, WeaFundament, WeaDetail
import csv
import os 

def run():
    file_path_quelle = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufQuelle.csv")
    file_path_angebot = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufAngebot.csv")
    file_path_indikation = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufIndikation.csv")
    file_path_schaetzung = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufSchaetzung.csv")
    file_path_vertrag = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufVertrag.csv")

    file_path_quelleDoc = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufQuelleDoc.csv")
    file_path_servicePreis = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufServicepreis.csv")
    file_path_servicePreisVerguetung = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufServicepreisVerguetung.csv")
    file_path_weaPreis = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufWeaPreis.csv")
    file_path_preisKondition = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufKondition.csv")
    file_path_weaFundament = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufFundament.csv")
    file_path_weaDetail = os.path.join(BASE_DIR, "weaeinkauf", "resources", "eObjEinkaufWeaDetail.csv")


    quellen = {}
    service_Preis = {}
    wea_Preis = {}

    with open(file_path_quelle, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            alt_id = int(row[0])
            name = row[1]
            quellendatum = row[2]
            bemerkung = row[3]
            created_by = row[4]
            created_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M').astimezone()
            quelle = Quelle.objects.create(alt_id=alt_id, name=name, quellendatum=quellendatum, bemerkung=bemerkung, created_by=created_by, created_at=created_at)
            quellen[alt_id] = quelle # Store quelle in dictionary with alt_id as key
    
    #Then, import Angebot-Daten, linking them to quellen using the dictionary
    with open(file_path_angebot,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            quellendatum = row[2]
            bemerkung = row[3]
            created_by = row[4]
            created_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M').astimezone()
            quellen_id = int(row[6])
            angebotskennung = row[7]
            wetterrisiko = row[8]

            # Check if quellen_id exists in the dictionary
            if quellen_id in quellen:
                angebot = Angebot.objects.create(name=name, quellendatum=quellendatum, bemerkung=bemerkung, created_by=created_by, created_at=created_at, quellen_id=quellen_id, 
                                                 wetterrisiko=wetterrisiko, angebotskennung=angebotskennung, quelle=quellen[quellen_id])
            else:
                print(f"Quelle mit id {quellen_id} in Angebot nicht gefunden.")

    
    with open(file_path_indikation,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            quellendatum = row[2]
            bemerkung = row[3]
            created_by = row[4]
            created_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M').astimezone()
            quellen_id = int(row[6])

            # Check if quellen_id exists in the dictionary
            if quellen_id in quellen:
                indikation = Indikation.objects.create(name=name, quellendatum=quellendatum, bemerkung=bemerkung, created_by=created_by, created_at=created_at, quellen_id=quellen_id, quelle=quellen[quellen_id])
            else:
                print(f"Quelle mit id {quellen_id} in Indikation nicht gefunden.")

    with open(file_path_schaetzung,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            quellendatum = row[2]
            bemerkung = row[3]
            created_by = row[4]
            created_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M').astimezone()
            quellen_id = int(row[6])
            schaetzer = row[7]

            # Check if quellen_id exists in the dictionary
            if quellen_id in quellen:
                schaetzung = Schaetzung.objects.create(name=name, quellendatum=quellendatum, bemerkung=bemerkung, created_by=created_by, created_at=created_at, 
                                                       quellen_id=quellen_id, quelle=quellen[quellen_id], schaetzer=schaetzer)
            else:
                print(f"Quelle mit id {quellen_id} in Schätzung nicht gefunden.")

    with open(file_path_vertrag,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            quellendatum = row[2]
            bemerkung = row[3]
            created_by = row[4]
            created_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M').astimezone()
            quellen_id = int(row[6])
            vertragskennung = row[7]
            wetterrisiko = row[8]
            lieferzeit = row[9]
            vertragsart = row[10]
            sonderkuendigungsrecht = row[11]
            vertragsbeginn = row[12]
            
            # Check if quellen_id exists in the dictionary
            if quellen_id in quellen:
                # Check if vertragsbeginn is empty
                if vertragsbeginn != "":
                    vertrag = Vertrag.objects.create(name=name, quellendatum=quellendatum, bemerkung=bemerkung, created_by=created_by, created_at=created_at, 
                                                 quellen_id=quellen_id, vertragskennung=vertragskennung,  quelle=quellen[quellen_id], wetterrisiko=wetterrisiko, 
                                                 lieferzeit=lieferzeit, vertragsart=vertragsart, sonderkuendigungsrecht=sonderkuendigungsrecht, vertragsbeginn=vertragsbeginn)

                else:
                    vertrag = Vertrag.objects.create(name=name, quellendatum=quellendatum, bemerkung=bemerkung, created_by=created_by, created_at=created_at, 
                                                 quellen_id=quellen_id, vertragskennung=vertragskennung,  quelle=quellen[quellen_id], wetterrisiko=wetterrisiko, 
                                                 lieferzeit=lieferzeit, vertragsart=vertragsart, sonderkuendigungsrecht=sonderkuendigungsrecht)
            else:
                print(f"Quelle mit id {quellen_id} in Vertrag nicht gefunden.")

    #Then, import Angebot-Daten, linking them to quellen using the dictionary
    with open(file_path_quelleDoc,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            filename = row[2]
            created_by = row[4]
            created_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M').astimezone()
            quellen_id = int(row[3])

            # Check if quellen_id exists in the dictionary
            if quellen_id in quellen:
                quelleDoc = QuelleDoc.objects.create(name=name, filename=filename, created_by=created_by, created_at=created_at, quellen_id=quellen_id, 
                                                 quelle=quellen[quellen_id])
            else:
                print(f"Quelle mit id {quellen_id} in Quellen Doc nicht gefunden.")

    
    with open(file_path_servicePreis,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            alt_id = int(row[0])
            name = row[1]
            laufzeit = row[2]
            bemerkung = row[3]
            created_by = row[4]
            created_at = datetime.strptime(row[5], '%Y-%m-%d %H:%M').astimezone()
            quellen_id = int(row[6])
            basisjahr = row[7]
            grenzwert = row[8]
            kuendigungsrecht = row[9]

            # Check if quellen_id exists in the dictionary
            if quellen_id in quellen:
                # Check if grenzwert is empty
                if grenzwert != "":
                    servicePreis = ServicePreis.objects.create(alt_id=alt_id, name=name, laufzeit=laufzeit, bemerkung=bemerkung, created_by=created_by, created_at=created_at, quellen_id=quellen_id,
                                                            basisjahr=basisjahr, grenzwert=grenzwert, kuendigungsrecht=kuendigungsrecht, quelle=quellen[quellen_id])
                    service_Preis[alt_id] = servicePreis

                else:
                    servicePreis = ServicePreis.objects.create(alt_id=alt_id, name=name, laufzeit=laufzeit, bemerkung=bemerkung, created_by=created_by, created_at=created_at, quellen_id=quellen_id,
                                                            basisjahr=basisjahr, kuendigungsrecht=kuendigungsrecht, quelle=quellen[quellen_id])
                    service_Preis[alt_id] = servicePreis
            else:
                print(f"Quelle mit id {quellen_id} in Service-Preis nicht gefunden.")

    with open(file_path_servicePreisVerguetung,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            servicePreisID = int(row[2])
            jahr = row[3]
            indexierung = row[4]
            bemerkung = row[5]
            var = row[6]
            fix = row[7]
            minPreis = row[8]

            # Check if servicePreis_id exists in the dictionary
            if servicePreisID in service_Preis:
                # Check if indexierung is empty
                if indexierung != "":
                    # Check if minPreis is empty
                    if minPreis != "":
                        # Check if var is empty
                        if var != "":
                            # Check if fix is empty
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                           var=var, fix=fix, minPreis=minPreis, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                           var=var, minPreis=minPreis, servicePreis=service_Preis[servicePreisID])

                        else:
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                            fix=fix, minPreis=minPreis, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                            minPreis=minPreis, servicePreis=service_Preis[servicePreisID])
                    else:
                        if var != "":
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                           var=var, fix=fix, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                           var=var, servicePreis=service_Preis[servicePreisID])
                        else:
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                            fix=fix, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, indexierung=indexierung, 
                                                                                             servicePreis=service_Preis[servicePreisID])
                else:
                    if minPreis != "":
                        if var != "":
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                           var=var, fix=fix, minPreis=minPreis, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                           var=var, minPreis=minPreis, servicePreis=service_Preis[servicePreisID])
                        else:
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                            fix=fix, minPreis=minPreis, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                            minPreis=minPreis, servicePreis=service_Preis[servicePreisID])
                    else:
                        if var != "":
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                           var=var, fix=fix, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                           var=var, servicePreis=service_Preis[servicePreisID])
                        else:
                            if fix != "":
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                            fix=fix, servicePreis=service_Preis[servicePreisID])
                            else:
                                servicePreisVerguetung = ServicePreisVerguetung.objects.create(name=name, servicePreisID=servicePreisID, bemerkung=bemerkung, jahr=jahr, 
                                                                                             servicePreis=service_Preis[servicePreisID])
            else:
                print(f"Service Preis mit id {servicePreisID} in Service Preis Verguetung nicht gefunden.")

    with open(file_path_weaPreis,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            alt_id = int(row[0])
            name = row[1]
            weaTyp_id = row[2]
            preis = row[3]
            waehrung = row[4]
            transportkosten = row[5]
            gueltigkeit = row[6]
            garantie_verfuegbarkeit = row[7]
            created_by = row[8]
            created_at = datetime.strptime(row[9], '%Y-%m-%d %H:%M').astimezone()
            quellen_id = int(row[10])
            preis_w_fundament = row[11]

            # Check if quellen_id exists in the dictionary
            if quellen_id in quellen:
                # Check if transportkosten is empty
                if transportkosten != "":
                    # Check if gueltigkeit is empty
                    if gueltigkeit != "":
                        weaPreis = WeaPreis.objects.create(alt_id=alt_id, name=name, weaTyp_id=weaTyp_id, preis=preis, created_by=created_by, created_at=created_at, 
                                                           quellen_id=quellen_id, waehrung=waehrung,  quelle=quellen[quellen_id], transportkosten=transportkosten, 
                                                           gueltigkeit=gueltigkeit, garantie_verfuegbarkeit=garantie_verfuegbarkeit, preis_w_fundament=preis_w_fundament)
                        wea_Preis[alt_id] = weaPreis

                    else:
                        weaPreis = WeaPreis.objects.create(alt_id=alt_id, name=name, weaTyp_id=weaTyp_id, preis=preis, created_by=created_by, created_at=created_at, 
                                                           quellen_id=quellen_id, waehrung=waehrung,  quelle=quellen[quellen_id], transportkosten=transportkosten, 
                                                           garantie_verfuegbarkeit=garantie_verfuegbarkeit, preis_w_fundament=preis_w_fundament)
                        wea_Preis[alt_id] = weaPreis
                    
                else:
                    if gueltigkeit != "":
                        weaPreis = WeaPreis.objects.create(alt_id=alt_id, name=name, weaTyp_id=weaTyp_id, preis=preis, created_by=created_by, created_at=created_at, 
                                                           quellen_id=quellen_id, waehrung=waehrung,  quelle=quellen[quellen_id], 
                                                           gueltigkeit=gueltigkeit, garantie_verfuegbarkeit=garantie_verfuegbarkeit, preis_w_fundament=preis_w_fundament)
                        wea_Preis[alt_id] = weaPreis

                    else:
                        weaPreis = WeaPreis.objects.create(alt_id=alt_id, name=name, weaTyp_id=weaTyp_id, preis=preis, created_by=created_by, created_at=created_at, 
                                                           quellen_id=quellen_id, waehrung=waehrung,  quelle=quellen[quellen_id], 
                                                           garantie_verfuegbarkeit=garantie_verfuegbarkeit, preis_w_fundament=preis_w_fundament)
                        wea_Preis[alt_id] = weaPreis
            else:
                print(f"Quelle mit id {quellen_id} in WEA-Preis nicht gefunden.")

    with open(file_path_preisKondition,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            weaPreisID = int(row[4])
            land = row[2]
            wea_anzahl = row[3]

            # Check if servicePreis_id exists in the dictionary
            if weaPreisID in wea_Preis:
                preisKondition = PreisKondition.objects.create(name=name, weaPreisID=weaPreisID, land=land, wea_anzahl=wea_anzahl, weaPreis=wea_Preis[weaPreisID])
            else:
                print(f"WEA-Preis mit id {weaPreisID} in Preis-Kondition nicht gefunden.")

    with open(file_path_weaFundament,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            weaPreisID = int(row[3])
            fundament_preis = row[2]

            # Check if servicePreis_id exists in the dictionary
            if weaPreisID in wea_Preis:
                weaFundament = WeaFundament.objects.create(name=name, weaPreisID=weaPreisID, fundament_preis=fundament_preis, weaPreis=wea_Preis[weaPreisID])
            else:
                print(f"WEA-Preis mit id {weaPreisID} in WEA-Fundament nicht gefunden.")

    with open(file_path_weaDetail,'r') as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            name = row[1]
            nabenhoehe = row[2]
            turmtyp = row[3]
            weaPreisID = int(row[7])
            auslaufdatum = row[4]
            genehmigungsunterlagen = row[5]
            windklasse = row[6]
            gesamthoehe = row[8]
            
            # Check if servicePreis_id exists in the dictionary
            if weaPreisID in wea_Preis:
                # Check if auslaufdatum is empty
                if auslaufdatum != "":
                    weaDetail = WeaDetail.objects.create(name=name, weaPreisID=weaPreisID, nabenhoehe=nabenhoehe, turmtyp=turmtyp, auslaufdatum=auslaufdatum, 
                                                         genehmigungsunterlagen=genehmigungsunterlagen, windklasse=windklasse, gesamthoehe=gesamthoehe, weaPreis=wea_Preis[weaPreisID])

                else:
                    weaDetail = WeaDetail.objects.create(name=name, weaPreisID=weaPreisID, nabenhoehe=nabenhoehe, turmtyp=turmtyp, 
                                                         genehmigungsunterlagen=genehmigungsunterlagen, windklasse=windklasse, gesamthoehe=gesamthoehe, weaPreis=wea_Preis[weaPreisID])
            else:
                print(f"WEA-Preis mit id {weaPreisID} in WEA-Detail nicht gefunden.")
            

