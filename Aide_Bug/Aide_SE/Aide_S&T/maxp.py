import threading
import networkx as nx
import matplotlib.pyplot as plt
import random
import time 

class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run


class TaskSystem:
    def __init__(self, listeTaches, precedences):
        self.listeTaches = listeTaches
        self.precedences = precedences
        self.graph = self.graphique()



    def getDependencies(self, nomTache):
        listeDep = self.precedences.get(nomTache)
        return listeDep

    def runSeq(self): 
        tacheExecutees = []  # Initialisation d'une liste vide pour stocker les tâches exécutées.

        while len(tacheExecutees) < len(self.precedences):  # tant que le nombre de tâches exécutées est inférieur au nombre total de tâches à exécuter
            for cle, valeur in self.precedences.items():
                if cle not in tacheExecutees and set(valeur).issubset(tacheExecutees):  # Si la tâche n'a pas encore été exécutée et que toutes ses dépendances ont été exécutées (c'est-à-dire si l'ensemble des dépendances est inclus dans l'ensemble des tâches exécutées)
                    for t in self.listeTaches:
                        if t.name == cle:
                            t.run()
                            tacheExecutees.append(cle)
                            break
    def run(self):
            tacheExecutees = []  # Initialisation d'une liste vide pour stocker les tâches exécutées.
            threads = []
            while len(tacheExecutees) < len(self.listeTaches):  # tant que le nombre de tâches exécutées est inférieur au nombre total de tâches à exécuter
                for cle, valeur in self.precedences.items():
                    if cle not in tacheExecutees and set(valeur).issubset(tacheExecutees):  # Si la tâche n'a pas encore été exécutée et que toutes ses dépendances ont été exécutées (c'est-à-dire si l'ensemble des dépendances est inclus dans l'ensemble des tâches exécutées)
                        for tache in self.listeTaches:
                            if tache.name == cle:
                                thread = threading.Thread(target=tache.run)
                                thread.start()
                                threads.append(thread)
                                tacheExecutees.append(cle)
                                break
            for thread in threads:
                thread.join()

    def graphique(self):

        A = nx.DiGraph()
        for task in self.listeTaches:
            A.add_node(task.name)
            for dep in self.precedences[task.name]:
                A.add_edge(dep, task.name)

        position = nx.spring_layout(A)
        nx.draw(A, position, with_labels = True, node_size = 1800, node_color = "darkorange", font_size = 10, font_weight = "bold")
        plt.show()

        return A
    def detTestRnd(self, test=25):
            for i in range(test):
            # on génère des valeurs aléatoires pour X,Y,Z
                x1, y1, z1 = random.randint(1, 25), random.randint(1, 25), random.randint(1, 25)
                x2, y2, z2 = x1, y1, z1

                self.X, self.Y, self.Z = x1, y1, z1
                self.run()
                set1 = (self.X, self.Y, self.Z)

                self.X, self.Y, self.Z = x2, y2, z2
                self.run()
                set2 = (self.X, self.Y, self.Z)

                # on compare les résultats des deux exécutions parallèles
                if set1 != set2:
                    print("Le système de tâche n'est pas déterminé")

            print("Le système de tâche est determiné")

    def parCost(self, runs=10):
        seq_times = []
        par_times = []

        for _ in range(runs):
            start = time.time()
            self.runSeq()
            end = time.time()
            seq_times.append(end - start)

            start = time.time()
            self.run()
            end = time.time()
            par_times.append(end - start)

        seq_avg = sum(seq_times) / len(seq_times)
        par_avg = sum(par_times) / len(par_times)

        print(f"Moyenne des temps d'exécution séquentielle: {seq_avg}")
        print(f"Moyenne des temps d'exécution parallèle: {par_avg}")