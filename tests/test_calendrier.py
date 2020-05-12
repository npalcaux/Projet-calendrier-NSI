import unittest

from calendrier.generateur_dates import JourSemaine, Semaine, Mois, Annee, generateur_mois, _mois_plus_valeur, \
    _mois_annee_plus_valeur


class TestCalendrierMethods(unittest.TestCase):
    def test_semaine_entiere(self):
        pass

    def test_semaine_part(self):
        pass

    def test_arithmetique_mois(self):
        valeur = _mois_plus_valeur(0, -1)
        self.assertEqual(11, valeur)

        valeur = _mois_plus_valeur(0, 1)
        self.assertEqual(1, valeur)

        valeur = _mois_plus_valeur(0, -15)
        self.assertEqual(9, valeur)

        valeur = _mois_plus_valeur(1, 14)
        self.assertEqual(3, valeur)


    def test_arithmetique_mois_annee(self):
        valeur = _mois_annee_plus_valeur(0, 2020, -1)
        self.assertEqual((11, 2019), valeur)

        valeur = _mois_annee_plus_valeur(0, 2020, 1)
        self.assertEqual((1, 2020), valeur)

        valeur = _mois_annee_plus_valeur(0, 2020, -15)
        self.assertEqual((9, 2018), valeur)

        valeur = _mois_annee_plus_valeur(1, 2020, 14)
        self.assertEqual((3, 2021), valeur)


    def test_mois(self):
        mois = [j for j in generateur_mois(2, 2020, 6)]
        self.assertEqual((1, 6, 0, 2, 2020), mois[6])
        self.assertEqual((31, 1, 5, 2, 2020), mois[36])
