# PIL est la bibliothèque graphique recommendée par M.Camion.
# Image est l'objet qui correspond à une feuille vierge
# sur laquelle nous pouvons écrire et dessiner.
# ImageDraw est un outil pour dessiner, l'équivalent d'un stylo pour écrire du texte.
# ImageFont est la police à utiliser. M.Camion nous recommendé d'utiliser la police GFSDidotBold.
import os

from PIL import Image, ImageDraw, ImageFont

# generateur_dates est une mini-bibliothèque de fonctions et des objets
# pour la manipulation du calendrier adapté aux besoins du projet développés par nos soins.
from calendrier.generateur_dates import Mois, Annee, NOM_MOIS
# outils_dessins est une mini-bibliothèque qui contient des outils
# pour dessiner les mois développés par nos soins.
# les "/" sont pour couper les lignes de code qui sont trop longs
from calendrier.outils_dessin import \
    Couleur, Point, Dimensions, \
    TAILLE_SEMAINE, TAILLE_CASE_JOUR, \
    sauvegarde_image, POLICE_JOUR, POLICE_NOM_MOIS, TAILLE_ENTETE_MOIS, calculer_taille_texte, \
    POLICE_JOURS_SEMAINE, COULEUR_PAR_DEFAUT, calculer_taille_image_du_mois


def dessiner_jour(jour_str: str, p: Point, drawer: ImageDraw, police: ImageFont, couleur: Couleur = Couleur.NOIR):
    """
    fonction destinée à dessiner un jour dans un point (p) donné de l'image.
    en utilisant les paramètres j de type Jour, "p" de type Point, "canevas" de type Image
    ensuite: police, police de caractère pour écrire le chiffre correspondant au jour
    couleur, la couleur du texte (par défaut NOIR).
    """

    # On demande à PIL d'écrire le chiffre correspondant au jour du mois passé en paramètres sur l'image au point p.
    # Rmq: Nous transformons préalablement le point en Tuple car la librairie PIL ne comprends pas nos objets de type Point
    ptxt = (p.x + (TAILLE_CASE_JOUR.largeur - calculer_taille_texte(jour_str, police).largeur) // 2, p.y)
    drawer.text(ptxt, jour_str, fill=couleur.format_rgb(), font=police)


def dessiner_jour_entete(j: str, p: Point, canevas: Image, police: ImageFont, couleur: Couleur = Couleur.NOIR):
    """
    fonction destinée à dessiner un jour dans un point (p) donné de l'image.
    en utilisant les paramètres j de type Jour, "p" de type Point, "canevas" de type Image
    ensuite: police, police de caractère pour écrire le chiffre correspondant au jour
    couleur, la couleur du texte (par défaut NOIR).
    """

    # On demande à la librairie PIL de nous prêter un crayon pour dessiner et écrire aisément sur l'image.
    drawer = ImageDraw.Draw(canevas)

    # On demande à PIL d'écrire le chiffre correspondant au jour du mois passé en paramètres sur l'image au point p.
    # Rmq: Nous transformons préalablement le point en Tuple car la librairie PIL ne comprends pas nos objets de type Point
    ptxt = (p.x + (TAILLE_CASE_JOUR.largeur - calculer_taille_texte(j, police)) // 2, p.y)
    drawer.text(ptxt, j, fill=couleur.format_rgb(), font=police)


def dessiner_semaines(m: Mois, point_insertion: Point, drawer: ImageDraw, police: ImageFont):
    """
    Fonction destinée à dessiner le mois.
    on prend en paramètres: m, l'objet Mois à dessiner,
    :param m: le mois a aficher
    :param point_insertion: le point d'ou nous commençons a dessienr le mois
    :param canevas: l'image sur laquelle nous dessinons
    :param police: la police à utiliser
    :return:
    """
    p = point_insertion
    for semaine in m.semaines:
        for jour in semaine.jours:
            if jour:
                dessiner_jour(f"{jour.jour_mois:>2}", p, drawer, police,
                              couleur=Couleur.ROUGE if jour.est_dimanche() else COULEUR_PAR_DEFAUT)
            p = p.deplacer_x(TAILLE_CASE_JOUR)
        p = p.deplacer_y(TAILLE_CASE_JOUR)
        p.x = point_insertion.x


def dessiner_canevas(taille: Dimensions, CouleurFond: Couleur = Couleur.BLANC) -> Image: # Dimension s'écrit avec un seul s, pas 2!
    """
    Création de l’image au format 'rgb' avec la couleur de fond passé en parametre
    """
    im = Image.new('RGB', taille.to_tuple(), CouleurFond.format_rgb())
    return im
# RGB pour dire à PIL qu'on veut une image en couleurs.


def dessiner_entete_nom_mois(mois: str, point_insertion: Point, drawer: ImageDraw, couleur_titre: Couleur = Couleur.NOIR):
    """
    Dessine l'en-tête du mois
    :param annee:
    :param point_insertion: le point d'insértion de l'en-tête
    :param canevas: l'image (canevas) sur laquelle on "dessine"
    :param couleur_titre: la couleur du texte
    """
    # création d’un objet 'dessin' qui permet de dessiner sur l’image
    taile_texte = calculer_taille_texte(mois, POLICE_NOM_MOIS)
    p = (point_insertion.x + (TAILLE_SEMAINE.largeur - taile_texte.largeur) // 2, point_insertion.y)
    drawer.text(p, mois, fill=couleur_titre.value, font=POLICE_NOM_MOIS)  # L'année est en entier que l'on passe en paramètres.


def dessiner_ligne_lmmjvsd(p, drawer: ImageDraw):
    for j in ('L', 'M', 'M', 'J', 'V', 'S'):
        dessiner_jour(j, p, drawer, police=POLICE_JOURS_SEMAINE)
        p = p.deplacer_x(TAILLE_CASE_JOUR)
    dessiner_jour('D', p, drawer, police=POLICE_JOURS_SEMAINE, couleur=Couleur.ROUGE)


def dessiner_separateur(point_insertion: Point, longueur_separateur: int, drawer: ImageDraw):
    drawer.line([point_insertion.to_tuple(), point_insertion.deplacer_x(longueur_separateur).to_tuple()], fill=Couleur.BLEU.format_rgb(), width=2)


def generer_image_mois_pour_annee(annee: Annee):
def generer_images_mois_pour_annee(annee: Annee):
    for mois in annee.liste_mois:
        canevas = dessiner_canevas(calculer_taille_image_du_mois(mois))
        taille_canevas = calculer_taille_image_du_mois(mois)
        canevas = dessiner_canevas(taille_canevas)

        back_im = Image.open(os.path.join('image_fond', TABLEAU_CORRESPONDENCE_MOIS_FOND[mois.no_mois]))
        resize = back_im.resize(taille_semaines(mois).empiler(TAILLE_ENTETE_JOURS_SEMAINE).to_tuple())
        canevas.paste(resize, (0, TAILLE_ENTETE_MOIS.hauteur))

        origine = Point(x=0, y=0)
        name = dessiner_mois(canevas, mois, origine)

        sauvegarde_image(canevas, fichier=os.path.join("mois_calendrier", f"{name}.jpeg"))


def dessiner_mois(canevas, mois, origine):
    name = NOM_MOIS[mois.no_mois]
    drawer = ImageDraw.Draw(canevas)
    dessiner_entete_nom_mois(name, origine, drawer)
    y = origine.deplacer_y(TAILLE_ENTETE_MOIS)
    dessiner_ligne_lmmjvsd(y, drawer)
    dessiner_separateur(y, TAILLE_ENTETE_MOIS.largeur, drawer)
    point_insertion_semaines = origine.deplacer_y(TAILLE_CASE_JOUR).deplacer_y(TAILLE_ENTETE_MOIS)
    dessiner_semaines(mois, point_insertion_semaines, drawer, POLICE_JOUR)
    return name
