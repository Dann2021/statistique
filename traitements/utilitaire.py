import ast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def transformeur(
    chaine,
):  # cette fonction prendra une chaine de tulpe et la transformera en tableau numpy de classe

    # ici on convertit la chaine en liste
    liste = chaine.split(" ")

    # transormation en data de classe
    message: str = ""
    data: list = []
    try:
        data = [np.array(ast.literal_eval(classe)) for classe in liste]
    except SyntaxError:
        message += "Erreur de syntaxe, verifiez bien les données saisies dans les classes"  # message à afficher lorsque se produit en erreur de syntaxe

    # print(data)

    # renvoi d'un tableau
    return data, message


def transformeur_liste(chaine):
    # ici on convertit la chaine en liste dans le cas des effectifs
    liste = chaine.split(" ")
    message: str = ""
    entiers: list = []
    try:
        entiers = [int(nombre) for nombre in liste]
    except ValueError:
        message += "Erreur dans la saisie des effectifs"

    return np.array(liste), entiers, message


def parcours_tableau(
    data,
):  # Fonction pour permettre un affichage de donnees en mode (a,b) dans un  dataframe
    message: str = ""
    try:
        a, b = [], []  # Liste des a et des b
        for couple in data:
            try:
                ca = couple[0]
                cb = couple[1]
                a.append(ca)
                b.append(cb)
            except (IndexError, TypeError):
                message += (
                    "Erreur : Les données doivent être sous forme de tuples (a,b)"
                )
    except Exception as e:
        message += f"L'erreur est : {e}"

    return a, b, message


def amplitude(a, b):  # calcul des amplitudes
    am = []  # Tableau pour recevoir les amplitudes
    for va, vb in zip(a, b):
        valeur = vb - va
        valeur = np.around(valeur, 2)  # arrondie à deux chiffre après la virgule
        am.append(valeur)
    return am


def verification_amplitudes(tableau):
    test = len(set(tableau)) == 1
    if test:
        return (
            "Les amplitudes sont égales",
            0,
        )  # ici on ajoute une seconde valeur de retour pour verifier le resultat

    return "Les amplitudes sont inégales", 1


def correction_hauteur(bool, ampli):
    data = []
    if bool:  # Si les amplitudes sont inégales on les corrige
        minimum = min(ampli)
        data = [(v / minimum) for v in ampli]
        return np.array(data)


def effectif_corrige(effectif, ai):
    data = []
    for e, a in zip(effectif, ai):
        v = float(e) / float(a)
        data.append(v)
    return np.array(data)


# Fonctions pour avoir le mode ou les modes
def mode(tableau):
    message = "Cette serie statistique admet un mode"

    mode = max(tableau)
    index = tableau.index(mode)
    return mode, index, message


def mode2(a, b, e):
    dico: dict = {}
    maxi = max(e)
    index = e.index(maxi)
    count = e.count(maxi)
    l1, l2 = [], []
    if count == 1:
        c1, c2 = a[index], b[index]
        print(f"La classe modale est : [{c1};{c2}]")
        return c1, c2
    else:
        print("Il y a plusieurs classes modales")
        # parcourt des effectifs pour enregistrer les index
        index_max = [i for i, v in enumerate(e) if v == maxi]

        print(f"index_max : {index_max}")
        i = 0
        while i < len(index_max):
            c1, c2 = a[index_max[i]], b[index_max[i]]
            print(f"La classe modale est : [{c1};{c2}] dont l'effectif est {maxi}")
            l1.append(c1)
            l2.append(c2)
            dico.update({"a": l1, "b": l2, "effectif": maxi})
            i += 1
        return c1, c2, dico


def mode_multiple(a, b, e):
    dico: dict = {}  # Dictionnaire que la fonction retournera

    # Le mode est l'effectif le plus élévé dans une serie statistique
    # donc on prendra le maximum de l'effectif (e)

    maximum = max(e)

    # ici on souhaite maintenant connaitre l'index de ce maximum
    index = e.index(maximum)

    # creation de listes qui contiendront les classe
    l1, l2 = [], []  # l1 pour a et l2 pour b

    # creation d'une variable pour afficher un message
    message = "Cette serie statistique est multi modale"

    # parcourt des effectif pour enregistrer leur index

    index_max = [i for i, v in enumerate(e) if v == maximum]

    # parcourt de index_max pour connaitre les positions des classes des effectifs trouvés
    i = 0
    while i < len(index_max):
        c1, c2 = (
            a[index_max[i]],
            b[index_max[i]],
        )  # on capture les bornes des classe à partir des index

        l1.append(c1)  # on enregistre ces classes dans des listes
        l2.append(c2)
        dico.update({"a": l1, "b": l2, "mode": maximum})
        i += 1
    return message, dico


def centre_classe(a, b):
    tableau = [((va + vb) / 2) for va, vb in zip(a, b)]
    return np.array(tableau)


# calcul des frequences et effectif
def cumules(liste, cat):

    # frequence simples
    tableau = [float(v) for v in liste]
    total = np.sum(tableau)
    s = 0
    i = 0

    if cat == "feq":
        f = [v / total for v in tableau]

        # frequences cumulées

        fc = []  # croissant
        fd = []  # decroissant

        for v in f:
            s += v
            fc.append(s)

        i = 0
        while i < len(f):
            fd.append(fc[-1])
            fc[-1] -= f[i]

        return f, np.array(fc), np.array(fd)

    elif cat == "eff":
        nc, nd = [], []
        for v in tableau:
            s += int(v)
            nc.append(s)

        while i < len(tableau):
            nd.append(nc[-1])
            nc[-1] -= tableau[i]

            i += 1

        return np.array(nc), np.array(nd)
    else:
        return "Nous sommes dans la fonctions frequences, ceci se produit car cette catégorie n'existe pas"


# fonction pour retourner un dataframe en fonction de verification des amplitues


def dataframe_dynamique(valeur_retour, a, b, effectif, amp, ai, ec, centre):

    # creation des listes pour les effectifs cumulés
    # nc, nd = [], []  # Effectif cumulé croissant et décroissant
    # sc = 0

    # for vc in effectif:
    #    sc += int(vc)
    #    nc.append(sc)
    # ici pour faire les effectifs cumulés croissants, on prend d'abord le maximum du nc
    # total = max(nc)

    # ajout de la frequence
    f, fc, fd = cumules(effectif, cat="feq")
    nc, nd = cumules(effectif, cat="eff")

    if valeur_retour == 0:
        dico = {
            "a": a,
            "b": b,
            "n": effectif,
            "n+": nc,
            "n-": nd,
            "f": f,
            "f+": fc,
            "f-": fd,
            "amplitude": amp,
            "ai": ai,
            "xi": centre,
        }
        return dico
    dico2 = {
        "a": a,
        "b": b,
        "n": effectif,
        "n+": nc,
        "f": f,
        "f+": fc,
        "amplitude": amp,
        "ai": ai,
        "ec": ec,
        "xi": centre,
    }

    return dico2
