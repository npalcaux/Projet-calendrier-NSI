from datetime import date
from enum import Enum, unique
from typing import List, Tuple

from calendrier.gen_da import generateur_calendrier

NOM_MOIS = (
    "JANVIER",
    "FEVRIER",
    "MARS",
    "AVRIL",
    "MAI",
    "JUIN",
    "JUILLET",
    "AOUT",
    "SEPTEMBRE",
    "OCTOBRE",
    "NOVEMBRE",
    "DECEMBRE"
)

@unique
class JoursSemaine(Enum):
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


class Jour:
    def __init__(self, jour_mois, jour_semaine, mois: int, mois_appartenance: int):
        self.jour_mois = jour_mois
        self.jour_semaine = jour_semaine
        self.mois = mois
        self.mois_appartenance = mois_appartenance

    def est_dimanche(self):
        return self.jour_semaine == JoursSemaine.DIMANCHE.value

    def etrangere(self) -> bool:
        return self.mois != self.mois_appartenance

class Semaine:
    def __init__(self, no_semaine, jours: List[Jour] = None):
        self.jours = jours if jours else []
        self.no_semaine = no_semaine

class Mois:
    def __init__(self, no_mois, semaines: List[Semaine] = None, annee: int = None):
        self.semaines = semaines if semaines else []
        # s'assurer que la liste de semaines est trié
        self.semaines.sort(key=lambda semaine: semaine.no_semaine)
        self.no_mois = no_mois
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
        Mois(mois,
             [
                 Semaine(sem, [Jour(j[0], j[1], j[3], mois) for j in calendrier if j[2] == sem])
                 for sem in set(j[2] for j in calendrier if j[3] == mois and j[4] == annee)
             ], annee)
        for mois in range(12)
    ])
