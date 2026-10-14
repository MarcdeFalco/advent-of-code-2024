"""Advent of Code 2024, jour 11 : nombres qui se dédoublent.

Partie 1 : on simule 25 étapes sur la liste explicite, dont la longueur croît
exponentiellement.
Partie 2 (75 étapes) : chaque nombre évolue indépendamment des autres. On
calcule nb_descendants(x, r), le nombre d'éléments issus de x après r étapes,
par une récurrence mémoïsée (functools.cache) : les valeurs rencontrées se
répètent beaucoup, donc le nombre d'appels distincts reste petit.
"""
from functools import cache


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return list(map(int, f.read().split()))


def cligne(pierres):
    resultat = []
    for x in pierres:
        if x == 0:
            resultat.append(1)
        elif len(str(x)) % 2 == 0:
            s = str(x)
            resultat.append(int(s[:len(s) // 2]))
            resultat.append(int(s[len(s) // 2:]))
        else:
            resultat.append(x * 2024)
    return resultat


@cache
def nb_descendants(x, r):
    if r == 0:
        return 1
    if x == 0:
        return nb_descendants(1, r - 1)
    s = str(x)
    if len(s) % 2 == 0:
        return (nb_descendants(int(s[len(s) // 2:]), r - 1)
                + nb_descendants(int(s[:len(s) // 2]), r - 1))
    return nb_descendants(x * 2024, r - 1)


def partie1(pierres):
    for _ in range(25):
        pierres = cligne(pierres)
    return len(pierres)


def partie2(pierres):
    return sum(nb_descendants(x, 75) for x in pierres)


pierres = lire_entree('input.txt')
print('Partie 1 :', partie1(pierres))
print('Partie 2 :', partie2(pierres))
