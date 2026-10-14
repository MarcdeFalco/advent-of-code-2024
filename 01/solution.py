"""Advent of Code 2024, jour 1 : deux listes à apparier.

Partie 1 : on trie les deux colonnes ; apparier le i-ème plus petit élément de
chaque liste donne la somme des écarts.
Partie 2 : pour chaque élément de la liste de gauche, on compte ses occurrences
dans la liste de droite (list.count, donc O(n^2)).
"""


def lire_entree(nom_fichier):
    gauche, droite = [], []
    with open(nom_fichier) as f:
        for ligne in f:
            if ligne.strip():
                a, b = map(int, ligne.split())
                gauche.append(a)
                droite.append(b)
    return gauche, droite


def partie1(donnees):
    gauche, droite = donnees
    return sum(abs(a - b) for a, b in zip(sorted(gauche), sorted(droite)))


def partie2(donnees):
    gauche, droite = donnees
    return sum(a * droite.count(a) for a in gauche)


donnees = lire_entree('input.txt')
print('Partie 1 :', partie1(donnees))
print('Partie 2 :', partie2(donnees))
