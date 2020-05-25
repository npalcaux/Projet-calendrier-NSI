# PIL est la bibliothèque graphique recommendée par M.Camion.
# Image est l'objet qui correspond à une feuille vierge
# sur laquelle nous pouvons écrire et dessiner.
# ImageDraw est un outil pour dessiner, l'équivalent d'un stylo pour écrire du texte.
# ImageFont est la police à utiliser. M.Camion nous recommendé d'utiliser la police GFSDidotBold.
import os

from PIL import ImageDraw

from calendrier.constantes import \
    POLICE_NOM_MOIS, Couleur
# generateur_dates est une mini-bibliothèque de fonctions et des objets
# pour la manipulation du calendrier adapté aux besoins du projet développés par nos soins.
from calendrier.generateur_dates import Annee, Mois
from calendrier.objets_graphiques import ObjetGraphiqueMois

# outils_dessins est une mini-bibliothèque qui contient des outils
# pour dessiner les mois développés par nos soins.
# les "/" sont pour couper les lignes de code qui sont trop longs
from calendrier.outils_dessin import \
    sauvegarde_image, Point, Dimensions, calculer_taille_texte, dessiner_canevas


# RGB pour dire à PIL qu'on veut une image en couleurs.


def generer_images_mois(mois: Mois):
    mois_geo = ObjetGraphiqueMois(
        mois, True, couleur_cadre_jour=Couleur.CYAN, utiliser_image_fond=True
    )

    canevas = dessiner_canevas(mois_geo.taille)
    mois_geo.dessiner(ImageDraw.Draw(canevas), Point(x=0, y=0), canevas=canevas)

    sauvegarde_image(canevas, fichier=os.path.join("mois_calendrier", f"{mois_geo.nom_mois}.jpeg"))


def generer_images_mois_pour_annee(annee: Annee):
    for mois in annee.mois:
        generer_images_mois(mois)


def generer_image_annee(annee: Annee):
    liste_obj_graphiques_mois = [
        ObjetGraphiqueMois(mois, False) for mois in annee.mois
    ]

    taille_max_mois = max(mois.taille for mois in liste_obj_graphiques_mois)

    liste_obj_graphiques_mois = [
        ObjetGraphiqueMois(mois, False, taille_forcee=taille_max_mois) for mois in annee.mois
    ]

    taille_texte = calculer_taille_texte(str(annee.annee), POLICE_NOM_MOIS)

    taille_canevas = taille_texte
    for i in range(3):
        taille_courante = Dimensions(0, 0)
        for j in range(4):
            taille_courante = taille_courante.elargir(liste_obj_graphiques_mois[i+j].taille)
        taille_canevas = taille_canevas.empiler(taille_courante)

    canevas = dessiner_canevas(taille_canevas)

    origine_zone_mois = Point(0, 0).deplacer_y(taille_texte)
    origine_mois = origine_zone_mois
    draw = ImageDraw.Draw(canevas)
    for i in range(3):
        taille_rangee = Dimensions(0, 0)
        for j in range(4):
            mois_geo = liste_obj_graphiques_mois[i*4 + j]
            mois_geo.dessiner(draw, origine_mois)

            taille_rangee = taille_rangee.elargir(mois_geo.taille)

            origine_mois.x = taille_rangee.longueur
        origine_mois = origine_mois.deplacer_y(taille_rangee.largeur)
        origine_mois.x = 0

    sauvegarde_image(canevas, fichier=os.path.join("mois_calendrier", f"{annee.annee}.jpeg"))
