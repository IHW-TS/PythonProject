import numpy as np  # Importe la bibliothèque NumPy pour les opérations mathématiques avancées
import matplotlib.pyplot as plt  # Importe Pyplot de Matplotlib pour la visualisation graphique
import random  # Importe le module random pour générer des nombres aléatoires
import pandas as pd  # Importe la bibliothèque Pandas pour la manipulation de données

# Définit une classe nommée City
class City:
    def __init__(self, x, y):  # Constructeur de la classe avec deux paramètres : x et y
        self.x = x  # Attribut pour stocker la coordonnée x de la ville
        self.y = y  # Attribut pour stocker la coordonnée y de la ville

    def distance(self, city):  # Méthode pour calculer la distance entre deux villes
        # Utilise np.hypot pour calculer l'hypoténuse (distance euclidienne) entre deux points
        return np.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):  # Méthode spéciale pour définir la représentation d'objet de la classe
        # Renvoie une chaîne de caractères qui représente la ville sous forme de coordonnées (x, y)
        return f"({self.x},{self.y})"

# Fonction pour calculer la distance totale d'un itinéraire
def total_distance(route):
    # Calcule la somme des distances entre toutes les villes consécutives dans l'itinéraire,
    # en utilisant la méthode distance de la classe City
    # Utilise une compréhension de liste pour créer une liste des distances, qui est ensuite sommée
    return sum([route[i].distance(route[(i + 1) % len(route)]) for i in range(len(route))])

# Fonction pour créer un individu (itinéraire) aléatoire
def create_individual(cities):
    # Retourne une liste aléatoire des villes, ce qui représente un itinéraire unique
    return random.sample(cities, len(cities))

# Fonction pour créer une population d'individus
def create_population(city_list, population_size):
    # Génère une population de taille population_size, en créant chaque individu avec la fonction create_individual
    return [create_individual(city_list) for _ in range(population_size)]

# Fonction pour classer la population par itinéraire
def rank_population(population):
    # Crée une liste des itinéraires avec leur index et distance totale,
    # puis trie cette liste en fonction de la distance (du plus court au plus long)
    distances = [(i, total_distance(individual)) for i, individual in enumerate(population)]
    return sorted(distances, key=lambda x: x[1])

# Fonction de sélection pour l'algorithme génétique
def selection(ranked_population, elite_size):
    # Sélectionne les meilleurs itinéraires en fonction de la valeur d'élite
    selection_results = [ranked_population[i][0] for i in range(elite_size)]
    # Ajoute des individus supplémentaires à la sélection de manière aléatoire, hors de l'élite
    for _ in range(len(ranked_population) - elite_size):
        selection_results.append(ranked_population[random.randint(0, len(ranked_population) - 1)][0])
    return selection_results

# Fonction pour créer un pool d'accouplement à partir des indices sélectionnés
def mating_pool(population, selected_indices):
    # Sélectionne les individus de la population actuelle basée sur les indices sélectionnés pour le pool d'accouplement
    return [population[i] for i in selected_indices]

# Fonction pour effectuer le croisement (ou recombinaison) entre deux parents
def crossover(parent1, parent2):
    child = []  # Liste pour stocker l'enfant résultant
    gene_a = int(random.random() * len(parent1))  # Sélectionne un point de croisement aléatoire A
    gene_b = int(random.random() * len(parent1))  # Sélectionne un point de croisement aléatoire B

    start_gene = min(gene_a, gene_b)  # Le début du segment pour le croisement
    end_gene = max(gene_a, gene_b)  # La fin du segment pour le croisement

    # Ajoute les gènes du premier parent à l'enfant dans la plage définie entre start_gene et end_gene
    for i in range(start_gene, end_gene):
        child.append(parent1[i])

    # Ajoute les gènes du second parent à l'enfant si les gènes ne sont pas déjà présents,
    # pour compléter l'itinéraire sans dupliquer de villes
    child += [item for item in parent2 if item not in child]

    # Renvoie l'enfant qui est une combinaison des gènes des deux parents
    return child

# Fonction pour muter un individu (itinéraire)
def mutate(individual, mutation_rate):
    # Itère sur chaque ville dans l'itinéraire
    for swapped in range(len(individual)):
        # Vérifie si une mutation doit se produire, basé sur le taux de mutation
        if random.random() < mutation_rate:
            # Sélectionne une deuxième ville aléatoire dans l'itinéraire pour l'échange
            swap_with = int(random.random() * len(individual))
            
            # Échange les deux villes
            city1 = individual[swapped]
            city2 = individual[swap_with]
            individual[swapped] = city2
            individual[swap_with] = city1
    return individual  # Retourne l'itinéraire muté

# Fonction pour créer la prochaine génération
def next_generation(current_gen, elite_size, mutation_rate):
    ranked_pop = rank_population(current_gen)  # Classe la génération actuelle
    selection_results = selection(ranked_pop, elite_size)  # Sélectionne les meilleurs itinéraires
    matingpool = mating_pool(current_gen, selection_results)  # Crée un pool d'accouplement
    # Effectue le croisement sur le pool d'accouplement pour créer des enfants
    children = [crossover(matingpool[i], matingpool[len(matingpool) - i - 1]) for i in range(len(matingpool))]
    # Applique la mutation sur les enfants pour créer la nouvelle génération
    next_gen = [mutate(individual, mutation_rate) for individual in children]
    return next_gen  # Retourne la nouvelle génération

# Fonction principale de l'algorithme génétique
def genetic_algorithm(cities, pop_size, elite_size, mutation_rate, generations):
    pop = create_population(cities, pop_size)  # Crée une population initiale
    # Affiche la distance de l'itinéraire le plus court dans la population initiale
    print("Initial distance: " + str(1 / rank_population(pop)[0][1]))
    
    for i in range(generations):  # Boucle sur le nombre de générations
        pop = next_generation(pop, elite_size, mutation_rate)  # Crée une nouvelle génération
    
    # Affiche la distance de l'itinéraire le plus court dans la dernière génération
    print("Final distance: " + str(1 / rank_population(pop)[0][1]))
    # Récupère le meilleur itinéraire de la dernière génération
    best_route_index = rank_population(pop)[0][0]
    best_route = pop[best_route_index]
    return best_route  # Retourne le meilleur itinéraire

# Définit une graine aléatoire pour la reproductibilité des résultats
random.seed(42)
# Crée une liste aléatoire de villes avec des coordonnées x et y comprises entre 0 et 200
city_list = [City(x=int(random.random() * 200), y=int(random.random() * 200)) for _ in range(num_cities)]

# Exécute l'algorithme génétique et récupère le meilleur itinéraire
best_route = genetic_algorithm(city_list, population_size, elite_size, mutation_rate, num_generations)

# Fonction pour tracer le meilleur itinéraire trouvé
def plot_route(route):
    plt.figure(figsize=(10,5))  # Définit la taille de la figure
    # Récupère les coordonnées x et y des villes dans l'itinéraire
    x = [city.x for city in route]
    y = [city.y for city in route]
    # Trace l'itinéraire sur le graphique
    plt.plot(x, y, 'mo-', label='Path')
    # Trace une ligne entre le dernier et le premier point pour fermer la boucle
    plt.plot([x[0], x[-1]], [y[0], y[-1]], 'mo-')
    # Met en évidence le point de départ/fin
    plt.scatter(x[0], y[0], c='red', marker='*', s=150, label='Start/End')
    plt.title('Best Route')  # Ajoute un titre à la figure
    plt.xlabel('X Coordinate')  # Ajoute une étiquette à l'axe des abscisses
    plt.ylabel('Y Coordinate')  # Ajoute une étiquette à l'axe des ordonnées
    plt.legend()  # Affiche la légende
  
    plt.show()

plot_route(best_route)
