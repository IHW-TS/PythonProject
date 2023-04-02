






import random
frontiere = []
listExpense={}
N=3
maxFrontiere=0
Heur=0


class taquin:
    def __init__(self, tab, parent):
        self.tab = tab
        self.parent = parent
        self.f =0
        self.g =0
        self.h =0 ##a calculer dans tous les cas même le premier?
        self.chemin = "" #exemple "ONN"


    def but(self):
        ##vérifier que tab est trié
        for i in range(0,len(self.tab)-1):
            if self.tab[i]>self.tab[i+1]:
                return 0
        return 1
        """for i in self.tab:
            if self.tab[i] != i :
                return 0
            else:
                return 1"""


#A*
def graphSearch():
    while len(frontiere)>0:
            s = frontiere.pop(0)## l'élement qui va être traité
            print (s.tab)
            #print("A")
            if s.but():
                return afficheSolution(s)
            else:
                expense(s)
                print ("new etape")

    return print("Aucune solution")

def expense(etat):
    listSuccesseur = actionsPossibles(etat)
    """Ajouter l'état à la frontière
        s'il est pas déjà dans les exploré
        ajouter etat dans dictionnaire des exploré et l'enlevé s'il reste des identique dans la frontière"""
    listExpense[tuple(etat.tab)] = etat.f


    i=0

    while i<len(listSuccesseur):
        if (tuple(listSuccesseur[i].tab) not in listExpense) or ((tuple(listSuccesseur[i].tab) in listExpense) and listSuccesseur[i].f < listExpense[tuple(listSuccesseur[i].tab)]):

            if len(frontiere)==0:
                frontiere.append(listSuccesseur[i])
                i+=1
            else:
                j=0
                while j<len(frontiere) and frontiere[j].f<listSuccesseur[i].f :
                    j+=1
                if j<len(frontiere):
                    frontiere.insert(j, listSuccesseur[i])
                else:
                    frontiere.append(listSuccesseur[i])
                i+=1
        i+=1



    ##for k in listExpense: #supprime les occurences dans la frontiere de l'état qui vient d'être expensé

        """if frontiere[k].tab==etat.tab and frontiere[k].f==etat.f:
            frontiere.pop(k)
            print("pop")"""

    ##if maxFrontiere<len(frontiere): maxFrontiere=len(frontiere) ## mise en mémoire de la taille max que va avoir la frontiere


def actionsPossibles(etat):

    tab = etat.tab
    coupSuivant = ()
    nouvEtats=[]

    #suivant la place du trou on génère les états d'après, faire des if en fonction d'un N
    #on calcul les f, g, h de chacun
    #on les ajoute dans la frontière (la regénéré a chaque fois?)

    #recherhce des actions possibles à partir d'un emplacement spécifique
    x = tab.index(N*N-1)
    if x<N:
        if x==0:
            coupSuivant = ('S','E')
        elif x==N-1 :
            coupSuivant = ('S','O')
        else:
            coupSuivant = ('S','O','E')
    elif x>=N*(N-1):
        if x==N*(N-1):
            coupSuivant = ('N','E')
        elif x ==(N*N)-1 :
            coupSuivant = ('N','O')
        else:
            coupSuivant = ('N','E','O')
    else:
        if x%N == N%N:
            coupSuivant = ('N','S','E')
        elif x%N == N-1:
            coupSuivant = ('N','S','O')
        else:
            coupSuivant = ('N','O','E','S')
    #print(coupSuivant)
    #génère les résultats à partir des mouvements possible
    v=0
    for i in coupSuivant:
        #modification du taquin, effectue le mouvement
        modif = list(tab)
        if i=='N':
            #échange les deux éléments de place
            sauvegarde = modif[x]
            modif[x]=modif[x-N]
            modif[x-N]=sauvegarde
        elif i=='S':
            sauvegarde = modif[x]
            modif[x]=modif[x+N]
            modif[x+N]=sauvegarde
        elif i=='E':
            sauvegarde = modif[x]
            modif[x]=modif[x+1]
            modif[x+1]=sauvegarde
        else: #vers O
            sauvegarde = modif[x]
            modif[x]=modif[x-1]
            modif[x-1]=sauvegarde

        #crée le nouvel état
        nouvEtats.append(taquin(modif,etat))
        nouvEtats[v].g = etat.g+1
        nouvEtats[v].h = calculH(modif,x);
        nouvEtats[v].f = nouvEtats[v].g + nouvEtats[v].h
        nouvEtats[v].chemin = etat.chemin+i
        #print("f:")
        #print(nouvEtats[v].f)
        #print(nouvEtats[v].tab)
        #print(nouvEtats[v].chemin)
        v+=1
        #faire calcul de f g h dans la classe 'taquin(tab,etat).calcFGH()'
        #quescequ'on en fait? ajouter à la frontière?

    return nouvEtats


def calculH(tab, X):
    h = 0
    if N==3:
        ##pos=[[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]
        pi = [[36, 12, 12, 4, 1, 1, 4, 1, 0], [8, 7, 6, 5, 4, 3, 2, 1, 0], [8, 7, 6, 5, 4, 3, 2, 1, 0], [8, 7, 6, 5, 3, 2, 4, 1, 0], [8, 7, 6, 5, 3, 2, 4, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1, 0]]
        coeffPair = 1
        coeffImpair = 4
        for i in tab:
            posTab = tab.index(i)
            posCol = posTab//N
            posLig = posTab%N
            posMan = abs(posLig-(i%N))+abs(posCol-(i//N))
            h = h+ (posMan * (pi[Heur][i])) #a modif (pi[Heur][i])

        if (Heur+1)%2:
            return h//coeffImpair
        else:
            return h//coeffPair
    else:
        for i in tab:
            posTab = tab.index(i)
            posCol = posTab//N
            posLig = posTab%N
            posMan = abs(posLig-(i%N))+abs(posCol-(i//N))
            h = h+ (posMan * 1)

        return h//1




def afficheSolution(s):
    print("Solution!")
    print(Heur)
    print (s.tab)
    print(s.chemin)
    print(s.f)
    print(len(frontiere))
    print(len(s.chemin))

"""tab =  [0,1,2,3,4,5,6,7,8]
random.shuffle(tab)
print(tab)
for i in range (0,6):
    Heur=i
    frontiere.clear()
    init = taquin(tab, None)
    frontiere.insert(0,init)
    graphSearch()"""


for i in range (0,6):
    print("A")
    Heur=i
    frontiere.clear()
    init = taquin([3,0,2,1,5,4,7,6,8], None)
    listExpense={tuple([3,0,2,1,5,4,7,6,8]) : calculH([3,0,2,1,5,4,7,6,8],0)}
    frontiere.insert(0,init)
    print("C")
    graphSearch()
    print("B")