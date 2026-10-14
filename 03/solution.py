"""Advent of Code 2024, jour 3 : instructions dans un texte bruité.

Une seule expression régulière reconnaît les trois formes d'instructions
(mul(a,b), do(), don't()) ; finditer les parcourt dans l'ordre du texte.
Partie 2 : un drapeau, mis à jour par do() et don't(), indique si les
multiplications comptent.
"""
import re

INSTRUCTION = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return f.read()


def somme_produits(texte, avec_drapeau):
    total = 0
    actif = True
    for m in INSTRUCTION.finditer(texte):
        if m.group(0) == 'do()':
            actif = True
        elif m.group(0) == "don't()":
            actif = False
        elif actif or not avec_drapeau:
            total += int(m.group(1)) * int(m.group(2))
    return total


def partie1(texte):
    return somme_produits(texte, avec_drapeau=False)


def partie2(texte):
    return somme_produits(texte, avec_drapeau=True)


texte = lire_entree('input.txt')
print('Partie 1 :', partie1(texte))
print('Partie 2 :', partie2(texte))
