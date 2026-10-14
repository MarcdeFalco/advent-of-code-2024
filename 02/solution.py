"""Advent of Code 2024, jour 2 : suites presque monotones.

Une ligne est sûre si ses écarts successifs sont tous de même signe et de
valeur absolue entre 1 et 3.
Partie 2 : on essaie toutes les suppressions d'un élément (force brute, O(n^2)
par ligne, sans importance pour des lignes courtes).
"""


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return [list(map(int, ligne.split())) for ligne in f if ligne.strip()]


def est_sure(niveaux):
    ecarts = [niveaux[i] - niveaux[i + 1] for i in range(len(niveaux) - 1)]
    # On se ramène au cas décroissant (écarts positifs) en changeant le signe.
    if ecarts[0] < 0:
        ecarts = [-e for e in ecarts]
    return all(0 < e < 4 for e in ecarts)


def partie1(rapports):
    return sum(1 for niveaux in rapports if est_sure(niveaux))


def partie2(rapports):
    total = 0
    for niveaux in rapports:
        sure = est_sure(niveaux)
        for i in range(len(niveaux)):
            sans_i = [niveaux[j] for j in range(len(niveaux)) if j != i]
            sure = sure or est_sure(sans_i)
        if sure:
            total += 1
    return total


rapports = lire_entree('input.txt')
print('Partie 1 :', partie1(rapports))
print('Partie 2 :', partie2(rapports))
