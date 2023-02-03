import networkx as nx 
import matplotlib.pyplot as plt 

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

X = 0
Y = 0
Z = 0

def runT1():
    global X
    X = X + 1

def runT2():
    global Y
    Y = Y + 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

t1 = Task()
t1.name = "T1"
t1.writes = ["X"]
t1.run = runT1

t2 = Task()
t2.name = "T2"
t2.writes = ["Y"]
t2.run = runT2

tSomme = Task()
tSomme.name = "somme"
tSomme.reads = ["X", "Y"]
tSomme.writes = ["Z"]
tSomme.run = runTsomme

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]}) 
s1.run()
s1.draw() 

print(X)
print(Y)
print(Z)
