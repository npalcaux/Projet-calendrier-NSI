from calendrier.dessin_calendrier import dessiner_calendrier
from calendrier.generateur_dates import Annee

if __name__ == '__main__':
    a = Annee(2011)
    dessiner_calendrier(a)