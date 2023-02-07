n = int(input("Entrez le nombre de cannibales : "))
print("Il y a ", n, " et de ce fait", n, "missionnaires")

p = int(input("Entrez le nombre maximum de personnes que la barque peut contenir: "))
print("La barque peut contenir maximum ", p, " personnes")


# missionnaires puis cannibales puis position du bateau
init = [n,n,0]
memoire = []
frontiere = []

def trouver_successeur(tableau) :
    if tableau[2] == 1 :
    #Si la position de la barque est à droite
        valeurP = (-1)
    else :
    # Si la position de la barque est à gauche
        valeurP = 1 
    for m in range (2, n <= p+1) : 
        for c in range (2, n<=p+1): 
            etats = [tableau[0]+ valeurP*m, tableau[1] +valeurP*c, tableau[2]+ valeurP]
            tab_valide(tableau)    
    return etats

        
def tab_valide(tableau) : 
    if (tableau[0] + tableau[1]) >= 2*n :
        return False 
    # nb de missionnaires ou de cannibales est négatif ou supérieur à n
    if (tableau[0] < 0 and tableau[1]<0 and tableau[0] > n and tableau[1] > n) :
        return False 
    # nb de missionnaires est supérieur au nombre de cannibales sur une rive
    if (tableau[0] > 0 and tableau[0] > tableau[1]) : 
        return False 
    return True 
    
def checkMemoire(etat) : 
    global memoire
    if etat in memoire : 
        return False
    else : 
        memoire.append(etat)
        return True
    
def solution(liste, etat) :
    if etat == [0,0,0]  :
        print("Le programme est terminé")
        return
       
def treeSearch(liste) : 
    global init 
    etat = init 
    for a in range () : 
        frontiere[a] = trouver_successeur(etat)
        checkMemoire.frontiere[a]
        solution(frontiere[a])