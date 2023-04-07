#tentative de correction mais le porgramme reste sur un boucle infinie 
import random
import heapq
import time


class Taquin:
    def __init__(self, environnement, heuristique, parent=None, mouvement=None, pi=None, phi=None, epsilon=None): # J'AI PASSE 10mn DE MA VIE A CHERCHER UN BUG ET CA VIENS DE CETTE PTN DE LIGNE DE MERDE FAITES VOS PRIERE LUNDI C TOUS CE QUE J'AI A DIRE C PAS POSSIBLE AUTANT DE FAUTE D'INATENTION C TROPPPPPPPPPPPPPPP 10MNNNNNNNNNNNNNN J'AURAI PU MANGER ET REVENIR (lm'erreur est la : _init_ correction : __init__)
        self.environnement = environnement
        self.parent = parent 
        self.mouvement = mouvement 
        self.h = 0
        if parent == None : 
            self.g=0
            self.chemin = "..." # LES 3 POITNS C POUR CLC ENLEVER MOI CA 
        else :
            self.chemin = parent.chemin + self.mouvement 
            self.g = parent.g + 1 #on devrait pas le mettre dans une fonction ça ? #Reponse a ton commentaire : NAN LOUISE Y PAS BESOIN MERDE TU VAS PAS CR2E UNE FOCNTION POUR UNE LIGNE DE COMMANDE 
        self.f = self.h + self.g
        self.final = [0,1,2,3,4,5,6,7,8] # LA IL MANQUE UN CHIFFRE LE 6, VOUS ETES DEUX ET VOUS ARRRIVER A PAS LE VOIR, C POUR LES CAMERAS LES LUNETTES ?????
        self.heuristique = heuristique 
        self.pi = pi
        self.phi = phi 
        self.epsilon = epsilon
        self.heuristiqueFonction()
        self.f = self.h + self.g


#MAIS CA C LE COMBLE DU COMBLE GNGNNGNGNGNG POURQUOI PAS FAIRE UN FONCTION MEMOIRE POUR MEMORISER.... DES CONNERIES OUI LA JE SERAIS D'ACCORD...
#   def memoire(etat):
#      if etat not in memoire :
#          memoire = etat 

    def __lt__(self, other): # permet de définir l'ordre entre deux instances
        return self.f < other.f
    
# LA FOCNTION CALCULLE ECLATER AU SOL LIMITE ELLE LES PARAMETRE DANSE Y A PAS DE SENSE 
    def calcul(self):
        if len(self.pi) != 9:
            raise ValueError("La longueur de la liste pi est incorrecte.")
        add = [self.pi[i] * self.epsilon[i] for i in range(0, 9)]
        total = sum(add) // self.phi
        return total
        

# j'ai enlevé le parametre heuri, il sert scritement rien c comme si je prenais des tomates et je mettais du ketchup dessus....
    def heuristiqueFonction(self):
        if self.heuristique == 1:
            self.pi = [36, 12, 12, 4, 1, 1, 4, 1, 0]
            self.phi = 4
        elif self.heuristique == 2:
            self.pi = [8, 7, 6, 5, 4, 3, 2, 1, 0]
            self.phi = 1
        elif self.heuristique == 3:
            self.pi = [8, 7, 6, 5, 4, 3, 2, 1, 0]
            self.phi = 4
        elif self.heuristique == 4:
            self.pi = [8, 7, 6, 5, 3, 2, 4, 1, 0]
            self.phi = 1
        elif self.heuristique == 5:
            self.pi = [8, 7, 6, 5, 3, 2, 4, 1, 0]
            self.phi = 4
        else:
            self.pi = [1, 1, 1, 1, 1, 1, 1, 1, 0]
            self.phi = 1
        self.epsilon = self.trouverMouvement()
        return self.calcul()
    
# Je peux pas implementer cette fonction avec l'algo trouver une autre maniere de raisonenr 
    def trouverMouvement(self):
        dist_mhn = [0] * 9
        etatEnCours = self.environnement

        for i in self.environnement:

            mvt = 0
            compteur = 0  
            if etatEnCours[i] != 8:
               if etatEnCours[i] != i : 
                    E = etatEnCours[i] - i
                    while (E > 3) or (E<(-3)) : 
                        if E < -3 :
                            move = "N"
                            mvt +=1
                            E = E +3 
                        if E == 3 :
                            move = "S"
                            mvt +=1
                            E = E-3
                    while E != 0 :
                        if E == -1 :
                            move = "O"
                            mvt += 1
                            E = E +1
                        if E == 1 : 
                            move = "E"  
                            mvt+= 1
                            E = E -1 
                    dist_mhn[etatEnCours[i]] = mvt

        return dist_mhn


    def est_solution(self):
        return self.environnement == self.final

    def voisins(self):
        voisins = []
        index_vide = self.environnement.index(8) # trouver l'index de la case vide qui est représentée par le chiffre 8

        mouvements = [ # définir les mouvements possibles : nord (N), sud (S), est (E), ouest (O) en fonction de leur effet sur l'index de la case vide
            ("N", -3),
            ("S", 3),
            ("E", 1),
            ("O", -1)
        ]

        for direction, delta in mouvements: # itérer sur les mouvements possibles
            nouvel_index = index_vide + delta # calculer l'index de la case après le mouvement
            if 0 <= nouvel_index < 9 and (index_vide % 3 + delta % 3) != 0: # vérifier si l'index est valide et si le mouvement ne dépasse pas les limites de la grille
                nouvel_environnement = self.environnement.copy() # copier l'environnement actuel
                nouvel_environnement[index_vide], nouvel_environnement[nouvel_index] = nouvel_environnement[nouvel_index], nouvel_environnement[index_vide] # échanger la case vide avec la nouvelle case
                voisin = Taquin(nouvel_environnement, self.heuristique, parent=self, mouvement=direction) # créer un nouvel objet Taquin représentant l'état après le mouvement
                voisins.append(voisin) # ajouter ce voisin à la liste des voisins
        
        return voisins


    def a_star(self):
        file_priorite = [(self.f, 0, self)] # initialiser la file de priorité avec l'état initial
        heapq.heapify(file_priorite) # transformer la liste en une file de priorité
        etats_deja_visites = set()  # initialiser l'ensemble des états visités

        nb_etats_visites = 0  # Ajout de la variable pour le nombre d'état recherché 

        while file_priorite: # tant que la file de priorité n'est pas vide
            _, _, etat_courant = heapq.heappop(file_priorite) # extraire l'état avec la plus petite valeur f
            if etat_courant.est_solution(): # si l'état courant est la solution, retourner le chemin
                print("Nombre d'états visités:", nb_etats_visites) # Affichage du nombre d'états visités
                return etat_courant.chemin
            if tuple(etat_courant.environnement) not in etats_deja_visites: # sinon, si l'état n'a pas été visité
                etats_deja_visites.add(tuple(etat_courant.environnement)) # l'ajouter à l'ensemble des états visités
                nb_etats_visites += 1  # Incrément de la variable pour le nombre d'état recherché 
                for voisin in etat_courant.voisins(): # parcourir les voisins de l'état courant
                    voisin.g = etat_courant.g + 1 # mettre à jour le coût g du voisin
                    voisin.h = voisin.heuristiqueFonction() # mettre à jour l'estimation heuristique h du voisin
                    voisin.f = voisin.g + voisin.h # mettre à jour la valeur f du voisin
                    heapq.heappush(file_priorite, (voisin.f, voisin.g, voisin)) # ajouter le voisin à la file de priorité
        
        print("Nombre d'états visités:", nb_etats_visites) # Affichage du nombre d'états visités si la solution n'a pas été trouvée
        return None

   
def nbAleatoire():
     etFinal = [0,1,2,3,4,5,6,7,8]
     etat = random.sample(etFinal, 9)
     print(etat) 
     return etat 

# c'est possible elle ete coder avec les pieds cette partie y a aucune relecture 
def choisirHeuristique():
    while True:
        hChoisi = int(input("Choisissez une heuristique entre 1 et 6 : "))
        if 1 <= hChoisi <= 6:
            break
        print("La valeur est invalide, entrez une nouvelle valeur")

    print("L'heuristique choisie est ", hChoisi)
    return hChoisi
    

t0 = time.time() # Temps de départ

env = nbAleatoire()
heuristique = choisirHeuristique()
initial = Taquin(env, heuristique)
solution = initial.a_star()

t1 = time.time() # Temps de fin
temps_execution = t1 - t0
temps_cpu = time.process_time()

print("Solution:", solution)
print("Temps d'exécution:", temps_execution)
print("Temps CPU:", temps_cpu)