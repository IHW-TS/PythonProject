
# Projet en Python 
Plusieurs projets universitaire mettant en pratique la stratégie de recherche _A*_ pour
résoudre des taquins.
Développé en Python 3.6.0

## Projet en IA

#### Projet d'échauffement "Missionnaire et Cannibale" 

- Ennoncé du Sujet
- Rechercher en profondeur => Problème : Affiche le premier chemin trouvé et non le plus court, le reste est correct. 
- Compte rendu en LateX + étude expérimentale pas assez approfondie ( pas eu le temps), je recommande de faire un graphique et avec au moins 100 exécutions avec des valeurs différentes pour comparer le temps d'exécution du programme CPU etc... 
- 25% de la Note Finale

#### Projet "Taquin"

- Ennoncé du Sujet
- Tout est correct manque l'ajout d'une fonction de vérification pour l'état initial du Taquin
- Ne fonctionne pas pour les tailles supérieures à 3x3
- Interface Graphique : Version Web => Amélioration de la présentation niveau disposition est affichage (HTML & CSS), La conversion du fichier taquin.py en JS est correcte.
- Diaporama et Compte rendu en LateX (bientôt)
- 50% de la Note Finale

## Projet en SE

#### Projet "Implémentation d'un système de gestion de tâches parallélisées"

- Ennoncé du Sujet
- Réalisation d'un programme en python => Implémenté un système de gestion de tâches parallélisées qui optimise les performances en exploitant les ressources de calcul disponibles.  
- Réalisation d'une structure de base pour mieux comprendre l'intérêt du projet => Très utile si vous ne comprenez rien au projet 
- On peut remarquer 2 versions du programme : 
```python
- Projet_SE_V1 : Fonctionne dans l'ensemble mais contient quelque bug.
                 Fonction Test randomisé de déterminisme n'a pas été réalisé. 
                 Il existe aussi un version avec deux fichiers qui imposé par le sujet.
- Projet_SE_V2 : Tout fonction correctement 
```
- 50% de la note final voir plus 

- Diaporama (bientôt)

# Installation
### Windows
- Télécharger les dossiers pour les différents 
- Si besoin, installer la dernière version de Python 3 sur 
[le site officiel](https://www.python.org/downloads/windows/)
- Lancer l'interpréteur : `Démarrer > Programmes > Python 3.6 > IDLE Python GUI`
- Indiquer à Python dans quel répertoire se trouve les fichiers :
```python
>>> import sys
>>> sys.path.append('C:\Users\utilisateur\Documents\dossierContenanttaquinpy') #exemple
```

### Linux
- Idem
- Ouvrir un terminal, aller dans le répertoire contenant `taquin.py` et lancer
la commande `python`

