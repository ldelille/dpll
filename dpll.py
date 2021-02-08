# ######################################################################
#
# Template pour coder l'algorithme DPLL
# 

# Une clause disjonctive est simplement une liste de liste d'entiers
# La négation est codé avec le signe "-"
# 
# Par exemple, la formule
#
#     x1 /\ (x2 \/ ~x3 \/ x4) /\ ~x5
#
# est codée comme [ [1] , [2 , -3 , 4] , [-5] ]

# ######################################################################
# 
# Templates
# 


def unitPropagateSingle(clause, xb):
    # Entrées:
    #  - clause : une liste d'entier (donc: une clause)
    #  - xb     : un entier (donc un littéral)

    if not clause:
        return None
    if xb not in clause and -xb not in clause:
        return clause
    if xb in clause:
        return None
    clause.remove(-xb)
    return clause

    # Doit retourner une clause sans xb, ou None si xb rend la clause toujours vrai.
    # La clause rendue ne doit jamais être vide


# print(unitPropagateSingle([1], -1))

def test1():
    assert unitPropagateSingle([1, 2, 3, 4], -1) == [2, 3, 4]
    assert unitPropagateSingle([2, 3, 4, 5], -1) == [2, 3, 4, 5]
    assert unitPropagateSingle([2, 3, 4, 1], -1) == [2, 3, 4]
    assert unitPropagateSingle([1, 2, 3, 4], 1) == None
    assert unitPropagateSingle([2, 3, 4, 1], 1) == None
    assert unitPropagateSingle([1, 2, 3, 4], 5) == [1, 2, 3, 4]
    assert unitPropagateSingle([1, 2, 3, -5], 5) == [1, 2, 3]
    assert unitPropagateSingle([1, -2, 3, 4], 2) == [1, 3, 4]
    assert unitPropagateSingle([1], 1) == None


test1()



#If a clause is impossible unitPropagate returns an empty list.
def unitPropagate(clauses, xb):
    # Meme chose, mais sur une liste de liste d'entiers
    # (donc une formule CNF générale)
    # print("starting unit propagate with arguments: ", clauses,"xb:", xb )
    result = []
    if not clauses:
        return None
    for clause in clauses:
        propagated_clause = unitPropagateSingle(clause, xb)
        if propagated_clause == []:
            return []
        if propagated_clause:
            result.append(propagated_clause)
    if len(result) == 0:
        return None
    else:
        return result


def test_unitPropagate():
    assert unitPropagate([[2, 3, 4, 5], [1, 2, 3, 4, ]], -1) == [[2, 3, 4, 5], [2, 3, 4]]
    assert unitPropagate([[2, 3, 4, 5], [1, -2, 3, 4, ]], -2) == [[3, 4, 5]]
    assert unitPropagate([[2], [-2]], -2) == []



test_unitPropagate()


def findPureLits(clauses):
    # clauses : toujours une formule CNF
    # Retourne la liste des littéraux qui apparaissent avec une seule
    # polarité dans la formule
    dic = {}
    for clause in clauses:
        for elem in clause:
            if -elem in dic:
                dic[elem] = 0
                dic[-elem] = 0
            elif elem in dic:
                if dic[elem] == 0:
                    continue
            else:
                dic[elem] = 1
    return [x for x in dic if dic[x] == 1]


def test2():
    assert set(findPureLits([[1, 2, -4], [-1], [2, 5, -8], [-5, 3, 8]])) == set([2, 3, -4])
    assert set(findPureLits([[1, 2], [-1], [2, -1], [-2, 3, 8]])) == set([3, 8])


test2()


def dpll(clauses):
    # En entrée : une liste de clauses -- c-a-d une formule CNF
    if clauses is None:    #found a valid path
        return True
    if len(clauses) == 0:    #if Unit propagate returned [], path was impossible
        return False
    # find unitary clause:
    for clause in clauses:
        if len(clause) == 1:
            return dpll(unitPropagate(clauses, clause[0]))
    for pure_lit in findPureLits(clauses):
        return dpll(unitPropagate(clauses, pure_lit))
    for clause in clauses:
        for elem in clause:
            return dpll(unitPropagate(clauses, elem)) or dpll(unitPropagate(clauses, -elem))


def test3():
    assert dpll([[1, 2, 3], [1, 2, -3], [1, -2, 3], [1, -2, -3], [-1, 2, 3], [-1, 2, -3], [-1, -2, 3],
                 [-1, -2, -3]]) == False
    assert dpll([[1, -1]]) == True
    assert dpll([[1, 2, 3, -4], [-1, 2, -3], [-1, -2, 3], [-1, -2, -3], [4]]) == True
    assert dpll(
        [[1, -2, 3, -4, -6, -8], [2, 3], [2, 3, 4, 5, 8], [2, -4, 5, -6], [2, -3, 6, -8], [2, -4, 6, -7], [-2, -3],
         [-2, -3, -4], [-2, 3, 4], [-2, -4, 5], [-2, -5, 6], [-7, -8], [7, 8], [-7, 8]]) ==True


test3()


#Ma fonction se comporte bein sur ces cas de test, mais renvoie False trop souvent sur les cas du kit....

# ######################################################################
#
# Votre fonction passe-t-elle les exemples de
# http://www.satcompetition.org/ donnés dans le kit ?
#
# Pour faire tourner les tests:
#  - ajuster la valeur de path: les fichiers dans UNSAT sont... unsat
#    et ceux dans SAT sont... sat.
#  - Décommentez la ligne "files = ..."


from os import listdir
from os.path import isfile, join
import random

path = "SATEXsmall/SAT/"  # À AJUSTER AU BESOIN

files = []
# files = [f for f in listdir(path) if isfile(join(path, f))]

random.shuffle(files)

for f in files:
    print(f)
    file = open(join(path, f), "r")

    l = file.readline()

    while l[0] == "c":
        l = file.readline()

        s = []
    while l:
        s.extend(l.split())
        l = file.readline()

    clauses = []
    c = []
    for i in range(4, len(s) - 2):
        if s[i] == "0":
            clauses.append(c)
            c = []
        else:
            c.append(int(s[i]))

    print(dpll(clauses))
