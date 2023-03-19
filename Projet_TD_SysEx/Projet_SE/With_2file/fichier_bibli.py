
import networkx as nx 
import matplotlib.pyplot as plt 
import time
import random 

class Task:
    def __init__(self):  
        self.name = ""
        self.reads = []
        self.writes = []
        self.run = None

class TaskSystem:  
    def __init__(self, tasks, precedence):  
        task_names = [task.name for task in tasks]
        for task_name in task_names: 
            if task_names.count(task_name) > 1: 
                raise ValueError("Task dupliquée : " + task_name)
        for task_name, dependencies in precedence.items(): 
            if task_name not in task_names: 
                raise ValueError("La Task " + task_name + " n'existe pas dans la liste des tâches")
            for dependency in dependencies: 
                if dependency not in task_names:
                    raise ValueError("La Task " + dependency + " n'existe pas dans la liste des tâches")

        self.tasks = tasks
        self.precedence = precedence

    def draw(self):
        G = nx.DiGraph()
        for task in self.tasks:
            G.add_node(task.name) 
        for task_name, dependencies in self.precedence.items(): 
            for dependency in dependencies:
                G.add_edge(dependency, task_name)
        nx.draw(G, with_labels=True) 
        plt.show() 

    def getDependencies(self, task_name):
        return self.precedence[task_name]

    def run(self):
        parallel_tasks = set()
        for task in self.tasks:  
            run_task = True
            for dependency in self.getDependencies(task.name):
                if dependency not in [t.name for t in parallel_tasks]:
                    run_task = False
                    break
            if run_task:  
                parallel_tasks.add(task)

        for task in parallel_tasks:
            task.run()

    def runSeq(self):
        for task_name in sorted(self.precedence.keys()):
            task = next(task for task in self.tasks if task.name == task_name)
            task.run()
            
    # def detTestRnd(self, num_tests):
    #     for i in range(num_tests):
    #         for task in self.tasks:
    #             for read_var in task.reads:
    #                 exec(f"{read_var} = random.randint(0, 100)")
    #         self.run()
    #         result = [eval(var) for var in set(sum([task.reads + task.writes for task in self.tasks], []))]
    #         if i == 0:
    #             results = [result]
    #         else:
    #             if result != results[0]:
    #                 return False
    #     print(results[0])
    #     return True

    def parCost(self, num_tests):
        total_parallel_time = 0
        total_sequential_time = 0
        for i in range(num_tests):
            start_time = time.time()
            self.run()
            end_time = time.time()
            total_parallel_time += end_time - start_time
            start_time = time.time()
            self.runSeq()
            end_time = time.time()
            total_sequential_time += end_time - start_time
        average_parallel_time = total_parallel_time / num_tests
        average_sequential_time = total_sequential_time / num_tests
        print(f"Temps moyen d'exécution parallèle: {average_parallel_time} secondes")
        print(f"Temps moyen d'exécution séquentiel: {average_sequential_time} secondes")