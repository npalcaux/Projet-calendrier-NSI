from datetime import date
from enum import Enum, unique
from typing import List, Tuple

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

    def fin_semaine(self, semaine_complete: bool = False) -> List['JoursSemaine']:
        rest_semaine = [j for j in JoursSemaine if j.value >= self.value]
        return [None for _ in range(self.value)] + rest_semaine if semaine_complete else rest_semaine

    def jour_suivant(self) -> 'JoursSemaine':
        if self.value == 6:
            return JoursSemaine.LUNDI
        else:
            return JoursSemaine(self.value + 1)


class Jour:
    def __init__(self, jour_semaine: JoursSemaine, jour_mois: int):
        self.jour_sem: JoursSemaine = jour_semaine
        self.jour_mois = jour_mois

    def __str__(self) -> str:
        return f"{self.jour_sem} {self.jour_mois}"

    def est_dimanche(self):
        return self.jour_sem == JoursSemaine.DIMANCHE

    def est_vide(self):
        return self.jour_mois < 1


class Annee:
    def __init__(self, annee: int):
        self.annee = annee
        janv = self.__calculer_jour_semaine_prem_janv()
        self.liste_mois: List[Mois] = [Mois(0, self.__calcul_jours_mois(0), JoursSemaine(janv), annee)]

        mois_precedent = self.liste_mois[0]
        for i in range(1, 12):
            jour_sem_premier_jour_mois = JoursSemaine(mois_precedent.dernier_jour_du_mois().jour_sem.jour_suivant())
            nombre_jour_dans_le_mois = self.__calcul_jours_mois(i)
            mois = Mois(i, nombre_jour_dans_le_mois, jour_sem_premier_jour_mois, annee)

            self.liste_mois.append(mois)
            mois_precedent = mois

    def __calculer_jour_semaine_prem_janv(self):
        d = date(self.annee, 1, 1)
        return d.weekday()

    def __est_anne_bisextile(self):
        return self.annee % 4 == 0

    def __calcul_jours_mois(self, numero_mois0: int) -> int:
        nummero_mois = numero_mois0 + 1
        if nummero_mois in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif nummero_mois == 2:
            return 29 if self.__est_anne_bisextile() else 28
        else:
            return 30

class Semaine:
    def __init__(self, jour_semaine_start: JoursSemaine = JoursSemaine.LUNDI, jour_mois_start:int = 1, dernier_jour_du_mois:int = 31) -> None:
        self.numero_semaine:int
        self.jours: List[Jour] = []
        self.__remplir_jours(jour_mois_start, dernier_jour_du_mois, jour_semaine_start)
        self.__normaliser_semaine()

    def __remplir_jours(self, jour_mois_start, jour_mois_fin, jour_semaine_start: JoursSemaine):
        jour_mois = jour_mois_start

        for jour_semaine in jour_semaine_start.fin_semaine():
            if jour_mois > jour_mois_fin:
                break

            self.jours.append(Jour(jour_semaine=jour_semaine, jour_mois=jour_mois))
            jour_mois = jour_mois + 1

    def __normaliser_semaine(self):
        if self.jours[0].jour_sem.value > JoursSemaine.LUNDI.value:
            self.jours = [None for _ in range(self.jours[0].jour_sem.value)] + self.jours
        elif self.jours[-1].jour_sem.value < 6:
            self.jours = self.jours + [None for _ in range(self.jours[-1].jour_sem.value, 6)]

    def last_day(self):
        return [j for j in self.jours if j][-1]


class Mois:
    def __init__(self, no_mois: int, nombre_de_jours: int, jour_start_semaine=JoursSemaine.LUNDI, annee=None) -> None:
        self.annee: int = annee
        self.nombre_de_jours = nombre_de_jours
        self.no_mois = no_mois
        self.semaines: List[Semaine] = []
        self.generateur_semaines_du_mois(nombre_de_jours, jour_start_semaine)

    def generateur_semaines_du_mois(self, jour_mois_fin, jour_semaine_start=JoursSemaine.LUNDI):
        jour_mois = 1

        while jour_mois <= jour_mois_fin:
            s = Semaine(jour_semaine_start, jour_mois, jour_mois_fin)
            jour_mois = s.last_day().jour_mois + 1
            self.semaines.append(s)
            jour_semaine_start = JoursSemaine.LUNDI

    def dernier_jour_du_mois(self) -> Jour:
        return self.semaines[-1].last_day()

    def __str__(self) -> str:
        return ", ".join([f"{j} {self.no_mois}" for j in self.semaines])
