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
        #self.verification_entrees()



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
            
    def verification_entrees(self):
        # Vérifier si les noms de tâches sont uniques
        noms_taches = []
        for tache in self.listeTaches:
            noms_taches.append(tache.name)
        noms_taches_set = set(noms_taches)

        if any(set(noms_taches).len(name) > 1 for name in noms_taches_set):
            raise ValueError("Les noms des tâches doivent être uniques")

        # Vérifier si les tâches citées dans le dictionnaire de précédence existent
        
        for tache, dependencies in self.precedences.items():
            if tache not in noms_taches:
                raise ValueError(f"La tâche '{tache}' dans le dictionnaire de précédence n'existe pas")
            for dep in dependencies:
                if dep not in noms_taches:
                    raise ValueError(f"La tâche '{dep}' citée dans les précédences de la tâche '{tache}' n'existe pas")
                

    def graphique(self):
        A = nx.DiGraph()
        for task in self.listeTaches:
            A.add_node(task.name)
            for dep in self.precedences[task.name]:
                A.add_edge(dep, task.name)
        position = nx.spring_layout(A)
        nx.draw(A, position, with_labels=True, node_size=1800, node_color="darkorange", font_size=10,font_weight="bold")
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

    def parCost(self, runs=25):
            seq_times = []
            par_times = []

            for _ in range(runs):
                start1 = time.time()
                self.runSeq()
                end1 = time.time()
                seq_times.append(end1 - start1)

                start2 = time.time()
                self.run()
                end2 = time.time()
                par_times.append(end2 - start2)

            seq_avg = sum(seq_times) / len(seq_times)
            temps1 = round(seq_avg, 3)
            par_avg = sum(par_times) / len(par_times)
            temps2 = round(par_avg, 3)

            print(f"Moyenne des temps d'exécution séquentielle: {temps1}")
            print(f"Moyenne des temps d'exécution parallèle: {temps2}")

    def parCost2(self, runs=25):
        seq_times = []
        par_times = []

        for _ in range(runs):
            start1 = time.time()
            self.runSeq()
            end1 = time.time()

            start2 = time.time()
            self.run()
            end2 = time.time()

            seq_times.append(end1 - start1)
            par_times.append(end2 - start2)

        avg_seq_time = sum(seq_times) / runs
        avg_par_time = sum(par_times) / runs

        print("Temps d'exécution moyen en séquentiel : {:.5f}".format(avg_seq_time))
        print("Temps d'exécution moyen en parallèle : {:.5f}".format(avg_par_time))
        print("Vitesse moyenne : {:.4f}".format(avg_seq_time / avg_par_time))


"""
X = None
Y = None
Z = None

def runT1():
    global X
    X = 1

def runT2():
    global Y
    Y = 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

t1 = Task("T1", reads=[], writes=["X"], run=runT1)
t2 = Task("T2", reads=["X"], writes=["Y"], run=runT2)
tSomme = Task("somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)


s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})

print("runSec est lancé : " )
s1.runSeq()
print(X)
print(Y)
print(Z)

print("runPar est lancé : ")
s1.run()
print(X)
print(Y)
print(Z)

s1.detTestRnd()
s1.parCost2() 
"""