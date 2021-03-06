from enum import Enum
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

from calendrier.constantes import COULEUR_PAR_DEFAUT_TEXTE, Couleur


def sauvegarde_image(image: Image, fichier='calendrier.png'):
    """
    autheur: Lucas

    fonction déstinée à sauvegarder une image dans le fichier.
    :param image: image a sauvegarder
    :param fichier: nom du fichier (par défaut est "calendrier.png")
    :return:
    """
    # enregistrement de l’image finale dans un fichier
    image.save(fichier)


class Point:
    """
    autheur: Nicolas
    """
    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, other: 'Dimensions'):
        return Point(self.x + other.longueur, self.y + other.largeur)

    def deplacer_x(self, other):
        if isinstance(other, Dimensions):
            valeur = other.longueur
        elif isinstance(other, (int, float)):
            valeur = other
        else:
            raise BaseException(f'parametre incorect {other}')

        return Point(self.x + valeur, self.y)

    def deplacer_y(self, other):
        if isinstance(other, Dimensions):
            valeur = other.largeur
        elif isinstance(other, (int, float)):
            valeur = other
        else:
            raise BaseException(f'parametre incorect {other}')

        return Point(self.x, self.y + valeur)

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y

    def deplacer(self, d: 'Dimensions'):
        return Point(self.x + d.longueur, self.y + d.largeur)


class Dimensions:
    """
    autheur: Lucas

    Dimensions est un objet qui définie la taille/dimension d'un objet graophique de forme rectangulaire.
    """
    @classmethod
    def from_tuple(cls, size: Tuple[int, int]) -> 'Dimensions':
        return Dimensions(size[0], size[1])

    def __init__(self, largeur: int, hauteur: int) -> None:
        self.longueur: int = largeur
        self.largeur: int = hauteur

    def __mul__(self, other: 'Dimensions'):
        return Dimensions(self.longueur * other.longueur, self.largeur * other.largeur)

    def __add__(self, other: 'Dimensions'):
        return Dimensions(self.longueur + other.longueur, self.largeur + other.largeur)

    def __sub__(self, other: 'Dimensions'):
        return Dimensions(self.longueur - other.longueur, self.largeur - other.largeur)

    def __getitem__(self, item):
        return self.longueur if item == 0 else self.largeur

    def to_tuple(self):
        return self.longueur, self.largeur

    def __gt__(self, other):
        return self.longueur >= other.longueur and self.largeur >= other.largeur

    def __eq__(self, other):
        return self.longueur == other.longueur and self.largeur == other.largeur

    @staticmethod
    def __empiler(un: 'Dimensions', autre: 'Dimensions') -> 'Dimensions':
        return Dimensions(
                max(un.longueur, autre.longueur),
                un.largeur + autre.largeur
            )

    def empiler(self, *autres: 'Dimensions') -> 'Dimensions':
        multi = self.empiler_multi([autre for autre in autres])
        return Dimensions.__empiler(self, multi)

    @staticmethod
    def empiler_multi(autres: List['Dimensions']) -> 'Dimensions':
        dimenssion_courante = Dimensions(0, 0)
        for autre in autres:
            dimenssion_courante = Dimensions.__empiler(dimenssion_courante, autre)

        return dimenssion_courante

    def elargir(self, *autres) -> 'Dimensions':
        varargs = [autre for autre in autres]
        varargs.append(self)
        return self.elargir_multi(varargs)

    @staticmethod
    def elargir_multi(autres:List) -> 'Dimensions':
        dimenssion_courante = Dimensions(0, 0)
        for autre in autres:
            if isinstance(autre, Dimensions):
                dimenssion_courante = Dimensions(dimenssion_courante.longueur + autre.longueur, max(dimenssion_courante.largeur, autre.largeur))
            else:
                dimenssion_courante = Dimensions(dimenssion_courante.longueur + autre, dimenssion_courante.largeur)
        return dimenssion_courante


class AlignementHorizontal(Enum):
    GAUCHE = -1
    CENTRE = 0
    DROITE = 1


class AlignementVertical(Enum):
    BAS = -1
    CENTRE = 0
    HAUT = 1


def dessiner_texte(crayon: ImageDraw, texte: str, police: ImageFont, taille_fenetre: Dimensions,
                   origine: Point = Point(0, 0), couleur_texte=COULEUR_PAR_DEFAUT_TEXTE,
                   alignement_horizontal=AlignementHorizontal.GAUCHE, alignement_vertical=AlignementVertical.CENTRE):
    """
    autheur: Nicolas

    Création de l’image au format 'rgb' avec la couleur de fond passé en parametre
    """
    taille_texte = calculer_taille_texte(texte, police)

    if alignement_horizontal == AlignementHorizontal.DROITE:
        x = origine.x + taille_fenetre.longueur - taille_texte.longueur
    elif alignement_horizontal == AlignementHorizontal.CENTRE:
        x = origine.x + (taille_fenetre.longueur - taille_texte.longueur) // 2
    else:
        x = origine.x

    if alignement_vertical == AlignementVertical.BAS:
        y = origine.y + taille_fenetre.longueur - taille_texte.longueur
    elif alignement_vertical == AlignementVertical.CENTRE:
        y = origine.y + (taille_fenetre.largeur - taille_texte.largeur) // 2
    else:
        y = origine.y

    p = (x, y)
    crayon.text(p, texte, fill=couleur_texte.format_rgb(), font=police)


def calculer_taille_texte(texte: str, police: ImageFont) -> Dimensions:
    """
    autheur: Nicolas

    Calcule la taille de texte pour une police donnée
    :param texte: le texte dont on veux calculer la taille
    :param police: la police pour laquelle on souhaite calculer la taille du texte
    :return: la dimension du texte donné en police donnée
    """
    return Dimensions.from_tuple(police.getsize(texte)) \
        + Dimensions.from_tuple(police.getoffset(texte))


def dessiner_canevas(taille: Dimensions, CouleurFond: Couleur = Couleur.BLANC) -> Image:
    """
    autheur: Lucas

    Création de l’image au format 'rgb' avec la couleur de fond passé en parametre
    """
    im = Image.new('RGB', taille.to_tuple(), CouleurFond.value)
    return im