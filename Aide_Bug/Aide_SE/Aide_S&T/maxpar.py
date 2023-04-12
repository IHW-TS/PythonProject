from maxp import *

X = None
Y = None
Z = None

def runT1():
    global X
    X = 1
    print("T1 lancée")
def runT2():
    global Y
    Y = 2
    print("T2 lancée")
def runTsomme():
    global X, Y, Z
    Z = X + Y
    print("runTsomme lancée")
    
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
#s1 = TaskSystem([t1, t2, tSomme], {  "T2": ["T1"], "T1": [], "somme": ["T1", "T2"]})

import time

# Comparaison du temps d'exécution de runSec
start_time_runSec = time.time()
s1.runSec()
print("Temps exé runSec: %s s" % (time.time() - start_time_runSec))


# Comparaison du temps d'exécution de run
start_time_run = time.time()
s1.run()
print("Temps exéde run: %s s" % (time.time() - start_time_run))

print(X)
print(Y)
print(Z)