import datetime
import sys

from calendrier.dessin_calendrier import generer_images_mois_pour_annee, generer_image_annee
from calendrier.generateur_dates import Annee

if __name__ == '__main__':
    arguments_ligne_commande = sys.argv

    if len(arguments_ligne_commande) < 2:
        print("Pas d'année précisée par l'utilisateur, génération du calendrier pour l'anneé en cours")
        date_du_jour = datetime.datetime.now()
        annee_calendrier = date_du_jour.year
    else:
        annee_utilisateur = arguments_ligne_commande[1]
        print(f"Année précisée par l'utilisateur: {annee_utilisateur}")
        annee_calendrier = int(annee_utilisateur)

    a = Annee(annee_calendrier)
    generer_images_mois_pour_annee(a)
    generer_image_annee(a)
