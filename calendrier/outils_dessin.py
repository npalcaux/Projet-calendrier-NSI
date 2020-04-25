from enum import Enum
from typing import Tuple

from PIL import ImageFont, Image

from calendrier.generateur_dates import Mois


def agrandissement_relatif(pourcentage: int, reference: int) -> int:
    return int(reference * (1 + pourcentage / 100))


class Point:
    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, other: 'Dimensions'):
        return Point(self.x + other.largeur, self.y + other.hauteur)

    def deplacer_x(self, other):
        if isinstance(other, Dimensions):
            valeur = other.largeur
        elif isinstance(other, (int, float)):
            valeur = other
        else:
            raise BaseException(f'parametre incorect {other}')

        return Point(self.x + valeur, self.y)

    def deplacer_y(self, other):
        if isinstance(other, Dimensions):
            valeur = other.hauteur
        elif isinstance(other, (int, float)):
            valeur = other
        else:
            raise BaseException(f'parametre incorect {other}')

        return Point(self.x, self.y + valeur)

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


class Dimensions:
    """
    Dimensions est un objet qui définie la taille/dimension d'un objet graophique de forme rectangulaire.
    """
    @classmethod
    def from_tuple(cls, size: Tuple[int, int]) -> 'Dimensions':
        return Dimensions(size[0], size[1])

    def __init__(self, largeur: int, hauteur: int) -> None:
        self.largeur: int = largeur
        self.hauteur: int = hauteur

    def __mul__(self, other: 'Dimensions'):
        return Dimensions(self.largeur * other.largeur, self.hauteur * other.hauteur)

    def __add__(self, other: 'Dimensions'):
        return Dimensions(self.largeur + other.largeur, self.hauteur + other.hauteur)

    def __getitem__(self, item):
        return self.largeur if item == 0 else self.hauteur

    def to_tuple(self):
        return self.largeur, self.hauteur


def calculer_taille_texte(texte: str, police: ImageFont) -> Dimensions:
    return Dimensions.from_tuple(police.getsize(texte)) \
           + Dimensions.from_tuple(police.getoffset(texte))


def calculer_taille_jour() -> Dimensions:
    """
    Calcule la taille de la case "jour" du calendrier
    On la dimenssione sur la base de la taille de la police
    utilisé pour l'affichege des jours de semaine (plus grande)
    :return: la taille d'in case jour
    """
    return calculer_taille_texte("00", POLICE_JOURS_SEMAINE) + Dimensions(10, 10)


def calculer_taille_semaine() -> Dimensions:
    return calculer_taille_jour() * Dimensions(7, 1)


def calculer_taille_entete_mois() -> Dimensions:
    nom_mois = calculer_taille_texte("JANVIER", POLICE_NOM_MOIS)
    return Dimensions(largeur=TAILLE_SEMAINE.largeur, hauteur=nom_mois.hauteur)


def calculer_taille_entete_lmmjvsd() -> Dimensions:
    entete_jours_semaine = calculer_taille_texte("L M M J V S D", POLICE_NOM_MOIS)
    return Dimensions(largeur=TAILLE_SEMAINE.largeur, hauteur=entete_jours_semaine.hauteur)

def calculer_taille_canevas(mois: Mois) -> Dimensions:
    taille_semaine = calculer_taille_semaine()
    hauteur_mois = calculer_taille_entete_mois().hauteur \
                   + calculer_taille_entete_lmmjvsd().hauteur \
                   + taille_semaine.hauteur * len(mois.semaines)

    return Dimensions(taille_semaine.largeur, hauteur_mois)


def sauvegarde_image(image: Image, fichier='calendrier.png'):
    """
    fonction déstinée à sauvegarder une image dans le fichier.
    :param image: image a sauvegarder
    :param fichier: nom du fichier (par défaut est "calendrier.png")
    :return:
    """
    # enregistrement de l’image finale dans un fichier
    image.save(fichier)

##########################################
#               CONSTANTES               #
##########################################
TAILLE_POLICE_JOURS = 25
TAILLE_POLICE_JOURS_SEMAINE = agrandissement_relatif(pourcentage=15, reference=TAILLE_POLICE_JOURS)
TAILLE_POLICE_NOM_MOIS = agrandissement_relatif(pourcentage=40, reference=TAILLE_POLICE_JOURS)

POLICE_JOUR = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS)
POLICE_JOURS_SEMAINE = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS_SEMAINE)
POLICE_NOM_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_NOM_MOIS)

TAILLE_CASE_JOUR = calculer_taille_jour()
TAILLE_SEMAINE = calculer_taille_semaine()
TAILLE_ENTETE_MOIS = calculer_taille_entete_mois()

class Couleur(Enum):
    ROUGE = (255,0,0),
    VERT = (0,255,0),
    BLEU = (0,0,255),
    BLANC = (255,255,255),
    NOIR = (0,0,0)

COULEUR_PAR_DEFAUT = Couleur.NOIR
