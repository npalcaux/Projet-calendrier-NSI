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


def __calcul_jours_mois(numero_mois0: int, annee: int) -> int:
    nummero_mois = numero_mois0 + 1
    if nummero_mois in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif nummero_mois == 2:
        return 29 if annee % 4 == 0 else 28
    else:
        return 30


def generateur_jour_semaine() -> Generator[int, None, None]:
    no_semaine = 0
    while True:
        for i in range(7):
            yield i, no_semaine
        no_semaine = no_semaine + 1


def generateur_calendrier(annee: int, jou_sem_start: int) -> Generator[Tuple, None, None]:
    jour_semaine_gen = generateur_jour_semaine()

    for j in range(jou_sem_start):
        jour_sem, no_sem = next(jour_semaine_gen)
        yield 31 - jou_sem_start + j+1, jour_sem, no_sem, 11, annee-1

    for mois_courrante in range(12):
        nombre_jours = __calcul_jours_mois(mois_courrante, annee)
        for jour in range(nombre_jours):
            jour_semaine, no_semaine = next(jour_semaine_gen)
            yield jour+1, jour_semaine, no_semaine, mois_courrante, annee

    # noinspection PyUnboundLocalVariable
    for j in range(7 - jour_semaine - 1):
        jour_sem, no_sem = next(jour_semaine_gen)
        yield j + 1, jour_sem, no_sem, 0, annee + 1

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


def annee(annee: int):
    jour_semaine_1er_janvier = __calculer_jour_semaine_1er_janv(annee)
    calendrier = [jour for jour in generateur_calendrier(annee, jour_semaine_1er_janvier)]

    return Annee(annee, [
        Mois(NomMois(mois),
             [
                 Semaine(sem, [Jour(j[0], JourSemaine(j[1]), j[3], mois) for j in calendrier if j[2] == sem])
                 for sem in set(j[2] for j in calendrier if j[3] == mois and j[4] == annee)
             ], annee)
        for mois in range(12)
    ])
