#tentative de correction 3, pfff changement d'autre focntion la boule infinie persiste toujours, peut etre faut-il retravailler tout le raisonnement
import random
import heapq
import time


class Taquin:
    def __init__(self, environnement, heuristique, parent=None, mouvement=None):
        self.environnement = environnement
        self.parent = parent
        self.mouvement = mouvement
        self.h = 0
        if parent is None:
            self.g = 0
            self.chemin = ""
        else:
            self.chemin = parent.chemin + self.mouvement
            self.g = parent.g + 1
        self.f = self.h + self.g
        self.final = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.heuristique = heuristique
        self.heuristiqueFonction()


    def heuristiqueFonction(self):
        poids = [
            [36, 12, 12, 4, 1, 1, 4, 0],  # π1
            [8, 7, 6, 5, 4, 3, 2, 1],  # π2 = π3
            [8, 7, 6, 5, 4, 3, 2, 1],  # π4 = π5
            [1, 1, 1, 1, 1, 1, 1, 1],  # π6
        ]
        normalization = [4, 1, 1, 4, 4, 1]  # p1, p2, p3, p4, p5, p6

        distance = 0
        for i in range(9):
            if self.environnement[i] != self.final[i] and self.environnement[i] != 8:
                distance += poids[self.heuristique - 1][self.environnement[i]] * abs(self.environnement[i] // 3 - i // 3) + abs(
                    self.environnement[i] % 3 - i % 3)

        distance //= normalization[self.heuristique - 1]
        self.h = distance
        self.f = self.h + self.g

    def voisins(self):
        voisins = []
        index_vide = self.environnement.index(8)

        mouvements = {
            'N': (index_vide - 3, 'N'),
            'S': (index_vide + 3, 'S'),
            'E': (index_vide + 1, 'E') if (index_vide + 1) % 3 != 0 else None,
            'O': (index_vide - 1, 'O') if (index_vide - 1) % 3 != 2 else None
        }

        for direction, mouvement in mouvements.items():
            if mouvement is not None and 0 <= mouvement[0] < 9:
                nouvel_environnement = self.environnement.copy()
                nouvel_environnement[index_vide], nouvel_environnement[mouvement[0]] = nouvel_environnement[mouvement[0]], nouvel_environnement[index_vide]
                voisins.append(Taquin(nouvel_environnement, self.heuristique, self, mouvement[1]))

        return voisins

    def __str__(self):
        return str(self.environnement)

    def __eq__(self, other):
        if isinstance(other, Taquin):
            return self.environnement == other.environnement
        return False

    def __lt__(self, other):
        if isinstance(other, Taquin):
            return self.f < other.f
        return False

    @staticmethod
    def astar(taquin_initial):
        frontiere = [taquin_initial]
        explore = set()
        while frontiere:
            current = heapq.heappop(frontiere)
            if current.environnement == current.final:
                return current.chemin
            explore.add(tuple(current.environnement))

            for voisin in current.voisins():
                if tuple(voisin.environnement) not in explore:
                    heapq.heappush(frontiere, voisin)

def main():
    environnement_initial = [1, 2, 5, 3, 4, 0, 6, 7, 8]
    heuristique = 1 # Choisir l'heuristique (1 à 6)

    taquin_initial = Taquin(environnement_initial, heuristique)
    start_time = time.time()
    solution = Taquin.astar(taquin_initial)
    end_time = time.time()

    if solution:
        print("Solution trouvée:", solution)
        print("Longueur de la solution:", len(solution))
    else:
        print("Aucune solution trouvée.")
    print("Temps de calcul:", end_time - start_time, "secondes")


if __name__ == "__main__":
    main()
