from calendrier.dessin_calendrier import generer_images_mois_pour_annee
from calendrier.generateur_dates import Annee

if __name__ == '__main__':
    a = Annee(2011)
    generer_images_mois_pour_annee(a)