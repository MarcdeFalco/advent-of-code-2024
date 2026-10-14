"""Advent of Code 2024, jour 19 : décompositions en motifs.

nb_decompositions(mot) compte les façons d'écrire mot comme concaténation de
motifs : on essaie chaque motif qui en est un préfixe et on recommence sur le
suffixe restant. Le dictionnaire cache mémoïse le résultat par suffixe (il
est partagé entre les mots, ce qui est correct car le résultat ne dépend que
du suffixe).
Partie 1 : nombre de mots décomposables ; partie 2 : somme des nombres de
décompositions.
"""

cache = {}


def nb_decompositions(mot, motifs):
    if mot in cache:
        return cache[mot]
    if mot == '':
        return 1
    total = 0
    for motif in motifs:
        if mot.startswith(motif):
            total += nb_decompositions(mot[len(motif):], motifs)
    cache[mot] = total
    return total


def partie1(motifs, mots):
    return sum(1 for mot in mots if nb_decompositions(mot, motifs) > 0)


def partie2(motifs, mots):
    return sum(nb_decompositions(mot, motifs) for mot in mots)


if __name__ == '__main__':
    lignes = open('input.txt').read().strip().split('\n')
    motifs = lignes[0].split(', ')
    mots = lignes[2:]
    print(partie1(motifs, mots))
    print(partie2(motifs, mots))
