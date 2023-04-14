from interrupts import *
from threading import Semaphore
import threading


print(disk[0:10])

s = Semaphore(1)
buffer = [None] * 4

# Initialisation des pointeurs de lecture et d'écriture pour le buffer
read = 0
write = 0
s = threading.Semaphore(1)

def readBuffer():
    # Acquisition du sémaphore
    s.acquire()
    # Lecture de l'élément pointé par le pointeur de lecture
    data = buffer[read]
    # Mise à None de l'élément lu
    buffer[read] = None
    # Mise à jour du pointeur de lecture (modulo 4 pour faire une boucle)
    read = (read + 1) % 4
    # Relâchement du sémaphore
    s.release()
    return data

def writeBuffer(data):
    s.acquire()
    # Ecriture des données dans l'élément pointé par le pointeur d'écriture
    buffer[write] = data
    write = (write + 1) % 4
    s.release()

def handleWriteFinished(): 
    print("Fini d'ecrire !")
    s.release()

registerInterruptHandler(DISK_WRITE_FINISHED, handleWriteFinished)

def handleReadFinished(cell):
    print("Lu donnee %s !" % cell) 
    s.release()

registerInterruptHandler(DISK_READ_FINISHED, handleReadFinished)

s.acquire()
writeCell(disk, 0, 32)

print(disk[0])
# Pause d'une durée de 2 secondes
sleep(2) 

s.acquire()
readCell(disk, 0)

# Lancement d'un nouveau thread affichant un message
threading.Thread(target = lambda: print("Salut depuis un autre thread !")).start()
