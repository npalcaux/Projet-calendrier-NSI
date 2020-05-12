from datetime import date
from enum import Enum, unique
from typing import List, Tuple, Generator


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


def _modulo_plus_valeur(valeur_depart: int, delta: int, base: int):
        mois_delta = valeur_depart + delta
        if mois_delta < 0:
            return mois_delta % base, -abs(mois_delta // base)
        else:
            return mois_delta % base, mois_delta // base


def _mois_annee_plus_valeur(mois: int, annee: int, delta_mois: int):
    valeur = _modulo_plus_valeur(mois, delta_mois, 12)
    return valeur[0], annee + valeur[1]


def _jour_plus(jour: int, delta: int):
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


def generateur_jour_semaine() -> Generator[Tuple, None, None]:
    no_semaine = 0
    while True:
        for i in range(7):
            yield i, no_semaine
        no_semaine = no_semaine + 1


def generateur_mois(mois: int, annee: int,
                    jou_sem_start: int = 0,
                    generateur_jours_semaine=generateur_jour_semaine()) -> Generator[Tuple, None, None]:
    """
    Le "coeur" de notre systeme de generation de dates.
     - permet de générer les semaines d'un mois/année donné à partir de son jour de debut et en
     s'aidant d'un générateur de jours/numeros de semaine (une fonction qui renvoie à l'infini
     une serie LMMJVSD assortie du numero de la semaine

    :param mois: le n° de mois (pour simplifier l'agorithme les mois sont numerotées de 0 à 11)
    :param annee: l'année (permet de calculer le nombre des jour dans le mois surtout pour le mois de fevrier)
    :param jou_sem_start: jour de la semaine avec laquelle commence le mois (ex. un Mardi)
    :param generateur_jours_semaine: générateur de jours/numeros de semaine - permet d'utiliser un générateur unique pour l'anée afin de numeroter les semaines si besoin
    :return:
    """
    semaine: List[Tuple] = []

    # on cherche les jours de la semaine precedente si le mois ne commence pas un Lundi
    if jou_sem_start:
        mois_precedent, annee_precedent = _mois_annee_plus_valeur(mois, annee, -1)
        jours_mois_precedent = __calcul_jours_mois(mois_precedent, annee)
        for j in range(jou_sem_start):
            jour_sem, no_sem = next(generateur_jours_semaine)
            semaine.append((jours_mois_precedent - jou_sem_start + j + 1, jour_sem, no_sem, mois_precedent, annee_precedent))

    jours_mois = __calcul_jours_mois(mois, annee)
    for jour in range(jours_mois):
        jour_semaine, no_semaine = next(generateur_jours_semaine)
        semaine.append((jour + 1, jour_semaine, no_semaine, mois, annee))
        if jour_semaine == 6:
            yield semaine
            # s'il en restent des jours dans le mois on ajoute une semaine
            if jour < jours_mois-1:
                semaine = []

    # noinspection PyUnboundLocalVariable
    # completer la semaine si le mois ne se termine pas par un Dimanche
    if jour_semaine < 6:
        mois_suivant, annee_suivant = _mois_annee_plus_valeur(mois, annee, 1)
        for j in range(6 - jour_semaine):
            jour_sem, no_sem = next(generateur_jours_semaine)
            semaine.append((j + 1, jour_sem, no_sem-1, mois_suivant, annee_suivant))
        yield semaine


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
    def __init__(self, no_semaine, jours: List[Jour] = None):
        self.jours = jours if jours else []
        self.no_semaine = no_semaine

class Mois:
    def __init__(self, nom_mois: NomMois, semaines: List[Semaine] = None, annee: int = None):
        self.semaines = semaines if semaines else []
        # s'assurer que la liste de semaines est trié
        self.semaines.sort(key=lambda semaine: semaine.no_semaine)
        self.nom_mois = nom_mois
        self.annee = annee

class Annee:
    def __init__(self, annee, mois: List[Mois] = None):
        self.liste_mois = mois if mois else []
        self.annee = annee


def __calculer_jour_semaine_1er_janv(annee: int):
    d = date(annee, 1, 1)
    return d.weekday()


def generateur_annee(annee) -> Generator[Tuple, None, None]:
    jour_sem_mois_start = __calculer_jour_semaine_1er_janv(annee)
    gen_jour_sem = generateur_jour_semaine()
    for no_mois in range(12):
        mois = [semaine for semaine in generateur_mois(no_mois, annee, jour_sem_mois_start, gen_jour_sem)]
        yield mois
        dernier_jour_mois = max(mois[-1], key=lambda jour: jour[0])
        jour_sem_mois_start = _jour_plus(dernier_jour_mois[1], delta=1)


def annee(annee: int):
    calendrier = [jour for jour in generateur_annee(annee)]

    return Annee(annee, [
        Mois(NomMois(mois),
             [
                 Semaine(sem[0][2], [Jour(j[0], JourSemaine(j[1]), j[3], mois) for j in sem])
                 for sem in calendrier[mois]
             ], annee)
        for mois in range(12)
    ])
