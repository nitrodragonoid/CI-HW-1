import random
import math

class EA:
    def __init__(self, size = 1, scheme = 1, generations = 10 , data = {1:(1,1)}):
        self.data = data
        self.cities = []
        self.size = size
        self.scheme = scheme
        self.population = {}
        self.generation = generations

    def get_data(self, file):
        data = {}
        cities = []
        f = open(file, "r")
        l = 1
        for x in f:
            if x == "EOF":
                break
            if l > 7:
                info = x.split(" ")
                data[int(info[0])] = (float(info[1]),float(info[2]))
                cities.append(int(info[0]))
            l+=1
        self.cities = cities
        self.data = data
        return self.data
    
    def compute_fitness(self,ind):
        total = 0 
        for i in range(len(ind)-1):
            d = math.sqrt((self.data[ind[i-1]][0] - self.data[ind[i]][0])**2 + (self.data[ind[i-1]][1] - self.data[ind[i]][1])**2)
            total += d
        d = math.sqrt((self.data[ind[0]][0] - self.data[ind[len(ind)-1]][0])**2 + (self.data[ind[0]][1] - self.data[ind[len(ind)-1]][1])**2)
        total += d
        return total
    
    def initialize_population(self):
        arr = self.cities.copy()
        for i in range(self.size):
            ind = arr.copy()
            random.shuffle(ind)
            self.population[ind] = self.compute_fitness(ind)
        return self.population
        
    
        
        

evol = EA(size = 5)
evol.get_data("qa194.tsp")
# print(evol.data)
evol.initialize_population()
# for i in evol.population:
#     print(i)
# print(evol.population)
