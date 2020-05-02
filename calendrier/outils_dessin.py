from enum import Enum
from typing import Tuple

from PIL import ImageFont, Image, ImageColor

from calendrier.generateur_dates import Mois, Annee


def agrandissement_relatif(pourcentage: int, reference: int) -> int:
    return int(reference * (1 + pourcentage / 100))


def retrecissement_relatif(pourcentage: int, reference: int) -> int:
    return int(reference * (1 - pourcentage / 100))


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

    def deplacer(self, d: 'Dimensions'):
        return Point(self.x + d.largeur, self.y + d.hauteur)


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

    def empiler(self, autre: 'Dimensions') -> 'Dimensions':
        return Dimensions(max(self.largeur, autre.largeur), self.hauteur + autre.hauteur)

    def elargir(self, autre: 'Dimensions') -> 'Dimensions':
        return Dimensions(self.largeur + autre.largeur, max(self.hauteur, autre.hauteur))


def calculer_taille_texte(texte: str, police: ImageFont) -> Dimensions:
    """
    Calcule la taille de texte pour une police donnée
    :param texte: le texte dont on veux calculer la taille
    :param police: la police pour laquelle on souhaite calculer la taille du texte
    :return: la dimension du texte donné en police donnée
    """
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


def calculer_taille_image_du_mois(mois: Mois) -> Dimensions:
    taille_semaine = calculer_taille_semaine()
    hauteur_mois = calculer_taille_entete_mois().hauteur \
                   + calculer_taille_entete_lmmjvsd().hauteur \
                   + taille_semaine.hauteur * len(mois.semaines)

    return Dimensions(taille_semaine.largeur, hauteur_mois)


def calculer_taille_image_annee(annee: Annee, lignes=3, colonnes=4) -> Dimensions:
    taille_image_annee = Dimensions(0, 0) + calculer_taille_texte(str(annee.annee), POLICE_NOM_MOIS)
    for l in range(lignes):
        taille_rangee_mois = Dimensions(0, 0)
        for c in range(colonnes):
            taille_mois = calculer_taille_image_du_mois(annee.liste_mois[l + c])
            taille_rangee_mois = taille_rangee_mois.elargir(taille_mois)
        taille_image_annee = taille_image_annee.empiler(taille_rangee_mois)
    return taille_image_annee


def sauvegarde_image(image: Image, fichier='calendrier.png'):
    """
    fonction déstinée à sauvegarder une image dans le fichier.
    :param image: image a sauvegarder
    :param fichier: nom du fichier (par défaut est "calendrier.png")
    :return:
    """
    # enregistrement de l’image finale dans un fichier
    image.save(fichier)


def taille_semaines(mois: Mois) -> Dimensions:
    return Dimensions(TAILLE_SEMAINE.largeur, TAILLE_SEMAINE.hauteur * len(mois.semaines))


##########################################
#               CONSTANTES               #
##########################################
TAILLE_POLICE_JOURS = 44
TAILLE_POLICE_JOURS_SEMAINE = agrandissement_relatif(pourcentage=15, reference=TAILLE_POLICE_JOURS)
TAILLE_POLICE_NOM_MOIS = agrandissement_relatif(pourcentage=40, reference=TAILLE_POLICE_JOURS)
TAILLE_POLICE_ANNEE_ENTETE_MOIS = retrecissement_relatif(pourcentage=45, reference=TAILLE_POLICE_JOURS)

POLICE_ANNEE_ENTETE_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_ANNEE_ENTETE_MOIS)
POLICE_JOUR = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS)
POLICE_JOURS_SEMAINE = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS_SEMAINE)
POLICE_NOM_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_NOM_MOIS)

TAILLE_CASE_JOUR = calculer_taille_jour()
TAILLE_SEMAINE = calculer_taille_semaine()
TAILLE_ENTETE_JOURS_SEMAINE = calculer_taille_entete_lmmjvsd()
TAILLE_ENTETE_MOIS = calculer_taille_entete_mois()


class Couleur(Enum):
    ROUGE = "#ff4040"
    VERT = "#3df23d"
    BLEU = "#3d3df2"
    JAUNE = "#f2f23d"
    CYAN = "#3df2f2"
    MAGENTA = "#f23df2"
    ORANGE = "#f2973d"
    TURQUOISE = "#3df297"
    VIOLET = "#973df2"
    VERT_CLAIR = "#97f23d"
    BLEU_CLAIR = "#3d97f2"
    ROSE = "#f23d97"
    NOIR = "#000000"
    BLANC = "#ffffff"

    def format_rgb(self):
        return self.value

COULEUR_PAR_DEFAUT_TEXTE = Couleur.NOIR
COULEUR_PAR_DEFAUT_ENTETE=Couleur.VERT_CLAIR

TABLEAU_CORRESPONDENCE_MOIS_FOND = [
    "janvier.jpg", "fevrier.png", "mars.jpg", "janvier.jpg",
    "janvier.jpg", "janvier.jpg", "janvier.jpg", "janvier.jpg",
    "janvier.jpg", "janvier.jpg", "janvier.jpg", "decembre.jpg",
]