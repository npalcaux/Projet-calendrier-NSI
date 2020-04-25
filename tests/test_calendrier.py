import unittest

from calendrier.generateur_dates import JoursSemaine, Semaine, Mois, Annee


class TestCalendrierMethods(unittest.TestCase):
    def test_semaine_entiere(self):
        s = Semaine()

        self.assertEqual(7, len(s.jours), 'Trop ou trop peu de jours')
        self.assertEqual(list(JoursSemaine), [j.jour_sem for j in s.jours])
        self.assertEqual([i+1 for i in range(7)], [j.jour_mois for j in s.jours])

    def test_semaine_part(self):
        s0 = Semaine(dernier_jour_du_mois=3)
        s = Semaine(jour_semaine_start=JoursSemaine.MERCREDI, jour_mois_start=10)

        self.assertEqual(7, len(s.jours), 'Trop ou trop peu de jours')
        self.assertEqual(JoursSemaine.MERCREDI.fin_semaine(semaine_complete=True), [j.jour_sem if j else None for j in s.jours])
        self.assertEqual([None, None, 10, 11, 12, 13, 14], [j.jour_mois if j else None for j in s.jours])

        self.assertEqual(
            [JoursSemaine.LUNDI, JoursSemaine.MARDI, JoursSemaine.MERCREDI, None, None, None, None],
            [j.jour_sem if j else None for j in s0.jours]
        )
        self.assertEqual(
            [1, 2, 3, None, None, None, None],
            [j.jour_mois if j else None for j in s0.jours]
        )

    def test_mois(self):
        m = Mois(3, nombre_de_jours=30, jour_start_semaine=JoursSemaine.MERCREDI)

        self.assertEqual(5, len(m.semaines), 'Trop ou trop peu de semaines')
        self.assertEqual(30, len([j for s in m.semaines for j in s.jours if j]), 'Trop ou trop peu de jours')
        self.assertEqual(30, m.semaines[-1].jours[-4].jour_mois, 'Mauvais jour fin de mois')
        self.assertEqual(JoursSemaine.JEUDI, m.semaines[-1].jours[-4].jour_sem, 'dernier jour du mois aurait du être un jeudi')

    def test_annee(self):
        a = Annee(2014)
        self.assertEqual(2014, a.annee)