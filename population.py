import random
from organism import Organism
import random
from random import choices
import math
import json


# Population class
class Population:
    def __init__(self, population_number, target):
        self.initial_population_number = population_number
        self.prev_population_number = None
        self.target = target
        self.fittest_score = self.target


    # Establish population    
    def establishPopulation(self):
        self.population = []

        # Fill the population with organisms that has random genes
        for _ in range(self.initial_population_number):
            organism = Organism([random.choice([1, 0]) for gene in range(self.target)])
            self.population.append(organism)


    # Cross genes
    def crossGenes(self):

        selection_pool = [] # Pool for crossover

        # Adding the organism in the selection pool N times. N is the fitness score of the organism
        for organism in self.population:
            for _ in range(organism.calculateFitness()):
                selection_pool.append(organism)

        # Make A pairs of parents selected from the selection pool
        for _ in range(len(self.population)//3):

            # Select random parents
            parent1 = random.choice(selection_pool)
            parent2 = random.choice(selection_pool)
            while parent2 == parent1:
                parent2 = random.choice(selection_pool)
            
            # Offsprings from the 2 parents
            offspring1 = parent1.crossoverWith(parent2)
            offspring2 = parent2.crossoverWith(parent1)

            offspring1.mutateGenes() # Mutate its genes
            offspring2.mutateGenes()

            self.population.append(offspring1) # Add to the population
            self.population.append(offspring2)
        
        selection_pool.clear() # Clears the pool


    def getExtinctionPool(self):
        # Setting up the extinction pool
        extinction_pool = []
        for organism in self.population:
            insert_n_times = math.ceil((self.target * 10) / organism.calculateFitness())

            for n in range(insert_n_times):
                extinction_pool.append(organism)
        
        return extinction_pool


    # Eliminates organisms with the 1st and 2nd lowest fitness scores
    def eliminateOrganisms(self):

        extinction_pool = self.getExtinctionPool()

        # The population has a 50% chance of having 10% of their population eliminated
        # and 20% for the rest of the 50% percent
        percentage = 20 if random.choice(range(1)) == 0 else 10

        # Eliminates the organisms
        random_organism_death_count = math.ceil(len(self.population) * (percentage/100))
        for i in range(random_organism_death_count):
            if len(self.population) == 0:
                break
            
            organism = random.choice(extinction_pool)

            self.population.remove(organism)

            # Removes organism from the extinction pool
            while organism in extinction_pool:
                extinction_pool.remove(organism)


    # Extinction waves to cut the population by 99%
    def executeMassExtinction(self, extinction_wave):

        print(f"[wave: {extinction_wave+1}]")

        # Eliminates 99% of the whole population
        random_organism_death_count = math.ceil(99/100 * len(self.population))

        # Gets me the extinction pool
        extinction_pool = self.getExtinctionPool()

        # Picking organisms from the extinction pool
        for i in range(random_organism_death_count):
            organism = random.choice(extinction_pool)

            self.population.remove(organism) # Removes organism from the population

            # Removes organism from the extinction pool
            while organism in extinction_pool:
                extinction_pool.remove(organism)


    # Background extinction to stabilize the population
    def executeBackgroundExtinction(self):

        # Eliminates 55% of the whole population
        random_organism_death_count = math.ceil(55/100 * len(self.population))

        # Gets me the extinction pool
        extinction_pool = self.getExtinctionPool()

        # Picking organisms from the extinction pool
        for i in range(random_organism_death_count):
            organism = random.choice(extinction_pool)

            self.population.remove(organism) # Removes organism from the population

            # Removes organism from the extinction pool
            while organism in extinction_pool:
                extinction_pool.remove(organism)


    # Get the fitness scores
    def getFitnessScores(self):
        fitness_scores = set()
        for organism in self.population:
            fitness_scores.add(organism.calculateFitness())
        
        fitness_scores = list(fitness_scores)

        return fitness_scores


    # Gets the fittest organism
    def fittestOrganism(self):
        for organism in self.population:
            if organism.calculateFitness() == self.fittest_score:
                return organism


    # Gets the info about the populations growth
    def populationGrowth(self):
        if self.prev_population_number == None or self.prev_population_number == len(self.population):
            return " "
        if self.prev_population_number < len(self.population):
            return "+"
        elif self.prev_population_number > len(self.population):
            return "-"


    # Run the population
    def runPopulation(self):

        generation = 1
        extinction_wave = 0

        print(f"[generation: {generation}|{extinction_wave}] [{self.populationGrowth()}|population: {len(self.population)}({max(self.getFitnessScores())}-{min(self.getFitnessScores())})|{self.target}]")

        is_alive = True
        while is_alive:


            self.prev_population_number = len(self.population)
            generation += 1

            self.crossGenes() # Cross genes
            self.eliminateOrganisms() # Eliminate organisms
            
            # Cut the population each 25 generations
            if generation % 25 == 0:
                self.executeMassExtinction(extinction_wave)
                extinction_wave += 1
            # Cut the population down by 55% each 10 generations
            elif generation % 10 == 0:
                self.executeBackgroundExtinction()

            try:
                print(f"[generation: {generation}|{extinction_wave}] [{self.populationGrowth()}|population: {len(self.population)}({max(self.getFitnessScores())}-{min(self.getFitnessScores())})|{self.target}]")
            except:
                print(f"[generation: {generation}|{extinction_wave}] [{self.populationGrowth()}|population: {len(self.population)}(_-_)|{self.target}]")


            if len(self.population) in range(2):
                print("\npopulation extinct")
                if self.prev_population_number > 10 * len(self.population) and len(self.population) != 0:
                    most_likely_cause = "extinction wave"
                else:
                    most_likely_cause = "insufficient breeding rate"

                print(f"most likely cause: {most_likely_cause}")
                break


            # For data visualization purposes
            # Loads data
            with open("population_data.json") as json_file:
                population_data = json.load(json_file)

            # Writes modified data
            with open("population_data.json", "w") as json_file:
                population_data["data"].append({
                    "generation": generation,
                    "population": len(self.population),
                    "fittest": max(self.getFitnessScores()),
                    "unfittest": min(self.getFitnessScores())
                })
                json.dump(population_data, json_file, indent=2)


            # Checks if the target has been achieved
            if max(self.getFitnessScores()) == self.fittest_score:
                print("\nobjective achieved")
                print(f"\ngeneration: {generation}")
                print(f"initial population size: {self.initial_population_number}")
                print(f"organism: {self.fittestOrganism()}")
                print(f"fitness score: {self.fittest_score}")

                is_alive = False
