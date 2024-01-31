import random
import math

class EA:
    def __init__(self, size = 30, generations = 50 , offsprings =  10, rate = 0.5, iteration = 10,  scheme = 1, data = {1:(1,1)}):
        self.data = data
        self.cities = []
        self.size = size
        self.scheme = scheme
        self.population = {}
        self.generation = generations
        self.offsprings = offsprings
        self.mutation_rate = rate
        self.iterations = iteration

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
        
    def crossover(self, parent_1, parent_2):
        ind = []
        start = math.random.randint(0, (len(parent_1)//2)-1)
        
        for i in range(len(parent_1)//2):
            ind.append(parent_1[i+start])
            
        for j in range(len(parent_2)):
            if parent_2[j] not in ind:
                ind.append(parent_2[j])
        
        return ind
    
    # selection schemes
    def fitness_proportional(self):
        sum = 0
        for ind in self.population:
            sum += 1/self.population[ind]
        wheel = {}
        current = 0
        for i in self.population:
            per = math.floor(100 * ((1/self.population[i])/sum))
            wheel[(current,current+per)] = i
            
        num = random.randint(0, math.floor(current))
        
        for ran in wheel:
            if num >= ran[0] and num <= ran[1]:
                return wheel[ran]
        
        r = random.randint(0, len(self.population)-1)
        return self.population.keys()[r]
    
    def ranked(self):
        pop = self.population.copy()
        sor = sorted(pop.keys(), key=lambda x: pop[x])
        sor.reverse()
        
        ranks = {}
        current = 0
        for i in range(1,len(sor)+1):
            ranks[(current,current+ i)] = sor[i]
            current+= i
        num = random.randint(0, math.floor(current))
        
        for ran in ranks:
            if num >= ran[0] and num <= ran[1]:
                return ranks[ran]
            
        return sor[0]
    
    def tournament(self, size):
        participants = {}
        for i in range(size):
            p = random.choice(self.population.keys())
            participants[p] = self.population[p]
            
        max = 0
        winner = p
        for i in participants:
            if participants[i] > max:
                max = participants[i]
                winner = i
        return winner
    
    def truncation(self):
        winner = self.population.keys()[0]
        for i in self.population:
            if self.population[i] > max:
                max = self.population[i]
                winner = i
        return winner
    
    def random_selection(self):
        return random.choice(self.population.keys())
    
    
    
    # selection schemes parents selection variant
    def create_offsprings_fitness_proportional(self):
        sum = 0
        for ind in self.population:
            sum += 1/self.population[ind]
        wheel = {}
        current = 0
        for i in self.population:
            per = math.floor(100 * ((1/self.population[i])/sum))
            wheel[(current,current+per)] = i
            
        
        for o in range(self.offsprings):
            
            num = random.randint(0, math.floor(current))
            
            for ran in wheel:
                if num >= ran[0] and num <= ran[1]:
                    parent_1 = wheel[ran]
                    
            num = random.randint(0, math.floor(current))
            
            for ran in wheel:
                if num >= ran[0] and num <= ran[1]:
                    parent_2 = wheel[ran]
                    
            child =  self.crossover(parent_1, parent_2)
            self.population[child] = self.compute_fitness(child)
                
        return self.population
    
    def create_offsprings_ranked(self):
        pop = self.population.copy()
        sor = sorted(pop.keys(), key=lambda x: pop[x])
        sor.reverse()
        
        ranks = {}
        current = 0
        for i in range(1,len(sor)+1):
            ranks[(current,current+ i)] = sor[i]
            current+= i
        
        for o in range(self.offsprings):
            num = random.randint(0, math.floor(current))
        
            for ran in ranks:
                if num >= ran[0] and num <= ran[1]:
                    parent_1 = ranks[ran]
                    
            num = random.randint(0, math.floor(current))
        
            for ran in ranks:
                if num >= ran[0] and num <= ran[1]:
                    parent_2 = ranks[ran]
                    
            child =  self.crossover(parent_1, parent_2)
            self.population[child] = self.compute_fitness(child)
                
        return self.population
    
    def create_offsprings_tournament(self, size):
        
        return winner
    
    def truncation(self):
        winner = self.population.keys()[0]
        for i in self.population:
            if self.population[i] > max:
                max = self.population[i]
                winner = i
        return winner
    
    def random_selection(self):
        return random.choice(self.population.keys())
    
    
    
    
    
    
    
    
    
    
    
    
    def mutation(individual):
        return individual
    
    def evolution(self):
        self.initialize_population()
        for g in range(self.generation):
            self.create_offsprings_fitness_proportional()
            # for o in range(self.offsprings):
            #     parent_1 = self.ranked()
            #     parent_2 = self.fitness_proportional()
            #     child =  self.crossover(parent_1, parent_2)
            #     self.population[child] = self.compute_fitness(child)
            
            new = {}
            for t in range(self.size):
                surviver = self.truncation()
                new[surviver] = self.population[surviver]
            self.population = new
            
                
        
        
        
    
        
        

evol = EA(size = 5)
evol.get_data("qa194.tsp")
# print(evol.data)
evol.initialize_population()
# for i in evol.population:
#     print(i)
# print(evol.population)
