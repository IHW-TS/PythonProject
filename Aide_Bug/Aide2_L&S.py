#tentative de resolution du porbleme de la boucle infinie en essayant un autre fonction def TrouverMouvement()
import random
import heapq

class Taquin:
    def __init__(self, environnement, heuristique, parent=None, mouvement=None):
        self.environnement = environnement
        self.parent = parent
        self.mouvement = mouvement
        self.h = 0
        if parent is None:
            self.g = 0
            self.chemin = "..."
        else:
            self.chemin = parent.chemin + self.mouvement
            self.g = parent.g + 1
        self.final = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.heuristique = heuristique
        self.heuristiqueFonction()
        self.f = self.h + self.g

    def __lt__(self, other):
        return self.f < other.f

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
        self.h = sum([self.pi[i] * self.epsilon[i] for i in range(len(self.pi))]) + self.phi

    def trouverMouvement(self):
        # Ajout de la fonction trouverMouvement
        index_vide = self.environnement.index(8)
        distance = [abs(index_vide - i) for i in range(9)]
        mouvements = [
            (-3, 1, 0),
            (3, -1, 0),
            (1, 0, 1),
            (-1, 0, 1)
        ]
        epsilon = [0] * 9
        for delta_x, delta_y, signe in mouvements:
            x = index_vide % 3 + delta_x
            y = index_vide // 3 + delta_y
            if 0 <= x < 3 and 0 <= y < 3:
                index = y * 3 + x
                val = self.environnement[index]
                epsilon[val] = distance[val] * signe
        return epsilon

    def est_solution(self):
        return self.environnement == self.final

    def voisins(self):
        voisins = []
        index_vide = self.environnement.index(8)

        mouvements = [
            ("N", -3),
            ("S", 3),
            ("E", 1),
            ("O", -1)
        ]

        for direction, delta in mouvements:
            nouvel_index = index_vide + delta
            if 0 <= nouvel_index < 9 and (index_vide % 3 + delta % 3) != 0:
                nouvel_environnement = self.environnement.copy()
                nouvel_environnement[index_vide], nouvel_environnement[nouvel_index] = nouvel_environnement[nouvel_index], nouvel_environnement[index_vide]
                voisin = Taquin(nouvel_environnement, self.heuristique, parent=self, mouvement=direction)
                voisins.append(voisin)
        
        return voisins

    def a_star(self):
        file_priorite = [(self.f, 0, self)]
        heapq.heapify(file_priorite)
        etats_deja_visites = set()

        while file_priorite:
            _, _, etat_courant = heapq.heappop(file_priorite)
            if etat_courant.est_solution():
                return etat_courant.chemin
            if tuple(etat_courant.environnement) not in etats_deja_visites:
                etats_deja_visites.add(tuple(etat_courant.environnement))
                for voisin in etat_courant.voisins():
                    voisin.g = etat_courant.g + 1
                    voisin.heuristiqueFonction()
                    voisin.f = voisin.g + voisin.h
                    heapq.heappush(file_priorite, (voisin.f, voisin.g, voisin))
        return None

def nbAleatoire():
     etFinal = [0,1,2,3,4,5,6,7,8]
     etat = random.sample(etFinal, 9)
     print(etat) 
     return etat 

def choisirHeuristique():
    while True:
        hChoisi = int(input("Choisissez une heuristique entre 1 et 6 : "))
        if 1 <= hChoisi <= 6:
            break
        print("La valeur est invalide, entrez une nouvelle valeur")

    print("L'heuristique choisie est ", hChoisi)
    return hChoisi
    

env = nbAleatoire()
heuristique = choisirHeuristique()
initial = Taquin(env, heuristique)
solution = initial.a_star()
if solution is not None:
    print("Solution:", solution)
else:
    print("Pas de solution trouvée. Veuillez réessayer avec un autre état initial ou une autre heuristique.")
