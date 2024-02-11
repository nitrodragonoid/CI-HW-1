
 # Python program to read
# image using PIL module
 
# importing PIL
from PIL import Image
 
# Read image
# img = Image.open('mona_lisa.jpg')
 
# # Output Images
# img.show()
 
# # prints format of image
# print(img.format)
 
# # prints mode of image
# print(img.mode)
# # data = list(img.getdata())
# # for i in data:
# #     print("row",i)
    
    
# pixels = list(img.getdata())
# width, height = img.size
# pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

# for i in pixels:
#     print("row",i)
# print("data:",data)


import random
import math

def permutation(lst):
    
    if len(lst) == 0:
        return []
 
    if len(lst) == 1:
        return [lst]
 
 
    l = [] 
    for i in range(len(lst)):
       m = lst[i]
 
       remLst = lst[:i] + lst[i+1:]
 
       for p in permutation(remLst):
           l.append([m] + p)
    return l

class EA:
    def __init__(self, size = 30, generations = 50 , offsprings =  10, rate = 0.5, iteration = 10, mutation = 1, parent_scheme = 1, surviver_scheme = 1, tournament_size = 2, data = {1:(1,1)}):
        self.data = data
        self.image = list()
        self.size = size
        self.population = {}
        self.generation = generations
        self.offsprings = offsprings
        self.mutation_rate = rate
        self.iterations = iteration
        self.mutation = mutation 
        self.parent_scheme = parent_scheme
        self.surviver_scheme = surviver_scheme
        self.tournament_size = tournament_size
        

    def get_data(self, file):
        
        img = Image.open(file)
 
        img.show()
 
        print(img.format)
 
        print(img.mode)    
    
        pixels = list(img.getdata())
        width, height = img.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

        self.image = pixels
        
        return self.data
    
    def area(x1, y1, x2, y2, x3, y3):
         
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) 
                + x3 * (y1 - y2)) / 2.0)
        
    def is_in(self, point, triangle):
        
        A = self.area(triangle[0][0], triangle[0][1], triangle[1][0], triangle[1][1], triangle[2][0], triangle[2][1])
        
        A1 = self.area(point[0], point[1], triangle[1][0], triangle[1][1], triangle[2][0], triangle[2][1])

        A2 = self.area(triangle[0][0], triangle[0][1], point[0], point[1], triangle[2][0], triangle[2][1])
        
        A3 = self.area(triangle[0][0], triangle[0][1], triangle[1][0], triangle[1][1], point[0], point[1])

        if(A == A1 + A2 + A3):
            return True
        else:
            return False
    
    def compute_fitness(self,ind):
        total = 0 
        for i in range(len(ind)):
            d = math.sqrt((self.data[ind[i-1]][0] - self.data[ind[i]][0])**2 + (self.data[ind[i-1]][1] - self.data[ind[i]][1])**2)
            total += d
        # d = math.sqrt((self.data[ind[0]][0] - self.data[ind[len(ind)-1]][0])**2 + (self.data[ind[0]][1] - self.data[ind[len(ind)-1]][1])**2)
        # total += d
        return total
    
    def initialize_population(self):
        arr = self.cities.copy()
        for i in range(self.size):
            ind = arr.copy()
            random.shuffle(ind)
            self.population[tuple(ind)] = self.compute_fitness(ind)
            # print(self.population[tuple(ind)])
        return self.population
        
    def crossover(self, p1, p2):
        parent_1 = list(p1)
        parent_2 = list(p2)
        ind = []
        start = random.randint(0, (len(parent_1)//2)-1)
        
        for i in range(len(parent_1)//2):
            ind.append(parent_1[i+start])
            
        for j in range(len(parent_2)):
            if parent_2[j] not in ind:
                ind.append(parent_2[j])
        
        return tuple(ind)
    
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
            current+=per
        # print(wheel)
            
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
        for i in range(1,len(sor)-1):
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
            p = random.choice(list(self.population.keys()))
            participants[p] = self.population[p]
            
        min = math.inf
        winner = p
        for i in participants:
            if participants[i] < min:
                min = participants[i]
                winner = i
        return winner
    
    def truncation(self,sols):
        winner = sols[0]
        min = math.inf
        for i in sols:
            if self.population[i] < min:
                min = self.population[i]
                winner = i
        return winner
    
    def random_selection(self):
        return random.choice(list(self.population.keys()))
    
    
    
    # selection schemes for parents selection 
    def create_offsprings_fitness_proportional(self):
        sum = 0
        for ind in self.population:
            sum += 1/self.population[ind]
        wheel = {}
        current = 0
        for i in self.population:
            per = math.floor(100 * ((1/self.population[i])/sum))
            wheel[(current,current+per)] = i
            current+=per
        # print(wheel)
            
        
        for o in range(self.offsprings):
            
            num = random.randint(0, math.floor(current))
            
            for ran in wheel:
                if num >= ran[0] and num <= ran[1]:
                    parent_1 = wheel[ran]
                    
            num = random.randint(0, math.floor(current))
            
            for ran in wheel:
                if num >= ran[0] and num <= ran[1]:
                    parent_2 = wheel[ran]
            
            if self.mutation == 1:                    
                child =  self.swap_mutation(self.crossover(parent_1, parent_2))
            else:
                child =  self.insert_mutation(self.crossover(parent_1, parent_2))
            self.population[child] = self.compute_fitness(child)
                
        return self.population
    
    def create_offsprings_ranked(self):
        pop = self.population.copy()
        sor = sorted(pop.keys(), key=lambda x: pop[x])
        sor.reverse()
        
        ranks = {}
        current = 0
        for i in range(len(sor)):
            ranks[(current,current+ i+1)] = sor[i]
            current+= i
        
        
        for o in range(self.offsprings):
            num = random.randint(0, math.floor(current))
            
            parent_1 = list(self.population.keys())[0]
            parent_2 = list(self.population.keys())[0]
            for ran in ranks:
                if num >= ran[0] and num <= ran[1]:
                    parent_1 = ranks[ran]
                    # print(parent_1)
                    break
                    
            num = random.randint(0, math.floor(current))
        
            for ran in ranks:
                if num >= ran[0] and num <= ran[1]:
                    parent_2 = ranks[ran]
                    break
                
            if self.mutation == 1:                    
                child =  self.swap_mutation(self.crossover(parent_1, parent_2))
            else:
                child =  self.insert_mutation(self.crossover(parent_1, parent_2))
            self.population[child] = self.compute_fitness(child)
                
        return self.population
    
    def create_offsprings_tournament(self, size):
        for o in range(self.offsprings):
            parent_1 = self.tournament(size)
            parent_2 = self.tournament(size)
            
            if self.mutation == 1:                    
                child = self.swap_mutation(self.crossover(parent_1, parent_2))
            else:
                child = self.insert_mutation(self.crossover(parent_1, parent_2))
            self.population[child] = self.compute_fitness(child)
                
        return self.population
    
    def create_offsprings_truncation(self):
        arr = list(self.population.keys()).copy()
        for o in range(self.offsprings):
            parent_1 = self.truncation(arr)
            arr.remove(parent_1)
            parent_2 = self.truncation(arr)
            
            if self.mutation == 1:                    
                child =  self.swap_mutation(self.crossover(parent_1, parent_2))
            else:
                child =  self.insert_mutation(self.crossover(parent_1, parent_2))
            self.population[child] = self.compute_fitness(child)
                
        return self.population
    
    def create_offsprings_random_selection(self):
        for o in range(self.offsprings):
            parent_1 = self.random_selection()
            parent_2 = self.random_selection()
            
            if self.mutation == 1:                    
                child =  self.swap_mutation(self.crossover(parent_1, parent_2))
            else:
                child =  self.insert_mutation(self.crossover(parent_1, parent_2))
            self.population[child] = self.compute_fitness(child)
                
        return self.population


    # selection schemes for surviver selection
    def survivers_fitness_proportional(self):
        sum = 0
        for ind in self.population:
            sum += 1/self.population[ind]
        wheel = {}
        current = 0
        for i in self.population:
            per = math.floor(100 * ((1/self.population[i])/sum))
            wheel[(current,current+per)] = i
            current+=per
        # print(wheel)
            
        num = random.randint(0, math.floor(current))
        
        new = {}
        
        for s in range(self.generation):
        
            for ran in wheel:
                if num >= ran[0] and num <= ran[1]:
                    new[wheel[ran]] = self.population[wheel[ran]]
        
        self.population = new
        return self.population
    
    def survivers_ranked(self):
        pop = self.population.copy()
        sor = sorted(pop.keys(), key=lambda x: pop[x])
        sor.reverse()
        
        ranks = {}
        current = 0
        for i in range(len(sor)):
            ranks[(current,current+ i+1)] = sor[i]
            current+= i
        num = random.randint(0, math.floor(current))
        
        new = {}
        
        for s in range(self.generation):
        
            for ran in ranks:
                if num >= ran[0] and num <= ran[1]:
                    new[ranks[ran]] = self.population[ranks[ran]]
        
        self.population = new
        return self.population
    
    def survivers_tournament(self, size):
        new = {}
        
        for s in range(self.generation):
            
            survivor = self.tournament(size)
            new[survivor] = self.population[survivor]
        
        self.population = new
        return self.population
    
    def survivers_truncation(self):
        new = {}
        arr = list(self.population.keys()).copy()
        if len(arr) == self.generation:
            return self.population
        for s in range(self.size):
            
            survivor = self.truncation(arr)
            arr.remove(survivor)
            new[survivor] = self.population[survivor]
        
        self.population = new
        return self.population
    
    def survivers_random_selection(self):
        new = {}
        
        for s in range(self.generation):
            
            survivor = self.random_selection()
            new[survivor] = self.population[survivor]
        
        self.population = new
        return self.population
    
    
    # mutation schemes
    def swap_mutation(self,individual):
        r = random.randint(0,100)
        num = 100 * self.mutation_rate
        mutated = list(individual)
        if r <= num:
            i = random.randint(0,len(mutated)-1)
            j = random.randint(0,len(mutated)-1)
            temp = mutated[i]
            mutated[i] = mutated[j]
            mutated[j] = temp
            
        return tuple(mutated)
    
    def insert_mutation(self,individual):
        r = random.randint(0,100)
        num = 100 * self.mutation_rate
        mutated = list(individual)
        if r <= num:
            i = random.randint(0,len(mutated)-1)
            j = random.randint(0,len(mutated)-1)
            city = mutated[i]
            mutated.remove(city)
            mutated.insert(j,city)
            
        return tuple(mutated)
    
    
    def best(self):
        winner = list(self.population.keys())[0]
        min = math.inf
        for i in self.population:
            if self.population[i] < min:
                min = self.population[i]
                winner = i
        
        print(winner)
        print(min)
        return winner,min
    
    
    def tsp_brute_force(self):
        arr = self.cities.copy()
        
        sols = permutation(arr)
        
        min_fit = math.inf
        best = sols[0]
        for i in sols:
            fitness = self.compute_fitness(i)
            if fitness <= min_fit:
                min_fit = fitness
                best = i
                
        print(best,":",min_fit)
        return best,min_fit
    
    def evolution(self):
        self.initialize_population()
        for g in range(self.generation):
            # print(g)
            # print(self.population)
            
            # best_ind = self.truncation()
            # best_score = self.population[best_ind]
        
            # print(best_ind)
            # print(best_score)
            if self.parent_scheme == 1:
                self.create_offsprings_fitness_proportional()
            elif self.parent_scheme == 2:
                self.create_offsprings_ranked()
            elif self.parent_scheme == 3:
                self.create_offsprings_tournament(self.tournament_size)
            elif self.parent_scheme == 4:
                self.create_offsprings_truncation()
            else:
                self.create_offsprings_random_selection()
            

            if self.parent_scheme == 1:
                self.survivers_fitness_proportional()
            elif self.parent_scheme == 2:
                self.survivers_ranked()
            elif self.parent_scheme == 3:
                self.survivers_tournament(self.tournament_size)
            elif self.parent_scheme == 4:
                self.survivers_truncation()
            else:
                self.survivers_random_selection()
            
            
        self.best()
        


 