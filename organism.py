import random
from random import choices


# Organism class
class Organism:
    def __init__(self, chromosome):
        self.chromosome = chromosome # Chromosome
    
    
    # Mutate the gene
    def mutateGenes(self):
        random_gene = random.choice(range(len(self.chromosome)))
        self.chromosome[random_gene] = 1 if self.chromosome[random_gene] == 0 else 0


    # Crosses the organisms genes with its pairs
    def crossoverWith(self, pair):
        chromosome_half = len(self.chromosome)//2

        # Combining the halves
        half1 = self.chromosome[:chromosome_half]
        half2 = pair.chromosome[chromosome_half:]

        return Organism(half1 + half2)

    
    # Calculate its fitness 
    def calculateFitness(self):
        fitness = 0
        for gene in self.chromosome:
            if gene == 1:
                fitness += 1
        return fitness
