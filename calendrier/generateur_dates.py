from datetime import date
from enum import Enum, unique
from typing import List, Tuple


@unique
class JourSemaine(Enum):
    """
    Jours de la semaine
    """
    LUNDI = 0
    MARDI = 1
    MERCREDI = 2
    JEUDI = 3
    VENDREDI = 4
    SAMEDI = 5
    DIMANCHE = 6


@unique
class NomMois(Enum):
    """
    Noms des mois
    """
    JANVIER = 0
    FEVRIER = 1
    MARS = 2
    AVRIL = 3
    MAI = 4
    JUIN = 5
    JUILLET = 6
    AOUT = 7
    SEPTEMBRE = 8
    OCTOBRE = 9
    NOVEMBRE = 10
    DECEMBRE = 11


class Jour:
    def __init__(self, jour_mois, jour_semaine: JourSemaine, mois: int, mois_appartenance: int):
        self.jour_mois = jour_mois
        self.jour_semaine = jour_semaine
        self.mois = mois
        self.mois_appartenance = mois_appartenance

    def est_dimanche(self):
        return self.jour_semaine == JourSemaine.DIMANCHE

    def etrangere(self) -> bool:
        return self.mois != self.mois_appartenance


class Semaine:
    def __init__(self, jours: List[Jour] = None):
        self.jours = jours if jours else []


class Mois:
    def __init__(self, nom_mois: NomMois, semaines: List[Semaine] = None, annee: int = None):
        self.semaines = semaines if semaines else []
        self.nom_mois = nom_mois
        self.annee = annee


class Annee:
    def __init__(self, annee, mois: List[Mois] = None):
        self.mois = mois if mois else []
        self.annee = annee


def _modulo_plus_valeur(valeur_depart: int, delta: int, base: int):
        mois_delta = valeur_depart + delta
        if mois_delta < 0:
            return mois_delta % base, -abs(mois_delta // base)
        else:
            return mois_delta % base, mois_delta // base


def _mois_annee_plus_valeur(mois: int, annee: int, delta_mois: int):
    valeur = _modulo_plus_valeur(mois, delta_mois, 12)
    return valeur[0], annee + valeur[1]


def _jour_plus(jour: int, delta: int = 1):
    return _modulo_plus_valeur(jour, delta=delta, base=7)[0]


def __calcul_jours_mois(numero_mois0: int, annee: int) -> int:
    if numero_mois0 >= 0:
        nummero_mois = numero_mois0 + 1
    else:
        nummero_mois = 12 - numero_mois0 + 1

    if nummero_mois in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif nummero_mois == 2:
        return 29 if annee % 4 == 0 else 28
    else:
        return 30


def _generateur_mois(mois: int, annee: int,
                     jour_sem_1er_du_mois: int = 0) -> List[List[Tuple[int]]]:
    """
    Le "coeur" de notre systeme de generation de dates.
     - permet de générer les semaines d'un mois/année donné à partir de son jour de debut et en
     s'aidant d'un générateur de jours/numeros de semaine (une fonction qui renvoie à l'infini
     une serie LMMJVSD assortie du numero de la semaine

    :param mois: le n° de mois (pour simplifier l'agorithme les mois sont numerotées de 0 à 11)
    :param annee: l'année (permet de calculer le nombre des jour dans le mois surtout pour le mois de fevrier)
    :param jour_sem_1er_du_mois: jour de la semaine avec laquelle commence le mois (ex. un Mardi)
    :param generateur_jours_semaine: générateur de jours/numeros de semaine - permet d'utiliser un générateur unique pour l'anée afin de numeroter les semaines si besoin
    :return:
    """
    liste_semaines: List[List[Tuple[int]]] = [[], [], [], [], [], []]
    jour_semaine = 0
    semaine = 0
    # on demarre la semaine avec les jours de la semaine precedente si le mois ne commence pas un Lundi
    if jour_sem_1er_du_mois:
        mois_precedent, annee_precedent = _mois_annee_plus_valeur(mois, annee, -1)
        jours_mois_precedent = __calcul_jours_mois(mois_precedent, annee)
        for j in range(jour_sem_1er_du_mois):
            liste_semaines[semaine].append((jours_mois_precedent - jour_sem_1er_du_mois + j + 1, jour_semaine, mois_precedent, annee_precedent))
            jour_semaine = _jour_plus(jour_semaine)

    # on ajoute les jours du mois
    jours_mois = __calcul_jours_mois(mois, annee)
    for jour in range(jours_mois):
        liste_semaines[semaine].append((jour + 1, jour_semaine, mois, annee))
        jour_semaine = _jour_plus(jour_semaine)
        if jour_semaine == 0:
            semaine = semaine + 1

    # noinspection PyUnboundLocalVariable
    # completer la derniere semaine avec les jours du mois suivant si le mois ne se termine pas par un Dimanche
    if jour_semaine > 0:
        mois_suivant, annee_suivant = _mois_annee_plus_valeur(mois, annee, 1)
        for j in range(7 - jour_semaine):
            liste_semaines[semaine].append((j + 1, jour_semaine, mois_suivant, annee_suivant))
            jour_semaine = _jour_plus(jour_semaine)

    if not liste_semaines[-1]:
        liste_semaines.pop()

    return liste_semaines


def __calculer_jour_semaine_1er_janv(annee: int):
    d = date(annee, 1, 1)
    return d.weekday()


def _generateur_annee(annee) -> List:
    jour_sem_mois_start = __calculer_jour_semaine_1er_janv(annee)
    mois_annee = []
    for no_mois in range(12):
        mois = _generateur_mois(no_mois, annee, jour_sem_mois_start)
        mois_annee.append(mois)

        dernier_jour_mois = max(mois[-1], key=lambda jour: jour[0])
        jour_sem_mois_start = _jour_plus(dernier_jour_mois[1], delta=1)

    return mois_annee


def annee(annee: int) -> Annee:
    calendrier = _generateur_annee(annee)

    return Annee(annee, [
        mois(no_mois, annee, calendrier[no_mois])
        for no_mois in range(12)
    ])


def mois(mois, annee, list_semaines_mois: List[List[Tuple[int]]]) -> Mois:
    return Mois(NomMois(mois),
                [
                    Semaine([Jour(j[0], JourSemaine(j[1]), j[2], mois) for j in sem])
                    for sem in list_semaines_mois
                ], annee)
