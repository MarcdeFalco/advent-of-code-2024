"""Advent of Code 2024, jour 9 : compactage d'un disque.

Le disque est décrit par une liste de zones [début, longueur, identifiant]
(identifiant None pour une zone libre).
Partie 1 : on parcourt les fichiers de droite à gauche et on déplace leurs
blocs un par un vers le prochain bloc libre à gauche (curseur next_free),
jusqu'à ce que les deux curseurs se croisent ; la somme de contrôle est
accumulée à la volée.
Partie 2 : pour chaque fichier, du plus grand identifiant au plus petit, on
cherche la première zone libre assez grande à sa gauche et on y déplace le
fichier en entier (coût O(F * Z)).
"""


def lire_entree(nom_fichier):
    with open(nom_fichier) as f:
        carte = f.read().strip()
    zones = []
    debut = 0
    for i, c in enumerate(carte):
        longueur = int(c)
        identifiant = i // 2 if i % 2 == 0 else None
        zones.append([debut, longueur, identifiant])
        debut += longueur
    return zones


def partie1(zones):
    somme = 0
    next_free = zones[1][0]     # prochain bloc libre (à gauche)
    free_index = 1              # indice de la zone libre qui le contient
    for debut, longueur, identifiant in reversed(zones):
        if identifiant is None:
            continue
        position = debut + longueur - 1     # dernier bloc du fichier
        if next_free >= position:
            # Les curseurs se sont croisés : le fichier reste en place.
            for p in range(debut, position + 1):
                somme += p * identifiant
            continue
        while next_free < position and position >= debut:
            debut_libre, longueur_libre, _ = zones[free_index]
            somme += next_free * identifiant
            position -= 1
            if next_free + 1 < debut_libre + longueur_libre:
                next_free += 1
            else:
                # Zone libre épuisée : on passe à la prochaine zone libre non
                # vide (les zones libres sont aux indices impairs).
                next_free = position
                while free_index + 2 < len(zones):
                    free_index += 2
                    if zones[free_index][1] > 0:
                        next_free = zones[free_index][0]
                        break
        # Plus de place à gauche : les blocs restants ne bougent pas.
        while position >= debut:
            somme += position * identifiant
            position -= 1
    return somme


def partie2(zones):
    zones = [zone[:] for zone in zones]
    for fichier in reversed(zones):
        if fichier[2] is None:
            continue
        for libre in zones:
            # Zone libre assez grande et située à gauche du fichier.
            if (libre[2] is None and libre[1] >= fichier[1]
                    and libre[0] < fichier[0]):
                fichier[0] = libre[0]
                libre[0] += fichier[1]
                libre[1] -= fichier[1]
                break
    somme = 0
    for debut, longueur, identifiant in zones:
        if identifiant is not None:
            somme += sum((debut + k) * identifiant for k in range(longueur))
    return somme


zones = lire_entree('input.txt')
print('Partie 1 :', partie1(zones))
print('Partie 2 :', partie2(zones))
