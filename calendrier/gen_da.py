from typing import List, Generator, Tuple


def __est_anne_bisextile(annee: int):
    return annee % 4 == 0


def __calcul_jours_mois(numero_mois0: int, annee: int) -> int:
    nummero_mois = numero_mois0 + 1
    if nummero_mois in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif nummero_mois == 2:
        return 29 if __est_anne_bisextile(annee) else 28
    else:
        return 30


def generateur_jour_semaine(start: int) -> Generator[int, None, None]:
    no_semaine = 0
    if start > 0:
        for i in range(start, 7):
            yield i, no_semaine
        no_semaine = no_semaine + 1
    while True:
        for i in range(7):
            yield i, no_semaine
        no_semaine = no_semaine + 1


def generateur_calendrier(annee: int, jou_sem_start: int) -> Generator[Tuple, None, None]:
    semaine = generateur_jour_semaine(jou_sem_start)
    for mois_courrante in range(12):
        nombre_jours = __calcul_jours_mois(mois_courrante, annee)
        for jour in range(nombre_jours):
            jour_semaine, no_semaine = next(semaine)
            yield jour+1, jour_semaine, no_semaine, mois_courrante


if __name__ == '__main__':
    for mois in generateur_calendrier(2020, 2):
        print(mois)
