n = int(input("Entrez le nombre de cannibales : "))
print("Il y a ", n, " et de ce fait", n, "missionnaires")

p = int(input("Entrez le nombre maximum de personnes que la barque peut contenir: "))
print("La barque peut contenir maximum ", p, " personnes")

# missionnaires puis cannibales puis position du bateau
memoire = []

def trouver_successeur(tableau) :
    resultats = []
    if tableau[2] == 1 :
        # Si la position de la barque est à droite
        valeurP = (-1)
    else :
        # Si la position de la barque est à gauche
        valeurP = 1 
    for m in range(0, p+1): 
        for c in range(0, p+1):
            if m + c <= p and m + c != 0:
                etats = [tableau[0]+ valeurP*m, tableau[1] + valeurP*c, 1-tableau[2]]
                if tab_valide(etats):
                    resultats.append(etats)
    return resultats

def tab_valide(tableau) : 
    if (tableau[0] < 0 or tableau[1] < 0 or tableau[0] > n or tableau[1] > n):
        return False 
    if (tableau[0] > tableau[1] and tableau[0] != 0) or (tableau[1] > tableau[0] and tableau[1] != 0):
        return False 
    return True 
    
def checkMemoire(etat) : 
    global memoire
    if etat in memoire : 
        return False
    else : 
        memoire.append(etat)
        return True 

def solution(etat) :
    if etat == [0,0,0]  :
        print("Le programme est terminé")
        return True
    successeurs = trouver_successeur(etat)
    for s in successeurs:
        if checkMemoire(s):
            if solution(s):
                return True
    return False

solution([n, n, 0])
