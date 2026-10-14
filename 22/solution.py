"""Advent of Code 2024, jour 22 : générateur pseudo-aléatoire.

suivant enchaîne trois mélanges (multiplication ou division par une puissance
de 2, ou exclusif, modulo 2^24).
Partie 1 : somme des 2000es nombres secrets des acheteurs.
Partie 2 : une fenêtre glissante de cinq valeurs donne les quatre dernières
variations du chiffre des unités ; on ajoute le prix à ce quadruplet dans un
dictionnaire, seulement à sa première apparition pour chaque acheteur. La
réponse est le meilleur total.
"""
from collections import defaultdict

MODULE = 16777216  # 2^24


def suivant(s):
    s = ((s * 64) ^ s) % MODULE
    s = ((s // 32) ^ s) % MODULE
    s = ((s * 2048) ^ s) % MODULE
    return s


def partie1(graines):
    total = 0
    for s in graines:
        for _ in range(2000):
            s = suivant(s)
        total += s
    return total


def partie2(graines):
    scores = defaultdict(int)
    for s in graines:
        fenetre = [s]
        for _ in range(4):
            fenetre.append(suivant(fenetre[-1]))
        fenetre = tuple(fenetre)
        rang = 4  # indice du dernier nombre de la fenêtre
        vus = set()
        while rang <= 2000:
            prix = tuple(c % 10 for c in fenetre)
            variations = tuple(prix[i + 1] - prix[i] for i in range(4))
            if variations not in vus:
                scores[variations] += prix[-1]
            vus.add(variations)
            fenetre = fenetre[1:] + (suivant(fenetre[-1]),)
            rang += 1
    return max(scores.values())


if __name__ == '__main__':
    graines = list(map(int, open('input.txt').read().split()))
    print(partie1(graines))
    print(partie2(graines))
