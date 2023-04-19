import threading
import networkx 
import time 
import random 
import matplotlib.pyplot as plt

#classe qui permet de definir des tâches
class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run


#classe qui va géré les dépendances et l'ordre d'exécution des tâches
class TaskSystem:
    def __init__(self, task, parent):
        self.task = task 
        self.parent = parent
        self.valide_task()
        #affiche graphiquement le graphe de précédence du système de parallélisme maximal construit
        self.graph = self.draw()

    def valide_task(self):
        #vérifie que les noms des tâches sont uniques
        task_names = [task.name for task in self.task]
        if len(task_names) != len(set(task_names)):
            raise ValueError("Les noms des tâches doivent être uniques")

        #vérifie la cohérence entre les noms des tâches dans la liste des tâches et ceux dans le graphe de précédence
        for task_name in self.parent.keys():
            if task_name not in task_names:
                raise ValueError(f"Le nom de tâche {task_name} dans le dictionnaire de précédence n'est pas dans la liste des tâches")

        for dependencies in self.parent.values():
            for dep in dependencies:
                if dep not in task_names:
                    raise ValueError(f"La dépendance {dep} n'est pas une tâche valide")

    #renvoie sous forme de liste le nom des tâches qui doivent s’exécuter avant la tâche "task_name"
    def getDependies(self, task_name):
        return self.parent.get(task_name, [])

    #exécute les tâches de façon séquentielle en respectant l’ordre imposé par la relation de précédence
    def runSeq(self):
        #effectue un tri topologique sur le graphe pour obtenir l'ordre d'exécution des tâches
        task_ord = list(networkx.topological_sort(self.graph))
        #parcour les tâches dans l'ordre obtenu
        for task_name in task_ord:
            #trouve l'instance de la tâche correspondante à partir de son nom et l'exécute 
            task = next(t for t in self.task if t.name == task_name)
            task.run()

    #exécute les tâches selon la spécification du parallélisme maximal
    def run(self):
        task_ord = list(networkx.topological_sort(self.graph))
        #crée une liste vide pour stocker les threads qui seront créés
        threads = []

        #parcour les tâches dans l'ordre obtenu
        for task_name in task_ord:
            #trouve l'instance de la tâche correspondante à partir de son nom
            task = next(t for t in self.task if t.name == task_name)
            #crée un nouveau thread pour exécuter la fonction "run" de la tâche
            thread = threading.Thread(target = task.run)
            thread.start()
            #ajoute le thread à la liste des threads
            threads.append(thread)

        #attend que tous les threads aient terminé
        for thread in threads:
            thread.join()
       
    #affiche graphiquement le grahe de précédence en utilisant la bilbiothèque "networkx"
    def draw(self):
        #crée un graphe dirigé vide
        graph = networkx.DiGraph()
    
        for task in self.task:
            #ajoute un noeud au graphe pour chaque tâche en utilisant son nom
            graph.add_node(task.name)
            #parcourir les dépendances de la tâche actuelle
            for dep in self.parent[task.name]:
                #ajoute un arc dirigé entre chaque dépendance et la tâche actuelle
                graph.add_edge(dep, task.name)

        pos = networkx.spring_layout(graph)
        networkx.draw(graph, pos, with_labels=True, node_size=2000, node_color="green", font_size=10, font_weight="bold")
        plt.show()

        #renvoie le graphe construit
        return graph

    #teste le déterminsime du système en effectuant avec des valeurs aléatoires, différentes exécutions parrallèles du système 
    def detTestRnd(self, test = 100):
        for _ in range(test):
            #génére des valeurs aléatoires pour les variables X, Y et Z
            self.X = random.randint(1, 100)
            self.Y = random.randint(1, 100)
            self.Z = random.randint(1, 100)

            #exécute les tâches en parallèle avec le premier jeu de valeurs
            self.run()
            resultat1 = (self.X, self.Y, self.Z)

            #réinitialise les variables avec les mêmes valeurs aléatoires
            self.X = random.randint(1, 100)
            self.Y = random.randint(1, 100)
            self.Z = random.randint(1, 100)

            #exécute les tâches en parallèle avec le second jeu de valeurs
            self.run()
            resultat2 = (self.X, self.Y, self.Z)

            #compare les résultats des deux exécutions parallèles
            if resultat1 != resultat2:
                print("Le système n'est pas déterministe")
                return
        print(f"Après {test} tests, on peut conclure que le système est déterministe")

    #compare les temps d'exécutions séquentielle et parrallèle du système de tâche
    def parCost(self):
        runs = 100
        seq_time = []
        par_time = []

        for _ in range(runs):
            start_time = time.perf_counter()
            self.runSeq()
            end_time = time.perf_counter()
            seq_time.append(end_time - start_time)

            start_time = time.perf_counter()
            self.run()
            end_time = time.perf_counter()
            par_time.append(end_time - start_time)

        avg_seq_time = sum(seq_time) / runs
        avg_par_time = sum(par_time) / runs

        print(f"Temps d'exécution moyen en séquentiel : {avg_seq_time:.4f} s")
        print(f"Temps d'exécution moyen en parallèle : {avg_par_time:.4f} s")