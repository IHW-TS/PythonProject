
import fichier_bibli as bib
from fichier_bibli import Task
from fichier_bibli import TaskSystem

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