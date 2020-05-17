import os
from abc import ABC, abstractmethod

from PIL import ImageFont, ImageDraw, Image
import calendrier.constantes as CONST
from calendrier.constantes import Couleur

from calendrier.outils_dessin import dessiner_texte, Point, Dimensions, calculer_taille_texte, AlignementHorizontal, \
    AlignementVertical
from calendrier.generateur_dates import Jour, Mois, Semaine, JourSemaine


class ObjetGraphique(ABC):
    def __init__(self, data):
        self.donnees = data

    @abstractmethod
    def dessiner(self, drawer: ImageDraw, origine: Point, image: Image = None):
        pass


class ObjetGraphiqueTexte(ObjetGraphique):
    def __init__(self, texte: str,
                 taille: Dimensions,
                 police: ImageFont,
                 couleur_fond: Couleur = None,
                 couleur_cadre: Couleur = None,
                 couleur_texte: Couleur = CONST.COULEUR_PAR_DEFAUT_TEXTE,
                 alignement_horizontal=AlignementHorizontal.DROITE,
                 alignement_vertical=AlignementVertical.CENTRE,
                 epaisseur_cadre=1
                 ):
        super().__init__(texte)
        self.texte = self.donnees

        #   Calcule la taille de la case "jour" du calendrier
        #   On la dimenssione sur la base de la taille de la police
        #   utilisé pour l'affichege des jours de semaine (plus grande)
        self.taille = taille
        self.police = police
        self.couleur_fond = couleur_fond
        self.couleur_cadre = couleur_cadre
        self.couleur_texte = couleur_texte
        self.alignement_horizontal = alignement_horizontal
        self.alignement_vertical = alignement_vertical
        self.epaisseur_cadre = epaisseur_cadre

    def dessiner(self, drawer: ImageDraw, origine: Point, image: Image = None):
        """
        fonction destinée à dessiner un jour dans un point (p) donné de l'image.
        en utilisant les paramètres j de type Jour, "p" de type Point, "canevas" de type Image
        ensuite: police, police de caractère pour écrire le chiffre correspondant au jour
        couleur, la couleur du texte (par défaut NOIR).
        """

        # On demande à PIL d'écrire le chiffre correspondant au jour du mois passé en paramètres sur l'image au point p.
        # Rmq: Nous transformons préalablement le point en Tuple car la librairie PIL ne comprends pas nos objets de type Point
        if self.donnees:
            self.remplissage_et_cadre(drawer, origine)
            dessiner_texte(drawer, self.texte, self.police, self.taille, origine, self.couleur_texte, self.alignement_horizontal)

    def remplissage_et_cadre(self, drawer, origine_bloc: Point):
        marge_cadre = Dimensions(self.epaisseur_cadre, self.epaisseur_cadre)
        origine = origine_bloc.deplacer(marge_cadre)

        geometrie_rectangle = (origine.to_tuple(), origine.deplacer(self.taille - marge_cadre).to_tuple())
        if self.couleur_fond and self.couleur_cadre:
            drawer.rectangle(
                geometrie_rectangle,
                fill=self.couleur_fond.value,
                outline=self.couleur_cadre.value
            )
        elif self.couleur_cadre:
            drawer.rectangle(
                geometrie_rectangle,
                outline=self.couleur_cadre.value
            )
        elif self.couleur_fond:
            drawer.rectangle(
                geometrie_rectangle,
                fill=self.couleur_fond.value
            )


class ObjetGraphiqueJour(ObjetGraphiqueTexte):
    def __init__(self,
                 jour: Jour,
                 couleur_fond: Couleur = None,
                 couleur_cadre: Couleur = None):

        super().__init__(
            _jour_mois_to_string(jour.jour_mois),
            taille=TAILLE_OPTIMUM_CASE_JOUR,
            police=CONST.POLICE_JOUR,
            couleur_cadre=couleur_cadre,
            couleur_fond=couleur_fond,
            couleur_texte=Couleur.ROUGE if jour.jour_semaine == JourSemaine.DIMANCHE else CONST.COULEUR_PAR_DEFAUT_TEXTE,
            alignement_horizontal=AlignementHorizontal.CENTRE,
            alignement_vertical=AlignementVertical.CENTRE
        )
        self.jour = jour

    def dessiner(self, drawer: ImageDraw, origine: Point, image: Image = None):
        """
        fonction destinée à dessiner un jour dans un point (p) donné de l'image.
        en utilisant les paramètres j de type Jour, "p" de type Point, "canevas" de type Image
        ensuite: police, police de caractère pour écrire le chiffre correspondant au jour
        couleur, la couleur du texte (par défaut NOIR).
        """

        # On demande à PIL d'écrire le chiffre correspondant au jour du mois passé en paramètres sur l'image au point p.
        # Rmq: Nous transformons préalablement le point en Tuple car la librairie PIL ne comprends pas nos objets de type Point
        if self.jour.jour_d_un_autre_mois():
            self.couleur_texte = Couleur.GRIS_CLAIR
        super().dessiner(drawer, origine)


class ObjetGraphiqueSemaine(ObjetGraphique):
    def __init__(self, semaine: Semaine, couleur_cadre_jour:Couleur = None):
        super().__init__(semaine)

        self.jours = [
            ObjetGraphiqueJour(j, couleur_cadre=couleur_cadre_jour)
            for j in semaine.jours
        ]

        self.taille = Dimensions.elargir_multi([j.taille for j in self.jours])
        self.couleur_fond = None
        self.couleur_cadre = None

    def dessiner(self, drawer: ImageDraw, origine: Point, image: Image = None):
        p = origine
        for jour in self.jours:
            jour.dessiner(drawer, p)
            p = p.deplacer_x(jour.taille)


class ObjetGraphiqueMois(ObjetGraphique):
    def __init__(self,
                 mois: Mois,
                 inclure_annee: False,
                 couleur_fond=CONST.COULEUR_FOND,
                 couleur_cadre=CONST.COULEUR_SEPARATEUR_MOIS,
                 couleur_cadre_jour: Couleur = None,
                 utiliser_image_fond=False, taille_forcee: Dimensions=None):

        super().__init__(mois)

        self.epaisseur_cadre_mois = 3
        self.nom_mois = NOM_MOIS[mois.nom_mois.value]
        self.semaines = [ObjetGraphiqueSemaine(semaine, couleur_cadre_jour=couleur_cadre_jour) for semaine in mois.semaines]

        self.image_fond = None
        self.inclure_annee = inclure_annee
        self.epaisseur_separateur = 2
        self.utiliser_image_fond = utiliser_image_fond
        self.taille_forcee = taille_forcee

        # calcul dimenssions entete nom mois
        taille_texte_nom_mois = calculer_taille_texte(self.nom_mois, CONST.POLICE_NOM_MOIS)

        # calcul dimenssions entete nom jours semaine
        self.taille_entete_lmmjvsd = calculer_taille_texte("L M M J V S D", CONST.POLICE_JOURS_SEMAINE)

        largeur_semaine_max = max(
            max(semaine.taille.largeur for semaine in self.semaines),
            self.taille_entete_lmmjvsd.largeur
        )

        self.taille_entete_nom = Dimensions(largeur=largeur_semaine_max, hauteur=TAILLE_MAX_TEXTE_NOM_MOIS.hauteur)
        self.taille_zone_semaines = Dimensions.empiler_multi([s.taille for s in self.semaines])

        self.taille = self.taille_entete_nom.empiler(
            Dimensions(0, self.epaisseur_separateur),
            self.taille_entete_lmmjvsd,
            self.taille_zone_semaines,
        ) + Dimensions(2*self.epaisseur_cadre_mois, 2*self.epaisseur_cadre_mois)

        if self.taille_forcee and self.taille_forcee > self.taille:
            self.taille = self.taille_forcee

        self.couleur_fond = couleur_fond
        self.couleur_cadre = couleur_cadre
        self.couleur_titre = CONST.COULEUR_PAR_DEFAUT_TEXTE
        self.couleur_fond_entete = CONST.COULEUR_PAR_DEFAUT_ENTETE

    def dessiner(self, drawer: ImageDraw, origine0: Point, canevas: Image = None):
        self.__dessiner_cadre_mois(origine0, drawer)

        origine = origine0 + Dimensions(self.epaisseur_cadre_mois, self.epaisseur_cadre_mois)
        self.__dessiner_entete_nom_mois(origine, craion=drawer)

        origine_separateur = origine.deplacer_y(self.taille_entete_nom)
        self.__dessiner_separateur(origine_separateur, self.taille_entete_nom.largeur, drawer)

        origine_lmmjvsd = origine_separateur.deplacer_y(self.epaisseur_separateur)
        self.__dessiner_ligne_lmmjvsd(origine_lmmjvsd, drawer)

        origine_zone_semaines = origine_lmmjvsd.deplacer_y(self.taille_entete_lmmjvsd)
        if self.utiliser_image_fond:
            self.__dessiner_image_fond(origine_zone_semaines, canevas)

        self.__dessiner_semaines(origine_zone_semaines, drawer)

    def __dessiner_entete_nom_mois(self, origine: Point, craion: ImageDraw):
        """
        Dessine l'en-tête du mois

        :param origine: le point d'insértion de l'en-tête
        :param craion: l'outil de dessin
        :param couleur_titre: la couleur du texte du nom de mois
        """
        craion.rectangle(
            (origine.to_tuple(), origine.deplacer(self.taille_entete_nom).to_tuple()),
            fill=self.couleur_fond_entete.value
        )

        if self.inclure_annee:
            annee_str = str(self.donnees.annee)
            taille_annee_mois = calculer_taille_texte(annee_str, police=CONST.POLICE_ANNEE_ENTETE_MOIS)
            pt_ins_annee_mois = (
                origine.x + self.taille_entete_nom.largeur - taille_annee_mois.largeur, origine.y
            )
            craion.text(pt_ins_annee_mois, annee_str, fill=self.couleur_titre.value, font=CONST.POLICE_ANNEE_ENTETE_MOIS)

        # création d’un objet 'dessin' qui permet de dessiner sur l’image
        dessiner_texte(craion, self.nom_mois, CONST.POLICE_NOM_MOIS,
                       self.taille_entete_nom,
                       origine,
                       self.couleur_titre,
                       AlignementHorizontal.CENTRE)

    def __dessiner_ligne_lmmjvsd(self, origine, drawer):
        p = origine
        taille_case_jour = TAILLE_OPTIMUM_CASE_JOUR
        s_ = ('L', 'M', 'M', 'J', 'V', 'S')
        for j in range(6):
            dessiner_texte(drawer, s_[j], CONST.POLICE_JOURS_SEMAINE, taille_case_jour, p, alignement_horizontal=AlignementHorizontal.CENTRE)
            p = p.deplacer_x(taille_case_jour)
        dessiner_texte(drawer, "D", CONST.POLICE_JOURS_SEMAINE, taille_case_jour, p, Couleur.ROUGE, AlignementHorizontal.CENTRE)

    def __dessiner_separateur(self, origine, longueur_separateur, drawer):
        drawer.line((origine.to_tuple(), origine.deplacer_x(longueur_separateur).to_tuple()),
                    fill=self.couleur_cadre.value, width=self.epaisseur_separateur)

    def __dessiner_semaines(self, origine: Point, drawer: ImageDraw):
        p = origine
        for semaine in self.semaines:
            semaine.dessiner(drawer, p)
            p = p.deplacer_y(semaine.taille)

    def __dessiner_cadre_mois(self, origine: Point, drawer: ImageDraw):
        drawer.rectangle(
            (origine.to_tuple(), origine.deplacer(self.taille).to_tuple()),
            fill=self.couleur_fond.value,
            outline=self.couleur_cadre.value,
            width=self.epaisseur_cadre_mois
        )

    def __dessiner_image_fond(self, origine, canevas: Image):
        if not canevas:
            raise BaseException("Il faut fournir la reference de l'image canevas si on souhaite dessiner les images de fond de mois")

        # coller l'image du fond
        back_im = Image.open(os.path.join('image_fond', CONST.TABLEAU_CORRESPONDENCE_MOIS_FOND[self.donnees.nom_mois.value]))
        image_fond_semaines = back_im.resize(self.taille_zone_semaines.to_tuple())
        canevas.paste(image_fond_semaines, origine.to_tuple())


NOM_MOIS = (
    "JANVIER",
    "FEVRIER",
    "MARS",
    "AVRIL",
    "MAI",
    "JUIN",
    "JUILLET",
    "AOUT",
    "SEPTEMBRE",
    "OCTOBRE",
    "NOVEMBRE",
    "DECEMBRE"
)


def _jour_mois_to_string(valeur: int):
    return f"{valeur:>2}"


def __taille_max_case_jour() -> Dimensions:
    taille_jours = [calculer_taille_texte(_jour_mois_to_string(valeur), CONST.POLICE_JOUR) for valeur in range(10, 32)]
    return Dimensions(
        max(taille.largeur for taille in taille_jours),
        max(taille.hauteur for taille in taille_jours)
    )


def __taille_max_nom_mois():
    return max(calculer_taille_texte(nom, CONST.POLICE_NOM_MOIS) for nom in NOM_MOIS)


TAILLE_OPTIMUM_CASE_JOUR: Dimensions = __taille_max_case_jour() + Dimensions(10, 10)
TAILLE_MAX_TEXTE_NOM_MOIS = __taille_max_nom_mois() + Dimensions(10, 10)
