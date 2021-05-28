from population import Population
import random
from random import choices, randint
import json


def main():

    # For data visualization purposes
    # Clears the json file
    # Loads data
    with open("population_data.json") as json_file:
        population_data = json.load(json_file)

    # Writes modified data
    with open("population_data.json", "w") as json_file:
        population_data["data"].clear()
        json.dump(population_data, json_file, indent=2)


    initial_population_size = random.randint(50, 1001)
    target = random.randint(10, 50)

    population = Population(initial_population_size, target)
    population.establishPopulation()
    population.runPopulation()

if __name__ == "__main__":
    main()
