import unittest

from calendrier.generateur_dates import _generateur_mois, _modulo_plus_valeur, \
    _mois_annee_plus_valeur, NomMois, JourSemaine


class TestCalendrierMethods(unittest.TestCase):
    def test_semaine_entiere(self):
        pass

    def test_semaine_part(self):
        pass

    def test_arithmetique_mois(self):
        valeur = _modulo_plus_valeur(0, -25, 12)
        self.assertEqual((11, -3), valeur)

        valeur = _modulo_plus_valeur(0, 1, 12)
        self.assertEqual((1, 0), valeur)

        valeur = _modulo_plus_valeur(0, -15, 12)
        self.assertEqual((9, -2), valeur)

        valeur = _modulo_plus_valeur(1, 14, 12)
        self.assertEqual((3, 1), valeur)

        valeur = _modulo_plus_valeur(5, 11, 7)
        self.assertEqual((2, 2), valeur)

        valeur = _modulo_plus_valeur(5, 14, 7)
        self.assertEqual((5, 2), valeur)

        valeur = _modulo_plus_valeur(5, -12, 7)
        self.assertEqual((0, -1), valeur)


    def test_arithmetique_mois_annee(self):
        valeur = _mois_annee_plus_valeur(NomMois.JANVIER, 2020, -1)
        self.assertEqual((NomMois.DECEMBRE, 2019), valeur)

        valeur = _mois_annee_plus_valeur(NomMois.JANVIER, 2020, 1)
        self.assertEqual((NomMois.FEVRIER, 2020), valeur)

        valeur = _mois_annee_plus_valeur(NomMois.JANVIER, 2020, -15)
        self.assertEqual((NomMois.OCTOBRE, 2018), valeur)

        valeur = _mois_annee_plus_valeur(NomMois.FEVRIER, 2020, 14)
        self.assertEqual((NomMois.AVRIL, 2021), valeur)


    def test_mois(self):
        mois = _generateur_mois(NomMois.MARS, 2020, JourSemaine.DIMANCHE)
        jour = mois.semaines[0].jours[6]
        self.assertEqual((1, JourSemaine.DIMANCHE, NomMois.MARS, 2020), (jour.jour_mois, jour.jour_semaine, jour._mois, jour._annee))
        jour = mois.semaines[5].jours[1]
        self.assertEqual((31, JourSemaine.MARDI, NomMois.MARS, 2020), (jour.jour_mois, jour.jour_semaine, jour._mois, jour._annee))
