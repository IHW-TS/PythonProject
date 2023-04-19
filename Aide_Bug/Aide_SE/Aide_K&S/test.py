from bibliotheque import *

X = None
Y = None
Z = None

def runT1():
    global X
    X = 1
    print("T1 est lancée")

def runT2():
    global Y
    Y = 2
    print("T2 est lancée")
    
def runTsomme():
    global X, Y, Z
    Z = X + Y
    print("runTsomme est lancée")
    


t1 = Task("T1", reads=[], writes=["X"], run=runT1)
t2 = Task("T2", reads=["X"], writes=["Y"], run=runT2)
tSomme = Task("somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": ["T1"], "somme": ["T1", "T2"]})

s1.runSeq()

s1.run()

s1.draw()

s1.parCost()

s1.detTestRnd()

print(X)
print(Y)
print(Z)