"""Advent of Code 2024, jour 17 : machine à 3 bits.

Interprète direct des huit instructions sur les registres A, B, C, avec la
distinction entre opérande littéral et opérande « combo ».
Partie 1 : sortie du programme pour la valeur initiale de A.
Partie 2 : on cherche A tel que le programme affiche son propre code.
L'interprète peut s'arrêter dès que la sortie diverge du programme (arrêt
anticipé). La valeur de A est écrite en dur, et le script se contente de
la vérifier.
"""

A_TROUVE = 105981155568026  # valeur de la partie 2


def lire_entree(lignes):
    registres = {nom: int(lignes[i].split()[2]) for i, nom in enumerate('ABC')}
    programme = list(map(int, lignes[4].split()[1].split(',')))
    return registres, programme


def simule(programme, registres_initiaux, A, arret_anticipe=False):
    """Exécute le programme avec A comme valeur initiale du registre A.
    Avec arret_anticipe, on s'arrête dès que la sortie diffère du programme."""
    reg = dict(registres_initiaux)
    reg['A'] = A

    def combo(op):
        if op <= 3:
            return op
        return reg['ABC'[op - 4]]  # 4, 5, 6 : registres A, B, C

    pc = 0
    sortie = []
    while pc < len(programme):
        instr, op = programme[pc], programme[pc + 1]
        pc += 2
        if instr == 0:
            reg['A'] = reg['A'] >> combo(op)
        elif instr == 1:
            reg['B'] = reg['B'] ^ op
        elif instr == 2:
            reg['B'] = combo(op) % 8
        elif instr == 3:
            if reg['A'] != 0:
                pc = op
        elif instr == 4:
            reg['B'] = reg['B'] ^ reg['C']
        elif instr == 5:
            sortie.append(combo(op) % 8)
            n = len(sortie)
            if arret_anticipe and (n > len(programme)
                                   or sortie[-1] != programme[n - 1]):
                return sortie
        elif instr == 6:
            reg['B'] = reg['A'] >> combo(op)
        elif instr == 7:
            reg['C'] = reg['A'] >> combo(op)
    return sortie


def partie1(registres, programme):
    return ','.join(map(str, simule(programme, registres, registres['A'])))


def partie2(registres, programme):
    assert simule(programme, registres, A_TROUVE, True) == programme
    return A_TROUVE


if __name__ == '__main__':
    lignes = open('input.txt').read().strip().split('\n')
    registres, programme = lire_entree(lignes)
    print(partie1(registres, programme))
    print(partie2(registres, programme))
