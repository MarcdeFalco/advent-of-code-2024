"""Advent of Code 2024, jour 13 : combinaisons de deux vecteurs.

On cherche des entiers u, v >= 0 avec u * A + v * B = P (A, B : boutons,
P : prix), en minimisant 3u + v.
Partie 1 : force brute sur u, v <= 100.
Partie 2 : la cible est décalée de 10^13 ; si le déterminant est non nul, le
système 2x2 a une unique solution (formules de Cramer), qu'on garde si elle
est entière et positive.
"""
import re

DECALAGE = 10000000000000


def lire_machines(texte):
    """Renvoie la liste des sextuplets (aX, aY, bX, bY, pX, pY)."""
    machines = []
    for bloc in texte.strip().split('\n\n'):
        machines.append(tuple(map(int, re.findall(r'\d+', bloc))))
    return machines


def cout_force_brute(aX, aY, bX, bY, pX, pY):
    """Plus petit coût avec au plus 100 appuis par bouton, 0 si impossible."""
    for kA in range(101):
        for kB in range(101):
            if aX * kA + bX * kB == pX and aY * kA + bY * kB == pY:
                # le premier couple trouvé suffit (en pratique il est unique)
                return 3 * kA + kB
    return 0


def cout_cramer(aX, aY, bX, bY, pX, pY):
    """Résout u aX + v bX = pX, u aY + v bY = pY ; 0 si pas de solution
    entière positive (le cas d'un déterminant nul est ignoré)."""
    delta = aX * bY - aY * bX
    if delta == 0:
        return 0
    numerateur_u = bY * pX - bX * pY
    numerateur_v = -aY * pX + aX * pY
    if numerateur_u % delta != 0 or numerateur_v % delta != 0:
        return 0  # pas de solution entière
    u = numerateur_u // delta
    v = numerateur_v // delta
    if u >= 0 and v >= 0:
        return 3 * u + v
    return 0


def partie1(machines):
    return sum(cout_force_brute(*m) for m in machines)


def partie2(machines):
    return sum(cout_cramer(aX, aY, bX, bY, pX + DECALAGE, pY + DECALAGE)
               for aX, aY, bX, bY, pX, pY in machines)


if __name__ == '__main__':
    machines = lire_machines(open('input.txt').read())
    print(partie1(machines))
    print(partie2(machines))
