from enum import Enum

from PIL import ImageFont

def agrandissement_relatif(pourcentage: int, reference: int) -> int:
    """
    autheur: Nicolas

    :param pourcentage:
    :param reference:
    :return:
    """
    return int(reference * (1 + pourcentage / 100))


def retrecissement_relatif(pourcentage: int, reference: int) -> int:
    """
    autheur: Lucas
    """
    return int(reference * (1 - pourcentage / 100))

# autheur: Nicolas
TAILLE_POLICE_JOURS = 44

TAILLE_POLICE_JOURS_SEMAINE = agrandissement_relatif(pourcentage=10, reference=TAILLE_POLICE_JOURS)
TAILLE_POLICE_NOM_MOIS = agrandissement_relatif(pourcentage=30, reference=TAILLE_POLICE_JOURS)

TAILLE_POLICE_ANNEE_ENTETE_MOIS = retrecissement_relatif(pourcentage=55, reference=TAILLE_POLICE_JOURS)
TAILLE_POLICE_ANNEE = agrandissement_relatif(pourcentage=45, reference=TAILLE_POLICE_JOURS)

# autheur: Lucas
POLICE_JOUR = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS)
POLICE_JOURS_SEMAINE = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_JOURS_SEMAINE)
POLICE_NOM_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_NOM_MOIS)
POLICE_ANNEE_ENTETE_MOIS = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_ANNEE_ENTETE_MOIS)
POLICE_ANNEE = ImageFont.truetype(font='polices/GFSDidotBold.otf', size=TAILLE_POLICE_ANNEE)
EPAISSEUR_SEPARATEUR_MOIS = 2

class Couleur(Enum):
    """
    autheur: Lucas
    """
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
    GRIS_CLAIR = "#A8B1B9"

    def format_rgb(self):
        return self.value

# autheur: Nicolas
COULEUR_FOND = Couleur.BLANC
COULEUR_PAR_DEFAUT_TEXTE = Couleur.NOIR
COULEUR_PAR_DEFAUT_ENTETE=Couleur.VERT_CLAIR
COULEUR_SEPARATEUR_MOIS = Couleur.BLEU

# autheur: Lucas
TABLEAU_CORRESPONDENCE_MOIS_FOND = [
    "janvier.png",   "fevrier.png", "mars.png",     "avril.png",
    "mai.png",       "juin.png",    "juillet.png",  "aout.png",
    "septembre.png", "octobre.png", "novembre.png", "decembre.png"
]
