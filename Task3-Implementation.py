import random
import copy
import json


# Funktion zur Initialisierung der ersten Generation
def initial_population():
    population = []
    for _ in range(pop_size):
        chromosome = []
        # bis es drei Standorte in der aktuellen Kombination gibt
        while len(chromosome) < 3:
            # zufaellige Position wird ermittelt
            random_position = random.randint(0, umfang-1)
            # wenn der Standort noch nicht in der Kombination enthalten ist -> hinzufuegen
            # es soll nicht mehrere Eisbuden an einem Standort geben
            if random_position not in chromosome:
                chromosome.append(random_position)
        chromosome.sort()
        population.append(chromosome)
    # erste Generation zurueckgeben
    return population


# gibt Distanz zwischen zwei Positionen auf dem Umfang des Kreises zurueck
def distance_between_two(pos1, pos2):
    return min([umfang - max([pos1, pos2]) + min([pos1, pos2]), max([pos1, pos2]) - min([pos1, pos2])])


# gibt die minimale Distanz aller Haeuser zu einer Kombination von Eisbudenstandorten zurueck
def distance_for_every_house(chromosome):
    if str(chromosome) not in saved_distances:
        distances = []
        for h in haeuser:
            # fuer jeden Eisbudenstandort wird die Distanz berechnet, niedrigste wird ausgewaehlt
            dist1 = distance_between_two(h, chromosome[0])
            dist2 = distance_between_two(h, chromosome[1])
            dist3 = distance_between_two(h, chromosome[2])
            distances.append(min([dist1, dist2, dist3]))
        # berechnete Distanzen speichern, sodass sie nicht immmer wieder neue berechnet werden muessen
        saved_distances[str(chromosome)] = distances.copy()
        return distances
    else:
        return saved_distances[str(chromosome)]


# vergleicht zwei Kombination und gibt zurueck, ob erste Kombination in einer Abstimmung verlieren wuerde oder nicht
def compare_two_chromosomes(c1, c2):
    distances_c1 = distance_for_every_house(c1)
    distances_c2 = distance_for_every_house(c2)

    # die Anzahl der Ja-Stimmen fuer eine Umverlegung wird nach den Regeln aus der Aufgabenstellung berechnet
    yes_votes = 0
    for i in range(len(distances_c1)):
        if distances_c1[i] > distances_c2[i]:
            yes_votes += 1

    # Wenn die Mehrheit Ja-Stimmen sind -> erste Komb. hat verloren
    if yes_votes > len(haeuser) / 2:
        return True
    return False


# Fitness-Funktion
def calculate_fitness(population):
    # setzt Grundfitness
    fitness = [len(population)-1]*len(population)
    # vergleicht jede Kombination mit allen anderen
    for i in range(len(population)):
        chromosome = population[i]
        for j in range(len(population)):
            if i != j:
                compare_chromosome = population[j]
                if compare_two_chromosomes(chromosome, compare_chromosome) or chromosome[0] == compare_chromosome[0]:
                    # verringert Fitness-Wert um 1, wenn die aktuelle Kombination nicht geschlagen wurde
                    fitness[j] -= 1
    # gibt Fitness aller Kombinationen zurueck
    return fitness


# ermittelt die Kombinationen aus der aktuellen Generation, die den besten Fitness-Wert haben
def get_best_chromosomes(population, fitness):
    best_chromosomes = []
    for i in range(len(population)):
        # Wenn die Fitness der minimalen Fitness entspricht -> eine der besten Kombinationen der akt. Gen.
        if fitness[i] == min(fitness):
            dist = distance_for_every_house(population[i])
            if [population[i], dist] not in best_chromosomes:
                best_chromosomes.append([population[i], dist])
    # gibt "beste" Kombinationen zurueck
    return best_chromosomes


# Selektions-Funktion, erhält alte Generation und ermittelt den "Pool" der naechsten Generation
def selection(population, fitness):
    population_with_probabilites = []
    for i in range(len(population)):
        # Fuegt die Kombinationen gemaess der berechneten Anzahl auf grundlage des Fitness-Wertes hinzu
        population_with_probabilites += [copy.deepcopy(population[i])] * (pop_size-1 - fitness[i])
    mating_pool = []
    # waehlt zufaellig Kombinationen aus
    for _ in range(pop_size):
        choice = random.choice(population_with_probabilites)
        mating_pool.append(choice)
    return mating_pool


# Rekombinations-Funktion
def crossover(mating_pool):
    # iteriert ueber alle Kombination der aktuellen Generation
    for i in range(len(mating_pool)):
        # zufaellige Zahl um zu bestimmen, ob rekombiniert werden soll oder nicht
        random_number = random.randint(0, 99)/100
        if random_number < crossover_rate:
            # Partner wird zufaellig ausgewaehlt
            mating_partner = random.choice(mating_pool)
            if mating_partner != mating_pool[i]:
                # es wird zufaellig ausgewaehlt, welcher Teil behalten werden soll und welcher nicht
                splitting_index = random.choice([1, 2])
                mating_pool[i] = mating_pool[i][:splitting_index] + mating_partner[splitting_index:]
    return mating_pool


# Mutations-Funktion
def mutation(mating_pool):
    # es wird fuer jeden Standort entschieden, ob er mutieren soll oder nicht
    for i in range(len(mating_pool)):
        for j in range(len(mating_pool[i])):
            # zufaellige Zahl um zu bestimmen, ob mutiert werden soll oder nicht
            random_number = random.randint(0, 99)/100
            if random_number < mutation_rate:
                # setze neuen, zufaelligen Standort
                mating_pool[i][j] = random.randint(0, umfang-1)
        mating_pool[i].sort()
    return mating_pool


# Terminationsbedingung
def termination(best_chromosomes, generation_counter):
    # ueber jede beste Kombination der aktuellen Generation wird iteriert
    for chromosome in best_chromosomes:
        # es wird gespeichert, dass diese Komb. zur besten Komb. gehoert
        if str(chromosome[0]) not in overall_best_chromosomes:
            overall_best_chromosomes[str(chromosome[0])] = 1
        else:
            overall_best_chromosomes[str(chromosome[0])] += 1
        if generation_counter > min_generation_count:
            # Wenn Terminationsbedingung eintrifft, wird beendet
            if overall_best_chromosomes[str(chromosome[0])] > generation_counter * termination_percentage:
                return True
    return False

# Main-Funktion, die sich rekursiv aufruft
def ga(population, generationen_counter):
    # Fitness-Werte werden berechnet
    fitness = calculate_fitness(population)
    # beste Kombinationen werden ermittelt
    best_chromosomes = sorted(get_best_chromosomes(population, fitness))
    # neuer "Pool" wird ausgewählt
    mating_pool = selection(population, fitness)
    # Rekombination wird angewandt
    mating_pool_after_crossover = crossover(copy.deepcopy(mating_pool))
    # Mutation wird angewandt
    mating_pool_after_mutation = mutation(copy.deepcopy(mating_pool_after_crossover))

    # Terminationsbedinung wird ueberprueft
    if not termination(best_chromosomes, generationen_counter):
        # Wiederaufruf der Funktion --> neue Generation
        ga(mating_pool_after_mutation, generationen_counter+1)
    else:
        return

# waehlt anhand der Kombinationen, die am haeufigsten als beste auftraten, das Ergebnis aus
def select_overall_winning_ones():
    # beste Kombinationen abrufen
    most_occurences = most_occurences_of_chromosomes()
    # Fitness-Werte berechnen
    fitness = calculate_fitness(most_occurences)
    # Wenn Fitness-Wert keiner Komb. 0 ist --> konnte kein stabiler Eisbudenstandort gefunden werden
    if min(fitness) > 0:
        print("Es konnte kein stabiler Standort gefunden werden")
    # gibt Komb. aus, die einen Fitness-Wert von 0 haben --> vermutlich stabile Standorte
    else:
        best_chromosomes = [x[0] for x in get_best_chromosomes(most_occurences, fitness)]
        print("Stabile Standorte sind vermutlich", best_chromosomes)


# sucht die Kombinationen, die am haeufigsten als "beste" Kombinationen vorkamen und gibt sie zurueck
def most_occurences_of_chromosomes():
    most_occurences = []
    for chromosome, occurences in overall_best_chromosomes.items():
        if len(most_occurences) < comparison_between_best:
            most_occurences.append([chromosome, occurences])
        else:
            for i in range(len(most_occurences)):
                if most_occurences[i][1] < occurences:
                    most_occurences[i] = [chromosome, occurences]
                    break

    for j in range(len(most_occurences)):
        most_occurences[j] = json.loads(most_occurences[j][0])
    return most_occurences


# Einlesen der Datei
path = "eisbuden1.txt"
file = open(path, "r")

first = [int(x) for x in file.readline().split(" ") if x != "\n"]
umfang = first[0]
anzahl_haeuser = first[1]
haeuser = [int(x) for x in file.readline().split(" ") if x != "\n"]
saved_distances = {}
overall_best_chromosomes = {}

# Variablen definiert
pop_size = 55
mutation_rate = 0.085
crossover_rate = 0.85
min_generation_count = 15
comparison_between_best = 20
termination_percentage = 0.06

# Aufrufen der Hauptfunktionen
ga(initial_population(), 0)
select_overall_winning_ones()
