import threading
import random
import time
import matplotlib.pyplot as plt
import networkx as nx

class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run = run

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        self.X = None
        self.Y = None
        self.Z = None
        self.validate_inputs()
        self.graph = self.build_graph()

    def validate_inputs(self):
        task_names = [task.name for task in self.tasks]
        if len(task_names) != len(set(task_names)):
            raise ValueError("Les noms des tâches doivent être uniques")

        for task_name in self.precedence.keys():
            if task_name not in task_names:
                raise ValueError(f"Le nom de tâche {task_name} dans le dictionnaire de précédence n'est pas dans la liste des tâches")

        for dependencies in self.precedence.values():
            for dep in dependencies:
                if dep not in task_names:
                    raise ValueError(f"La dépendance {dep} n'est pas une tâche valide")

    def build_graph(self):
        G = nx.DiGraph()
        for task in self.tasks:
            G.add_node(task.name)
            for dep in self.precedence[task.name]:
                G.add_edge(dep, task.name)
        return G

    def getDependencies(self, task_name):
        return self.precedence.get(task_name, [])

    def runSeq(self):
        ordered_tasks = list(nx.topological_sort(self.graph))
        for task_name in ordered_tasks:
            task = next(t for t in self.tasks if t.name == task_name)
            task.run()

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

    def draw(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
        plt.show()

    def detTestRnd(self):
        num_tests = 100
        for _ in range(num_tests):
            self.run()
            result1 = (self.X, self.Y, self.Z)

            self.run()
            result2 = (self.X, self.Y, self.Z)

            if result1 != result2:
                print("Le système n'est pas déterministe")
                return
        print("Aucune indétermination détectée après", num_tests, "tests")

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


def runT1(self):
    self.X = 1

def runT2(self):
    self.Y = 2

def runTsomme(self):
    self.Z = self.X + self.Y