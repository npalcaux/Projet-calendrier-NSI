import unittest

from calendrier.generateur_dates import _generateur_mois, _modulo_plus_valeur, \
    _mois_annee_plus_valeur


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
        valeur = _mois_annee_plus_valeur(0, 2020, -1)
        self.assertEqual((11, 2019), valeur)

        valeur = _mois_annee_plus_valeur(0, 2020, 1)
        self.assertEqual((1, 2020), valeur)

        valeur = _mois_annee_plus_valeur(0, 2020, -15)
        self.assertEqual((9, 2018), valeur)

        valeur = _mois_annee_plus_valeur(1, 2020, 14)
        self.assertEqual((3, 2021), valeur)


    def test_mois(self):
        mois = [j for j in _generateur_mois(2, 2020, 6)]
        self.assertEqual((1, 6, 2, 2020), mois[0][6])
        self.assertEqual((31, 1, 2, 2020), mois[5][1])
