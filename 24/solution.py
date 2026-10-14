"""Advent of Code 2024, jour 24 : additionneur à réparer.

Partie 1 : chaque fil est défini par une porte ; on évalue récursivement les
sorties zNN et on lit le nombre binaire obtenu.
Partie 2 : le circuit doit être un additionneur à propagation de retenue dont
quatre paires de fils ont été échangées. On construit l'additionneur modèle
(s_i = x_i ^ y_i ^ c_{i-1}, c_i = (x_i & y_i) | ((x_i ^ y_i) & c_{i-1})) et on
unifie chaque sortie réelle avec le modèle, à la commutativité près. Au
premier désaccord, on cherche dans les sorties suivantes le sous-arbre qui
aurait dû être là, et on échange les deux fils.
"""

NB_BITS = 46  # sorties z00 à z45
OPERATIONS = {'AND': '&', 'OR': '|', 'XOR': '^'}


def lire_entree(lignes):
    valeurs = {}
    portes = {}
    for ligne in lignes:
        if ':' in ligne:
            fil, valeur = ligne.split(': ')
            valeurs[fil] = int(valeur)
        if '->' in ligne:
            a, op, b, _, sortie = ligne.split()
            portes[sortie] = (a, op, b)
    return valeurs, portes


# Partie 1

def valeur(fil, valeurs, portes):
    if fil in valeurs:
        return valeurs[fil]
    a, op, b = portes[fil]
    va = valeur(a, valeurs, portes)
    vb = valeur(b, valeurs, portes)
    if op == 'OR':
        return va | vb
    if op == 'XOR':
        return va ^ vb
    return va & vb


def partie1(valeurs, portes):
    sorties = sorted((f for f in portes if f[0] == 'z'), reverse=True)
    return int(''.join(str(valeur(f, valeurs, portes)) for f in sorties), 2)


# Partie 2 : arbres d'expressions

class Var:
    def __init__(self, nom):
        self.nom = nom

    @property
    def sortie(self):
        return self.nom


class Op:
    def __init__(self, op1, op, op2, sortie=None):
        self.op1 = op1
        self.op = op
        self.op2 = op2
        self.sortie = sortie  # nom du fil qui porte ce résultat


def additionneur_modele(bits=NB_BITS):
    """Expressions des bits de la somme de x[0..bits-1] et y[0..bits-1]."""
    somme = [Op(Var('x00'), '^', Var('y00'))]
    retenue = Op(Var('x00'), '&', Var('y00'))
    for i in range(1, bits):
        xi = Var('x%02d' % i)
        yi = Var('y%02d' % i)
        somme.append(Op(Op(xi, '^', yi), '^', retenue))
        retenue = Op(Op(xi, '&', yi), '|', Op(Op(xi, '^', yi), '&', retenue))
    return somme


def additionneur_lu(portes):
    """Expressions des sorties z00..z45 du circuit de l'entrée."""
    def construit(fil):
        if fil[0] in 'xy':
            return Var(fil)
        a, op, b = portes[fil]
        return Op(construit(a), OPERATIONS[op], construit(b), sortie=fil)

    return [construit('z%02d' % i) for i in range(NB_BITS)]


def unifie(e, modele):
    """None si e et modele s'unifient (à la commutativité près), sinon
    un couple (sortie, cible) : sortie est le fil du premier désaccord et
    cible le sous-arbre attendu dans le modèle."""
    if type(e) is not type(modele):
        return (e.sortie, modele)
    if isinstance(e, Var):
        if e.nom == modele.nom:
            return None
        return (e.sortie, modele)
    if e.op != modele.op:
        return (e.sortie, modele)
    direct = (unifie(e.op1, modele.op1), unifie(e.op2, modele.op2))
    if direct == (None, None):
        return None
    # un seul opérande s'unifie dans l'ordre direct : on renvoie le désaccord
    # de l'autre sans essayer l'ordre inverse
    if direct[0] is None:
        return direct[1]
    if direct[1] is None:
        return direct[0]
    inverse = (unifie(e.op1, modele.op2), unifie(e.op2, modele.op1))
    if inverse == (None, None):
        return None
    if inverse[0] is None:
        return inverse[1]
    return inverse[0]


def cherche_sous_expression(e, cible):
    """Fil du premier sous-arbre de e qui s'unifie avec cible, ou None."""
    if type(e) is not type(cible):
        return None
    if isinstance(e, Var):
        return e.nom if e.nom == cible.nom else None
    if unifie(e, cible) is None:
        return e.sortie
    gauche = cherche_sous_expression(e.op1, cible)
    if gauche is not None:
        return gauche
    return cherche_sous_expression(e.op2, cible)


def cherche_par_sortie(e, fil):
    if e.sortie == fil:
        return e
    if isinstance(e, Var):
        return None
    gauche = cherche_par_sortie(e.op1, fil)
    if gauche is None:
        return cherche_par_sortie(e.op2, fil)
    return gauche


def remplace(e, fil, op1, op, op2):
    """Remplace le contenu de chaque nœud de sortie fil dans e."""
    if e.sortie == fil:
        e.op1, e.op, e.op2 = op1, op, op2
    if isinstance(e, Var):
        return
    remplace(e.op1, fil, op1, op, op2)
    remplace(e.op2, fil, op1, op, op2)


def echange(expressions, fil1, fil2):
    """Échange le contenu des deux nœuds désignés par leurs fils."""
    noeud1, noeud2 = None, None
    for e in expressions:
        if noeud1 is None:
            noeud1 = cherche_par_sortie(e, fil1)
        if noeud2 is None:
            noeud2 = cherche_par_sortie(e, fil2)
    contenu1 = (noeud1.op1, noeud1.op, noeud1.op2)
    contenu2 = (noeud2.op1, noeud2.op, noeud2.op2)
    for e in expressions:
        remplace(e, fil1, *contenu2)
        remplace(e, fil2, *contenu1)


def partie2(portes):
    modele = additionneur_modele()
    reel = additionneur_lu(portes)
    echanges = []
    for i in range(NB_BITS):
        desaccord = unifie(reel[i], modele[i])
        if desaccord is not None:
            fil, cible = desaccord
            # le sous-arbre attendu a été branché ailleurs : on le cherche
            # dans les sorties suivantes
            for j in range(i + 1, NB_BITS):
                autre = cherche_sous_expression(reel[j], cible)
                if autre is not None:
                    echange(reel, fil, autre)
                    echanges += [fil, autre]
                    break
    return ','.join(sorted(echanges))


if __name__ == '__main__':
    valeurs, portes = lire_entree(open('input.txt').read().strip().split('\n'))
    print(partie1(valeurs, portes))
    print(partie2(portes))
