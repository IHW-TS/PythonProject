import threading
import random
import time
import matplotlib.pyplot as plt
import networkx as nx

# La classe Task représente une tâche avec un nom, les ressources qu'elle lit et écrit, et une fonction pour exécuter la tâche
class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

# La classe TaskSystem représente un ensemble de tâches avec un graphe de précédence
class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        self.X = None
        self.Y = None
        self.Z = None
        self.validate_inputs()
        self.graph = self.build_graph()

    # Cette fonction valide les entrées fournies lors de la création d'un objet TaskSystem
    def validate_inputs(self):
        # Vérification des noms de tâches uniques
        task_names = [task.name for task in self.tasks]
        if len(task_names) != len(set(task_names)):
            raise ValueError("Les noms des tâches doivent être uniques")

        # Vérification de la cohérence des noms de tâches dans le graphe de précédence
        for task_name in self.precedence.keys():
            if task_name not in task_names:
                raise ValueError(f"Le nom de tâche {task_name} dans le dictionnaire de précédence n'est pas dans la liste des tâches")

        for dependencies in self.precedence.values():
            for dep in dependencies:
                if dep not in task_names:
                    raise ValueError(f"La dépendance {dep} n'est pas une tâche valide")

    # Cette fonction construit le graphe de précédence à partir des informations fournies
    def build_graph(self):
        G = nx.DiGraph()
        for task in self.tasks:
            G.add_node(task.name)
            for dep in self.precedence[task.name]:
                G.add_edge(dep, task.name)
        return G

    # Cette fonction retourne les dépendances d'une tâche spécifique
    def getDependencies(self, task_name):
        return self.precedence.get(task_name, [])

    # Cette fonction exécute les tâches de manière séquentielle en respectant l'ordre topologique
    def runSeq(self):
        ordered_tasks = list(nx.topological_sort(self.graph))
        for task_name in ordered_tasks:
            task = next(t for t in self.tasks if t.name == task_name)
            task.run()

    # Cette fonction exécute les tâches en parallèle en utilisant des threads
    def run(self):
        ordered_tasks = list(nx.topological_sort(self.graph))
        threads = []
        for task_name in ordered_tasks:
            task = next(t for t in self.tasks if t.name == task_name)
            thread = threading.Thread(target=task.run)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    # Cette fonction affiche le graphe de précédence en utilisant networkx et matplotlib
    def draw(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
        plt.show()

    # Cette fonction teste le déterminisme du système en exécutant plusieurs fois les tâches
    def detTestRnd(self, num_tests=100):
        for _ in range(num_tests):
            # Générer des valeurs aléatoires pour les variables X, Y et Z
            self.X = random.randint(1, 100)
            self.Y = random.randint(1, 100)
            self.Z = random.randint(1, 100)

            # Exécuter les tâches en parallèle avec le premier jeu de valeurs
            self.run()
            result1 = (self.X, self.Y, self.Z)

            # Réinitialiser les variables avec les mêmes valeurs aléatoires
            self.X = random.randint(1, 100)
            self.Y = random.randint(1, 100)
            self.Z = random.randint(1, 100)

            # Exécuter les tâches en parallèle avec le second jeu de valeurs
            self.run()
            result2 = (self.X, self.Y, self.Z)

            # Comparer les résultats des deux exécutions parallèles
            if result1 != result2:
                print("Le système n'est pas déterministe")
                return
        print(f"Aucune indétermination détectée après {num_tests} tests")




    # Cette fonction compare les temps d'exécution en séquentiel et en parallèle
    def parCost(self):
        num_runs = 10
        seq_times = []
        par_times = []

        for _ in range(num_runs):
            start_time = time.perf_counter()
            self.runSeq()
            end_time = time.perf_counter()
            seq_times.append(end_time - start_time)

            start_time = time.perf_counter()
            self.run()
            end_time = time.perf_counter()
            par_times.append(end_time - start_time)

        avg_seq_time = sum(seq_times) / num_runs
        avg_par_time = sum(par_times) / num_runs

        print(f"Temps d'exécution moyen en séquentiel : {avg_seq_time:.4f} s")
        print(f"Temps d'exécution moyen en parallèle : {avg_par_time:.4f} s")

# Fonctions de tâche en dehors de la classe TaskSystem

def runT1(self):
    self.X = 1

def runT2(self):
    self.Y = 2

def runTsomme(self):
    self.Z = self.X + self.Y