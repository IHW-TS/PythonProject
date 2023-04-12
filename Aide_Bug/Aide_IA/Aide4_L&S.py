import random
import heapq
import time


class Taquin:
    def __init__(self, environnement, heuristique, parent=None, mouvement=None):
        self.environnement = environnement
        self.heuristique = heuristique
        self.parent = parent
        self.mouvement = mouvement
        self.g = parent.g + 1 if parent else 0
        self.h = self.heuristiqueFonction()
        self.f = self.g + self.h

    def calcul(self):
        inversion = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if self.pi[j] and self.pi[i] and self.pi[i] > self.pi[j]:
                    inversion += 1
        return (inversion + self.g) % 2

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
        return self.calcul()

    def __lt__(self, other):
        return self.f < other.f

    def trouverMouvement(self):
        return sum(abs((val - 1) % 3 - (i % 3)) + abs((val - 1) // 3 - (i // 3))
                   for i, val in enumerate(self.environnement) if val)

    def est_solution(self):
        return self.environnement == [1, 2, 3, 4, 5, 6, 7, 8, 0]
    
    def voisins(self):
        i = self.environnement.index(0)
        voisins = []
        mouvements = [('H', -3), ('B', 3), ('G', -1), ('D', 1)]
        for m, delta in mouvements:
            j = i + delta
            if 0 <= j < 9 and not (i % 3 == 2 and m == 'D') and not (i % 3 == 0 and m == 'G'):
                nouv_env = self.environnement[:]
                nouv_env[i], nouv_env[j] = nouv_env[j], nouv_env[i]
                voisins.append(Taquin(nouv_env, self.heuristique, self, m))
        return voisins


    def a_star(self):
        frontiere = [(self.f, self)]
        heapq.heapify(frontiere)
        deja_vu = set()
        deja_vu.add(tuple(self.environnement))

        while frontiere:
            _, noeud_courant = heapq.heappop(frontiere)

            if noeud_courant.est_solution():
                chemin = []
                while noeud_courant:
                    chemin.append(noeud_courant.mouvement)
                    noeud_courant = noeud_courant.parent
                return chemin[::-1][1:]

            for voisin in noeud_courant.voisins():
                voisin_tuple = tuple(voisin.environnement)
                if voisin_tuple not in deja_vu:
                    heapq.heappush(frontiere, (voisin.f, voisin))
                    deja_vu.add(voisin_tuple)

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