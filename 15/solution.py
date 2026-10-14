"""Advent of Code 2024, jour 15 : caisses dans un entrepôt.

Simulation pas à pas du robot sur la grille (indexée grille[y][x]).
Partie 1 : caisses d'une case, on avance jusqu'au bout de la file de caisses
et on déplace la première caisse au bout s'il y a de la place.
Partie 2 : caisses de largeur 2. Une poussée horizontale décale un segment de
ligne ; une poussée verticale peut entraîner un arbre de caisses, collectées
par un parcours avec pile (chaque caisse est repérée par sa moitié gauche).
On abandonne le mouvement si un mur est touché.
"""

DIRECTIONS = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}


def lire_entree(texte):
    carte, instructions = texte.strip().split('\n\n')
    return carte.split('\n'), instructions.replace('\n', '')


def prepare(lignes):
    """Grille modifiable, et position du robot (retiré de la grille)."""
    grille = [list(ligne) for ligne in lignes]
    for y, ligne in enumerate(grille):
        for x, c in enumerate(ligne):
            if c == '@':
                ligne[x] = '.'
                return grille, (x, y)


def score_gps(grille, caisse):
    return sum(100 * y + x
               for y, ligne in enumerate(grille)
               for x, c in enumerate(ligne) if c == caisse)


def partie1(lignes, instructions):
    grille, (x, y) = prepare(lignes)
    for instr in instructions:
        dx, dy = DIRECTIONS[instr]
        # longueur de la file de caisses devant le robot
        avance = 1
        while grille[y + avance * dy][x + avance * dx] == 'O':
            avance += 1
        if grille[y + avance * dy][x + avance * dx] == '.':
            # déplacer toute la file revient à déplacer la première au bout
            grille[y + dy][x + dx] = '.'
            if avance > 1:
                grille[y + avance * dy][x + avance * dx] = 'O'
            x, y = x + dx, y + dy
    return score_gps(grille, 'O')


def elargit(lignes):
    remplacement = {'O': '[]', '#': '##', '.': '..', '@': '@.'}
    return [''.join(remplacement[c] for c in ligne) for ligne in lignes]


def partie2(lignes, instructions):
    grille, (x, y) = prepare(elargit(lignes))
    for instr in instructions:
        dx, dy = DIRECTIONS[instr]
        if dy == 0:
            # poussée horizontale : on décale le segment de caisses
            avance = 1
            while grille[y][x + avance * dx] in '[]':
                avance += 1
            if grille[y][x + avance * dx] == '.':
                for i in reversed(range(1, avance + 1)):
                    grille[y][x + i * dx] = grille[y][x + (i - 1) * dx]
                x += dx
        else:
            # poussée verticale : on collecte les caisses entraînées
            a_visiter = []
            if grille[y + dy][x] == '[':
                a_visiter.append((x, y + dy))
            elif grille[y + dy][x] == ']':
                a_visiter.append((x - 1, y + dy))
            caisses = []
            bloque = grille[y + dy][x] == '#'
            while a_visiter and not bloque:
                xb, yb = a_visiter.pop()
                if (xb, yb) in caisses:
                    continue
                caisses.append((xb, yb))
                # cases au-dessus (ou au-dessous) des deux moitiés
                gauche, droite = grille[yb + dy][xb], grille[yb + dy][xb + 1]
                if gauche == '[':
                    a_visiter.append((xb, yb + dy))
                if gauche == ']':
                    a_visiter.append((xb - 1, yb + dy))
                if droite == '[':
                    a_visiter.append((xb + 1, yb + dy))
                if gauche == '#' or droite == '#':
                    bloque = True
            if bloque:
                continue
            y += dy
            # on déplace d'abord les caisses les plus éloignées du robot,
            # pour ne pas écraser une caisse pas encore déplacée
            caisses.sort(key=lambda c: -c[1] * dy)
            for bx, by in caisses:
                grille[by][bx] = grille[by][bx + 1] = '.'
                grille[by + dy][bx] = '['
                grille[by + dy][bx + 1] = ']'
    return score_gps(grille, '[')


if __name__ == '__main__':
    lignes, instructions = lire_entree(open('input.txt').read())
    print(partie1(lignes, instructions))
    print(partie2(lignes, instructions))
