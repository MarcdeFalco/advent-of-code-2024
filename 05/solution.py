"""Advent of Code 2024, jour 5 : listes soumises à des contraintes d'ordre.

Chaque règle « a avant b » est rangée dans predecesseurs[b]. Une liste est
correcte si aucun élément n'a de prédécesseur obligé placé après lui (test
sur toutes les paires).
Partie 2 : on remet les listes fausses dans l'ordre par un tri à bulles dont
la comparaison est donnée par les règles (cela suffit car les règles
définissent un ordre total sur les éléments d'une même liste).
"""
from collections import defaultdict


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        regles_texte, listes_texte = f.read().strip().split('\n\n')
    predecesseurs = defaultdict(list)
    for ligne in regles_texte.split('\n'):
        a, b = map(int, ligne.split('|'))
        predecesseurs[b].append(a)
    listes = [list(map(int, ligne.split(',')))
              for ligne in listes_texte.split('\n')]
    return predecesseurs, listes


def est_correcte(liste, predecesseurs):
    for i, b in enumerate(liste):
        for b2 in liste[i + 1:]:
            if b2 in predecesseurs[b]:
                return False
    return True


def partie1(donnees):
    predecesseurs, listes = donnees
    return sum(liste[len(liste) // 2] for liste in listes
               if est_correcte(liste, predecesseurs))


def partie2(donnees):
    predecesseurs, listes = donnees
    total = 0
    for liste in listes:
        if est_correcte(liste, predecesseurs):
            continue
        liste = liste[:]
        # Tri à bulles : on échange deux voisins si le second doit précéder
        # le premier.
        for i in range(len(liste)):
            for j in range(len(liste) - i - 1):
                if liste[j + 1] in predecesseurs[liste[j]]:
                    liste[j], liste[j + 1] = liste[j + 1], liste[j]
        total += liste[len(liste) // 2]
    return total


donnees = lire_entree('input.txt')
print('Partie 1 :', partie1(donnees))
print('Partie 2 :', partie2(donnees))
