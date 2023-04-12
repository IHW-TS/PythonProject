frontiere = []
listExpense = []
N = 3
maxFrontiere = 1


class taquin:
    def __init__(self, tab, parent):
        self.tab = tab
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0
        self.chemin = ""

    def but(self):
        for i in range(0, len(self.tab) - 1):
            if self.tab[i] > self.tab[i + 1]:
                return 0
        return 1


def graphSearch():
    while len(frontiere) > 0:
        s = frontiere.pop(0)
        print(s.tab)
        print("A")
        if s.but():
            return afficheSolution(s)
        else:
            expense(s)
            print("new etape")
    return print("Aucune solution")


#tu fais une recursion ca bouffe trop de memoire et quand je run ca m'affiche la solution (j'ai pas verifier si elle est correcte tu verifira) et a la fin t'as une erreur genre "maximum recursion depth exceeded while calling a Python object"
# j'ai modifier t'as fonction avec une boucle while 



def expense(etat):
    listSuccesseur = actionsPossibles(etat)
    listExpense.append(etat)

    i = 0
    while i<len(listSuccesseur):
        if i not in listExpense:
            if listSuccesseur[i] not in listExpense:
                if len(frontiere)==0:
                    frontiere.append(listSuccesseur[i])
                    i+=1
                else:
                    j=0
                    while j < len(frontiere) and frontiere[j].f < listSuccesseur[i].f: # j'ai enlevé le -1 sinon il porends pas en compte le dernier resultat de la liste et inversé l'ordre pour eviter.
                    # j'ai inverser l'ordre comme ca j est verifier avant de comparer les valeurs de f 
                        j+=1
                    if j<len(frontiere):
                        frontiere.insert(j, listSuccesseur[i])
                    else:
                        frontiere.append(listSuccesseur[i])
                    i+=1

        else:
            i+=1

    while i < len(listSuccesseur):
        if listSuccesseur[i] not in listExpense:
            if listSuccesseur[i] not in listExpense:
                if len(frontiere) == 0:
                    frontiere.append(listSuccesseur[i])
                    i += 1
                else:
                    j = 0
                    while j < len(frontiere) and frontiere[j].f < listSuccesseur[i].f: 
                        j += 1
                    if j < len(frontiere):
                        frontiere.insert(j, listSuccesseur[i])
                    else:
                        frontiere.append(listSuccesseur[i])
                    i += 1

        else:
            i += 1


def actionsPossibles(etat):
    tab = etat.tab
    coupSuivant = ()
    nouvEtats = []

    x = tab.index(N * N - 1)
    if x < N:
        if x == 0:
            coupSuivant = ('S', 'E')
        elif x == N - 1:
            coupSuivant = ('S', 'O')
        else:
            coupSuivant = ('S', 'O', 'E')
    elif x >= N * (N - 1):
        if x == N * (N - 1):
            coupSuivant = ('N', 'E')
        elif x == (N * N) - 1:
            coupSuivant = ('N', 'O')
        else:
            coupSuivant = ('N', 'E', 'O')
    else:
        if x % N == N % N:
            coupSuivant = ('N', 'S', 'E')
        elif x % N == N - 1:
            coupSuivant = ('N', 'S', 'O')
        else:
            coupSuivant = ('N', 'O', 'E', 'S')
    print(coupSuivant)

    v = 0
    for i in coupSuivant:
        modif = tab.copy()
        if i == 'N':
            sauvegarde = modif[x]
            modif[x] = modif[x - N]
            modif[x - N] = sauvegarde
        elif i == 'S':
            sauvegarde = modif[x]
            modif[x] = modif[x + N]
            modif[x + N] = sauvegarde
        elif i == 'E':
            sauvegarde = modif[x]
            modif[x] = modif[x + 1]
            modif[x + 1] = sauvegarde
        else:  # vers O
            sauvegarde = modif[x]
            modif[x] = modif[x - 1]
            modif[x - 1] = sauvegarde

        nouvEtats.append(taquin(modif, etat))
        nouvEtats[v].g = etat.g + 1
        nouvEtats[v].h = calculH(modif, x)
        nouvEtats[v].f = nouvEtats[v].g + nouvEtats[v].h
        nouvEtats[v].chemin = etat.chemin + i
        print("f:")
        print(nouvEtats[v].f)
        print(nouvEtats[v].tab)
        print(nouvEtats[v].chemin)
        v += 1

    return nouvEtats



def calculH(tab, X):
    h = 0
    pi = [[36, 12, 12, 4, 1, 1, 4, 1, 0], [8, 7, 6, 5, 4, 3, 2, 1, 0], [8, 7, 6, 5, 4, 3, 2, 1, 0], [8, 7, 6, 5, 3, 2, 4, 1, 0], [8, 7, 6, 5, 3, 2, 4, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1]]
    coeffPair = 1
    coeffImpair = 4
    for i in tab:
        posTab = tab.index(i)
        posCol = posTab//N
        posLig = posTab%N
        posMan = abs(posLig-(i%N))+abs(posCol-(i//N))
        h = h+ (posMan * (pi[0][i])) 

    return h//4



def afficheSolution(s):
    print("Solution!")
    print (s.tab)
    print(s.chemin)



init = taquin([0,1,2,3,4,5,8,6,7], None)
frontiere.insert(0,init)

graphSearch()


