import json
import numpy as np
from matplotlib import pyplot as plt


# Loading data
with open("population_data.json") as json_file:
    population_data = json.load(json_file)


# Assigning data
generation = [population_data["data"][data]["generation"] for data in range(len(population_data["data"]))]
population_size = [population_data["data"][data]["population"] for data in range(len(population_data["data"]))]
fittest = [population_data["data"][data]["fittest"] for data in range(len(population_data["data"]))]
unfittest = [population_data["data"][data]["unfittest"] for data in range(len(population_data["data"]))]


# Plotting data
plt.subplot(1, 2, 1)
plt.title("population size")
plt.plot(generation, population_size, color="r")

plt.subplot(1, 2, 2)
plt.title("fitness score")
plt.plot(generation, fittest, color="b")
plt.plot(generation, unfittest, color="r")
plt.legend(["fittest", "unfittest"])

plt.show()
