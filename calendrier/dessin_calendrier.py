# PIL est la bibliothèque graphique recommendée par M.Camion.
# Image est l'objet qui correspond à une feuille vierge
# sur laquelle nous pouvons écrire et dessiner.
# ImageDraw est un outil pour dessiner, l'équivalent d'un stylo pour écrire du texte.
# ImageFont est la police à utiliser. M.Camion nous recommendé d'utiliser la police GFSDidotBold.
from PIL import Image, ImageDraw, ImageFont, ImageColor

# generateur_dates est une mini-bibliothèque de fonctions et des objets
# pour la manipulation du calendrier adapté aux besoins du projet développés par nos soins.
from calendrier.generateur_dates import Mois, Annee, Jour, NOM_MOIS

# outils_dessins est une mini-bibliothèque qui contient des outils
# pour dessiner les mois développés par nos soins.
# les "/" sont pour couper les lignes de code qui sont trop longs
from calendrier.outils_dessin import \
    Couleur, Point, Dimensions, \
    calculer_taille_canevas, TAILLE_MOIS, TAILLE_JOUR, \
    sauvegarde_image, POLICE_JOUR, POLICE_NOM_MOIS, TAILLE_ENTETE_MOIS, TAILLE_IMAGE_MOIS, calculer_taille_texte, \
    POLICE_JOURS_SEMAINE


def dessiner_jour(j: Jour, p: Point, canevas: Image, police: ImageFont, couleur: Couleur = Couleur.NOIR):
    """
    fonction destinée à dessiner un jour dans un point (p) donné de l'image.
    en utilisant les paramètres j de type Jour, "p" de type Point, "canevas" de type Image
    ensuite: police, police de caractère pour écrire le chiffre correspondant au jour
    couleur, la couleur du texte (par défaut NOIR).
    """

    # On demande à la librairie PIL de nous prêter un crayon pour dessiner et écrire aisément sur l'image.
    drawer = ImageDraw.Draw(canevas)
    # Pour gérér les jours de la semaine vide en début/fin de mois.
    s = str(j.jour_mois) if j else ""
    # On demande à PIL d'écrire le chiffre correspondant au jour du mois passé en paramètres sur l'image au point p.
    # Rmq: Nous transformons préalablement le point en Tuple car la librairie PIL ne comprends pas nos objets de type Point
    drawer.text(p.to_tuple(), s, fill=couleur.value[0], font=police)

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
    drawer.text(p.to_tuple(), j, fill=couleur.value[0], font=police)

# TODO - a revoir
# fonction destinée à dessiner le mois.
# on prend en paramètres: m, l'objet Mois à dessiner,
def dessiner_semaines(m: Mois, p0: Point, canevas: Image, police: ImageFont):
    p = p0 # Pourquoi ?
    for semaine in m.semaines: # Pourquoi "in m.semaine" ?
        for i in range(6):
            dessiner_jour(semaine.jours[i], p, canevas, police)
            p = p.deplacer_x(TAILLE_JOUR)
        dessiner_jour(semaine.jours[6], p, canevas, police, couleur=Couleur.ROUGE)
        p = p.deplacer_y(TAILLE_JOUR)
        p.x = p0.x # x c'est l'abscisse ? C'est quoi le . de p.x ?

# TODO - a voir si on la garde étant donné que M.Gagelin veut les mois dans des fichiers à part.
def dessiner_annee(a: Annee, p: Point, canevas: Image, police: ImageFont):
    for i in range(3):
        for j in range(4):
            dessiner_semaines(a.liste_mois[i + j], p, canevas, police) # C'est quoi le . de a.x ? C'est quoi [i+j] ? Je ne comprends pas cette ligne.
            p = p.deplacer_x(TAILLE_MOIS)
        p = p.deplacer_y(TAILLE_MOIS)
        p.x = 0

def dessiner_canevas(taille: Dimensions, CouleurFond: Couleur = Couleur.BLANC) -> Image: # Dimension s'écrit avec un seul s, pas 2!
    """
    Création de l’image au format 'rgb' avec la couleur de fond
    """
    im = Image.new('RGB', taille.to_tuple(), CouleurFond.value[0])
    return im
# RGB pour dire à PIL qu'on veut une image en couleurs.


def dessiner_en_tete(mois: str, point_insertion: Point, canevas: Image, couleur_titre: Couleur = Couleur.NOIR):
    """
    Dessine l'en-tête du mois
    :param annee:
    :param point_insertion: le point d'insértion de l'en-tête
    :param canevas: l'image (canevas) sur laquelle on "dessine"
    :param couleur_titre: la couleur du texte
    """
    # création d’un objet 'dessin' qui permet de dessiner sur l’image
    drawer = ImageDraw.Draw(canevas) # On prête un crayon à PIL pour écrire sur l'image.
    taile_texte = calculer_taille_texte(mois, POLICE_NOM_MOIS)
    p = (point_insertion.x + (TAILLE_MOIS.largeur - taile_texte.largeur) // 2, point_insertion.y)
    drawer.text(p, mois, fill=couleur_titre.value, font=POLICE_NOM_MOIS) # L'année est en entier que l'on passe en paramètres.


#TODO: voir s'il est nécessaire de garder cela, car M.Gagelin.....
def dessiner_ligne_initiales_jours_semaine(p, canevas):
    for j in ('L', 'M', 'M', 'J', 'V', 'S'):
        dessiner_jour_entete(j, p, canevas, POLICE_JOURS_SEMAINE)
        p = p.deplacer_x(TAILLE_JOUR)
    dessiner_jour_entete('D', p, canevas, POLICE_JOURS_SEMAINE, couleur=Couleur.ROUGE)


def dessiner_separateur(point_insertion: Point, largeur: int, canevas: Image):
    draw = ImageDraw.Draw(canevas)
    draw.line([point_insertion.to_tuple(), point_insertion.deplacer_x(largeur).to_tuple()], fill=Couleur.BLEU.value[0], width=2)


def dessiner_calendrier(annee: Annee):
    for mois in annee.liste_mois:
        canevas = dessiner_canevas(TAILLE_IMAGE_MOIS)

        origine = Point(x=0, y=0)
        name = dessiner_mois(canevas, mois, origine)

        sauvegarde_image(canevas, fichier=f"{name}.jpeg") # Je ne comprends pas.


def dessiner_mois(canevas, mois, origine):
    name = NOM_MOIS[mois.no_mois]
    dessiner_en_tete(name, origine, canevas)
    y = origine.deplacer_y(TAILLE_ENTETE_MOIS)
    dessiner_ligne_initiales_jours_semaine(y, canevas)  # Pourquoi 10 10 ?
    dessiner_separateur(y, TAILLE_ENTETE_MOIS.largeur, canevas)
    dessiner_semaines(mois, origine.deplacer_y(TAILLE_JOUR).deplacer_y(TAILLE_ENTETE_MOIS), canevas, POLICE_JOUR)
    return name


if __name__ == '__main__':
    a = Annee(2011)
    dessiner_calendrier(a)