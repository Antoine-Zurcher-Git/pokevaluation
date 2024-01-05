from collectionData import *


def report(data: Collection, errorLinkNotFoundName):
    nTopCarte = 50
    topCarte = []
    valeurTotale = 0
    nbCarte = 0
    nbCarteMissed = 0
    intervals = [0.04, 0.09, 0.20, 0.49, 1.5, 10, 20, 50, 100, 200, 1000]
    cartesInIntervals = [ [] for i in range(len(intervals))]

    for serie in data.data:
        for carte in serie["pkm_poss_info"]:
            if "prix_txt" in carte and carte["prix_txt"] != errorLinkNotFoundName:
                prix = int(float(carte["prix_txt"].replace(" €","").replace(",","."))*100)
                carte["prix"] = prix
                carte["serie"] = serie["name"]

                valeurTotale += prix
                nbCarte += 1
                for iInter, inter in enumerate(intervals):
                    if prix/100.0 < inter:
                        cartesInIntervals[iInter].append(carte)
                        break
                if len(topCarte) == 0:
                    topCarte.append(carte)
                elif prix > topCarte[-1]["prix"]:
                    for iCarte in range(len(topCarte)):
                        if prix > topCarte[iCarte]["prix"]:
                            topCarte.insert(iCarte, carte)
                            break
                while len(topCarte) > nTopCarte:
                    topCarte.pop(len(topCarte)-1)
            else:
                nbCarteMissed += 1

    populationParInterval = [len(d) for d in cartesInIntervals]
    
    print(str(nbCarte) + " cartes analysées")
    print(str(nbCarteMissed) + " cartes manquées")
    print("Valeur Totale : "+str(valeurTotale/100.0))
    print("Population par interval : ")
    for i in range(len(intervals)):
        depart = 0
        if i > 0:
            depart = intervals[i-1]
        arrivee = intervals[i]
        population = populationParInterval[i]
        print(f"[{depart}, {arrivee}] -> {population} cartes")
    print(f"Top {nTopCarte} des cartes :")
    for i in range(len(topCarte)):
        nom = topCarte[i]["name"]
        prix = topCarte[i]["prix"]/100.0
        serie = topCarte[i]["serie"]
        print(f"{i+1} - {nom} : {prix} € (serie : {serie})")

