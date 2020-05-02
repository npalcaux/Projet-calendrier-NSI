from enum import Enum

from PIL import ImageFont


def agrandissement_relatif(pourcentage: int, reference: int) -> int:
    return int(reference * (1 + pourcentage / 100))


def retrecissement_relatif(pourcentage: int, reference: int) -> int:
    return int(reference * (1 - pourcentage / 100))

TAILLE_POLICE_JOURS = 44

TAILLE_POLICE_JOURS_SEMAINE = agrandissement_relatif(pourcentage=10, reference=TAILLE_POLICE_JOURS)
TAILLE_POLICE_NOM_MOIS = agrandissement_relatif(pourcentage=30, reference=TAILLE_POLICE_JOURS)

TAILLE_POLICE_ANNEE_ENTETE_MOIS = retrecissement_relatif(pourcentage=55, reference=TAILLE_POLICE_JOURS)
TAILLE_POLICE_ANNEE = agrandissement_relatif(pourcentage=45, reference=TAILLE_POLICE_JOURS)

POLICE_JOUR = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS)
POLICE_JOURS_SEMAINE = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS_SEMAINE)
POLICE_NOM_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_NOM_MOIS)
POLICE_ANNEE_ENTETE_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_ANNEE_ENTETE_MOIS)
POLICE_ANNEE = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_ANNEE)
EPAISSEUR_SEPARATEUR_MOIS = 2

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


COULEUR_FOND = Couleur.BLANC
COULEUR_PAR_DEFAUT_TEXTE = Couleur.NOIR
COULEUR_PAR_DEFAUT_ENTETE=Couleur.VERT_CLAIR
COULEUR_SEPARATEUR_MOIS = Couleur.BLEU

TABLEAU_CORRESPONDENCE_MOIS_FOND = [
    "janvier.jpg", "fevrier.png", "mars.jpg", "janvier.jpg",
    "janvier.jpg", "janvier.jpg", "janvier.jpg", "janvier.jpg",
    "janvier.jpg", "janvier.jpg", "janvier.jpg", "decembre.jpg",
]
