"""Advent of Code 2024, jour 12 : aire, périmètre et côtés des régions.

Un parcours avec pile (flood fill) découpe la grille en régions de même
lettre. Le périmètre compte les côtés de case qui donnent hors de la région.
Partie 2 : chaque côté de bord est représenté par son milieu (coordonnée
demi-entière) et la direction de sa normale ; un « côté » de l'énoncé est une
composante connexe de bords voisins de même normale, comptée par un second
parcours. La recherche des voisins filtre toute la liste des bords, d'où un
coût O(E^2) par région.
"""

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        return [ligne.strip() for ligne in f if ligne.strip()]


def regions(grille):
    largeur, hauteur = len(grille[0]), len(grille)
    visite = set()
    resultat = []
    for y0 in range(hauteur):
        for x0 in range(largeur):
            if (x0, y0) in visite:
                continue
            lettre = grille[y0][x0]
            region = []
            a_visiter = [(x0, y0)]
            while a_visiter:
                x, y = a_visiter.pop()
                if (x, y) in visite:
                    continue
                visite.add((x, y))
                region.append((x, y))
                for dx, dy in DIRECTIONS:
                    xv, yv = x + dx, y + dy
                    if (0 <= xv < largeur and 0 <= yv < hauteur
                            and grille[yv][xv] == lettre):
                        a_visiter.append((xv, yv))
            resultat.append(region)
    return resultat


def perimetre(points):
    return sum(1 for x, y in points for dx, dy in DIRECTIONS
               if (x + dx, y + dy) not in points)


def nb_cotes(points):
    # Bords : (milieu x, milieu y, normale sortante).
    bords = [(x + dx / 2, y + dy / 2, (dx, dy))
             for x, y in points for dx, dy in DIRECTIONS
             if (x + dx, y + dy) not in points]
    visite = set()
    cotes = 0
    for bord in bords:
        if bord in visite:
            continue
        cotes += 1
        a_visiter = [bord]
        while a_visiter:
            x, y, normale = a_visiter.pop()
            if (x, y, normale) in visite:
                continue
            visite.add((x, y, normale))
            # Bords voisins (milieu décalé d'une case) de même normale.
            for dx, dy in DIRECTIONS:
                for x1, y1, normale1 in bords:
                    if (x1, y1) == (x + dx, y + dy) and normale1 == normale:
                        a_visiter.append((x1, y1, normale1))
    return cotes


def partie1(grille):
    return sum(len(region) * perimetre(set(region))
               for region in regions(grille))


def partie2(grille):
    return sum(len(region) * nb_cotes(set(region))
               for region in regions(grille))


grille = lire_entree('input.txt')
print('Partie 1 :', partie1(grille))
print('Partie 2 :', partie2(grille))
