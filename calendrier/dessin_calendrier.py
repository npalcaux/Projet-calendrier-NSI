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
    POLICE_JOURS_SEMAINE, COULEUR_PAR_DEFAUT_TEXTE, calculer_taille_image_du_mois, TABLEAU_CORRESPONDENCE_MOIS_FOND, \
    TAILLE_ENTETE_JOURS_SEMAINE, taille_semaines, POLICE_ANNEE_ENTETE_MOIS, COULEUR_PAR_DEFAUT_ENTETE, \
    calculer_taille_image_annee


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
                # ":>2" signifie à Python qu'il doit sessiner le chiffre sur 2 colonnes, et l'aligner à gauche
                # aunsi, par exemple, le chiffre 1 sera affiche en tant que " 1"
                dessiner_jour(f"{jour.jour_mois:>2}", p, drawer, police,
                              couleur=Couleur.ROUGE if jour.est_dimanche() else COULEUR_PAR_DEFAUT_TEXTE)
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

def dessiner_centre(craion: ImageDraw, texte: str, police: ImageFont, taille_fenetre: Dimensions, point_insertion: Point = Point(0, 0), couleur_texte = COULEUR_PAR_DEFAUT_TEXTE):
    taile_texte = calculer_taille_texte(texte, police)
    p = (point_insertion.x + (taille_fenetre.largeur - taile_texte.largeur) // 2, point_insertion.y)
    craion.text(p, texte, fill=couleur_texte.format_rgb(), font=police)

def dessiner_entete_nom_mois(mois: str, annee: str, point_insertion: Point, craion: ImageDraw, couleur_titre: Couleur = Couleur.NOIR, inclure_annee = False):
    """
    Dessine l'en-tête du mois

    :param annee:
    :param point_insertion: le point d'insértion de l'en-tête
    :param canevas: l'image (canevas) sur laquelle on "dessine"
    :param couleur_titre: la couleur du texte
    """
    craion.rectangle(
        (point_insertion.to_tuple(), point_insertion.deplacer(TAILLE_ENTETE_MOIS).to_tuple()),
        fill=COULEUR_PAR_DEFAUT_ENTETE.format_rgb()
    )
    # création d’un objet 'dessin' qui permet de dessiner sur l’image
    dessiner_centre(craion, mois, POLICE_NOM_MOIS, TAILLE_SEMAINE, point_insertion, couleur_titre)

    if inclure_annee:
        taille_annee_mois = calculer_taille_texte(annee, police=POLICE_ANNEE_ENTETE_MOIS)
        pt_ins_annee_mois = (point_insertion.x + TAILLE_ENTETE_MOIS.largeur - taille_annee_mois.largeur, point_insertion.y)
        craion.text(pt_ins_annee_mois, annee, fill=couleur_titre.format_rgb(), font=POLICE_ANNEE_ENTETE_MOIS)


def dessiner_ligne_lmmjvsd(p, drawer: ImageDraw):
    for j in ('L', 'M', 'M', 'J', 'V', 'S'):
        dessiner_jour(j, p, drawer, police=POLICE_JOURS_SEMAINE)
        p = p.deplacer_x(TAILLE_CASE_JOUR)
    dessiner_jour('D', p, drawer, police=POLICE_JOURS_SEMAINE, couleur=Couleur.ROUGE)


def dessiner_separateur(point_insertion: Point, longueur_separateur: int, drawer: ImageDraw):
    drawer.line([point_insertion.to_tuple(), point_insertion.deplacer_x(longueur_separateur).to_tuple()], fill=Couleur.BLEU.format_rgb(), width=2)


def generer_images_mois_pour_annee(annee: Annee):
    for mois in annee.liste_mois:
        taille_canevas = calculer_taille_image_du_mois(mois)
        canevas = dessiner_canevas(taille_canevas)

        back_im = Image.open(os.path.join('image_fond', TABLEAU_CORRESPONDENCE_MOIS_FOND[mois.no_mois]))
        resize = back_im.resize(taille_semaines(mois).empiler(TAILLE_ENTETE_JOURS_SEMAINE).to_tuple())
        canevas.paste(resize, (0, TAILLE_ENTETE_MOIS.hauteur))

        name = dessiner_mois(canevas, mois, Point(x=0, y=0), inclure_annee=True)

        sauvegarde_image(canevas, fichier=os.path.join("mois_calendrier", f"{name}.jpeg"))


def generer_image_annee(annee: Annee):
    taille_canevas = calculer_taille_image_annee(annee)
    canevas = dessiner_canevas(taille_canevas)

    p = Point(0, 0).deplacer_y(calculer_taille_texte(str(annee.annee), POLICE_NOM_MOIS))
    for i in range(3):
        taille_rangee = Dimensions(0, 0)
        for j in range(4):
            mois = annee.liste_mois[i + j]
            dessiner_mois(canevas=canevas, mois=mois, origine=p)
            taille_mois = calculer_taille_image_du_mois(mois)
            taille_rangee = taille_rangee.elargir(taille_mois)
            p.x = taille_rangee.largeur
        p = p.deplacer_y(taille_rangee.hauteur)
        p.x = 0

    sauvegarde_image(canevas, fichier=os.path.join("mois_calendrier", f"{annee.annee}.jpeg"))


def dessiner_mois(canevas: Image, mois: Mois, origine: Point, inclure_annee=False):
    nom_mois = NOM_MOIS[mois.no_mois]
    drawer = ImageDraw.Draw(canevas)
    dessiner_entete_nom_mois(mois=nom_mois, annee=str(mois.annee), point_insertion=origine, craion=drawer, inclure_annee=inclure_annee)
    y = origine.deplacer_y(TAILLE_ENTETE_MOIS)
    dessiner_ligne_lmmjvsd(y, drawer)
    dessiner_separateur(y, TAILLE_ENTETE_MOIS.largeur, drawer)
    point_insertion_semaines = origine.deplacer_y(TAILLE_CASE_JOUR).deplacer_y(TAILLE_ENTETE_MOIS)
    dessiner_semaines(mois, point_insertion_semaines, drawer, POLICE_JOUR)
    return nom_mois
