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
    """
    auteur: Lucas
    regrouppe les propriétes d'un objet Jour du calendrier
    """
    def __init__(self, jour_mois, jour_semaine: JourSemaine, semaine: 'Semaine', mois: NomMois = None, annee: int = None):
        self.jour_mois = jour_mois
        self.jour_semaine = jour_semaine
        self._mois = mois if mois else semaine._mois.nom_mois
        self.__semaine = semaine
        self._annee = annee if annee else semaine._mois.annee

    def jour_d_un_autre_mois(self) -> bool:
        return self.__semaine._mois.nom_mois != self._mois


class Semaine:
    """
    auteur: Lucas
    regrouppe les propriétes d'un objet Jour du calendrier
    """
    def __init__(self, mois:'Mois'):
        self.jours: List[Jour] = []
        self._mois = mois


class Mois:
    """
    auteur: Nicolas
    regrouppe les propriétes d'un objet Jour du calendrier
    """
    def __init__(self, nom_mois: NomMois, annee: int = None):
        self.semaines: List[Semaine] = []
        self.nom_mois = nom_mois
        self.annee = annee
        self.dernier_jour_mois: JourSemaine = None


class Annee:
    """
    auteur: Lucas
    regrouppe les propriétes d'un objet Jour du calendrier
    """
    def __init__(self, annee, mois: List[Mois] = None):
        self.mois = mois if mois else []
        self.annee = annee


def _division_euclidiene(dividend: int, diviseur: int):
    """
    auteur: Nicolas
    calcule le reste et le résultat de la division entiere de deux nombres
    """
    if dividend < 0:
        return dividend % diviseur, -abs(dividend // diviseur)
    else:
        return dividend % diviseur, dividend // diviseur


def _mois_annee_plus_valeur(mois: NomMois, annee: int, delta_mois: int) -> Tuple[NomMois, int]:
    """
    auteur: Nicolas
    calcule le reste et le résultat de la division entiere de deux nombres
    """
    valeur = _division_euclidiene(mois.value + delta_mois, 12)
    return NomMois(valeur[0]), annee + valeur[1]


def jour_suivant(jour: JourSemaine):
    """
    auteur: Lucas
    calcule le reste et le résultat de la division entiere de deux nombres
    """
    if jour.value < JourSemaine.DIMANCHE.value:
        return JourSemaine(jour.value + 1)
    else:
        return JourSemaine.LUNDI


def __calcul_jours_mois(mois: NomMois, annee: int) -> int:
    """
    auteur: Lucas
    calcule le reste et le résultat de la division entiere de deux nombres
    """
    nummero_mois = mois.value + 1

    if nummero_mois in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif nummero_mois == 2:
        return 29 if annee % 4 == 0 else 28
    else:
        return 30


def _generateur_mois(nom_mois: NomMois, annee: int,
                     jour_sem_1er_du_mois: JourSemaine = JourSemaine.LUNDI) -> Mois:
    """
    auteur: Nicolas

    Le "coeur" de notre module de generation de dates.
     - permet de générer les semaines d'un mois/année donné à partir de son jour de debut et en
     s'aidant d'un générateur de jours/numeros de semaine (une fonction qui renvoie à l'infini
     une serie LMMJVSD assortie du numero de la semaine

    :param nom_mois: le n° de mois (pour simplifier l'agorithme les mois sont numerotées de 0 à 11)
    :param annee: l'année (permet de calculer le nombre des jour dans le mois surtout pour le mois de fevrier)
    :param jour_sem_1er_du_mois: jour de la semaine avec laquelle commence le mois (ex. un Mardi)
    :param generateur_jours_semaine: générateur de jours/numeros de semaine - permet d'utiliser un générateur unique pour l'anée afin de numeroter les semaines si besoin
    :return:
    """
    mois: Mois = Mois(nom_mois, annee)
    jour_semaine = JourSemaine.DIMANCHE
    semaine = Semaine(mois)
    # on demarre la semaine avec les jours de la semaine precedente si le mois ne commence pas un Lundi
    if jour_sem_1er_du_mois != JourSemaine.LUNDI:
        mois_precedent, annee_precedent = _mois_annee_plus_valeur(nom_mois, annee, -1)
        jours_mois_precedent = __calcul_jours_mois(mois_precedent, annee)
        for j in range(jours_mois_precedent - jour_sem_1er_du_mois.value + 1, jours_mois_precedent+1):
            jour_semaine = jour_suivant(jour_semaine)
            semaine.jours.append(Jour(j, jour_semaine, semaine, mois_precedent, annee_precedent))

    # on ajoute les jours du mois
    jours_mois = __calcul_jours_mois(nom_mois, annee)
    for jour_mois in range(jours_mois):
        jour_semaine = jour_suivant(jour_semaine)
        semaine.jours.append(Jour(jour_mois + 1, jour_semaine, semaine))
        if jour_semaine == JourSemaine.DIMANCHE:
            mois.semaines.append(semaine)
            semaine = Semaine(mois)

    mois.dernier_jour_mois = jour_semaine
    mois.semaines.append(semaine)
    # noinspection PyUnboundLocalVariable
    # completer la derniere semaine avec les jours du mois suivant si le mois ne se termine pas par un Dimanche
    if jour_semaine != JourSemaine.DIMANCHE:
        mois_suivant, annee_suivant = _mois_annee_plus_valeur(nom_mois, annee, 1)
        for j in range(6 - jour_semaine.value):
            jour_semaine = jour_suivant(jour_semaine)
            semaine.jours.append(Jour(j + 1, jour_semaine, semaine, mois_suivant, annee_suivant))

    return mois


def __calculer_jour_semaine_1er_janv(annee: int) -> JourSemaine:
    """
    auteur: Lucas
    calcule le reste et le résultat de la division entiere de deux nombres
    """
    d = date(annee, 1, 1)
    return JourSemaine(d.weekday())


def _generateur_annee(annee) -> List:
    """
    auteur: Lucas
    calcule le reste et le résultat de la division entiere de deux nombres
    """
    jour_sem_mois_start = __calculer_jour_semaine_1er_janv(annee)
    mois_annee = []
    for no_mois in NomMois:
        mois = _generateur_mois(no_mois, annee, jour_sem_mois_start)
        mois_annee.append(mois)

        jour_sem_mois_start = jour_suivant(mois.dernier_jour_mois)

    return mois_annee


def annee(annee: int) -> Annee:
    """
    auteur: Lucas
    calcule le reste et le résultat de la division entiere de deux nombres
    """
    mois_annee = _generateur_annee(annee)
    return Annee(annee, mois_annee)
