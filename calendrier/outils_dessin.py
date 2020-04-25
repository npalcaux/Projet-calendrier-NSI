from enum import Enum
from typing import Tuple

from PIL import ImageFont, Image

def poucentage(ref: int, pourcentage: int) -> int:
    return int(ref * (1 + pourcentage/100))

TAILLE_POLICE_JOURS = 25
TAILLE_POLICE_JOURS_SEMAINE = poucentage(TAILLE_POLICE_JOURS, 15)
TAILLE_POLICE_NOM_MOIS = poucentage(TAILLE_POLICE_JOURS, 40)

POLICE_JOUR = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS)
POLICE_JOURS_SEMAINE = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS_SEMAINE)
POLICE_NOM_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_NOM_MOIS)


class Couleur(Enum):
    ROUGE = (255,0,0),
    VERT = (0,255,0),
    BLEU = (0,0,255),
    BLANC = (255,255,255),
    NOIR = (0,0,0)


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
    return calculer_taille_texte("00", POLICE_JOUR) + Dimensions(10, 10)


TAILLE_JOUR = calculer_taille_jour()


def calculer_taille_mois() -> Dimensions:
    return TAILLE_JOUR * Dimensions(7, 7)


TAILLE_MOIS = calculer_taille_mois()


def calculer_taille_entete_mois() -> Dimensions:
    nom_mois = calculer_taille_texte("9999", POLICE_NOM_MOIS)
    return Dimensions(largeur=TAILLE_MOIS.largeur, hauteur=nom_mois.hauteur)

TAILLE_ENTETE_MOIS = calculer_taille_entete_mois()


def calculer_taille_canevas():
    return Dimensions(
        largeur=TAILLE_MOIS.largeur,
        hauteur=TAILLE_MOIS.hauteur + TAILLE_ENTETE_MOIS.hauteur)

TAILLE_IMAGE_MOIS = calculer_taille_canevas()


def sauvegarde_image(image: Image, fichier='calendrier.png'):
    """
    fonction déstinée à sauvegarder une image dans le fichier.
    :param image: image a sauvegarder
    :param fichier: nom du fichier (par défaut est "calendrier.png")
    :return:
    """
    # enregistrement de l’image finale dans un fichier
    image.save(fichier)
