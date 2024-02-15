import random
import math
from numpy.random import choice   
import matplotlib.pyplot as plt
import numpy as np


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
        self.cities = []
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
        for i in range(len(ind)):
            d = math.sqrt((self.data[ind[i-1]][0] - self.data[ind[i]][0])**2 + (self.data[ind[i-1]][1] - self.data[ind[i]][1])**2)
            total += d
        # d = math.sqrt((self.data[ind[0]][0] - self.data[ind[len(ind)-1]][0])**2 + (self.data[ind[0]][1] - self.data[ind[len(ind)-1]][1])**2)
        # total += d
        return total
    
    def initialize_population(self):
        arr = self.cities.copy()
        self.population = {}
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
        if len(ind) != len(parent_1):
            print("error")
            return False
        
        return tuple(ind)
    
    # selection schemes
    def fitness_proportional(self):
        
        total_weight = 0
        for ind in self.population:
            total_weight += 1/self.population[ind]
            
        individuals =  list(self.population.keys())
        
        c = []
        for i in range(len(individuals)):
            c.append(i)
        
        relative_fitness= [(1/self.population[i])/total_weight for i in individuals]
        
        win = choice(c, 1, p=relative_fitness)

        return individuals[win[0]]
    
    
    def ranked(self):
        
        pop = self.population.copy()
        sor = sorted(pop.keys(), key=lambda x: pop[x])
        sor.reverse()
        
        individuals =  list(self.population.keys())
        
        n = len(individuals)
        total_weight = (n*(n+1))/2
        
        
        c = []
        for i in range(len(individuals)):
            c.append(i)
        
        relative_fitness= [i/total_weight for i in c]
        
        win = choice(c, 1, p=relative_fitness)

        return individuals[win[0]]
        # pop = self.population.copy()
        # sor = sorted(pop.keys(), key=lambda x: pop[x])
        # sor.reverse()
        
        # ranks = {}
        # current = 0
        # for i in range(1,len(sor)-1):
        #     ranks[(current,current+ i)] = sor[i]
        #     current+= i
        # num = random.randint(0, math.floor(current))
        
        # for ran in ranks:
        #     if num >= ran[0] and num <= ran[1]:
        #         return ranks[ran]
            
        # return sor[0]
    
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
            
        total_weight = 0
        for ind in self.population:
            total_weight += 1/self.population[ind]
            
        individuals =  list(self.population.keys())
                
        c = []
        for i in range(len(individuals)):
            c.append(i)
        
        relative_fitness= [(1/self.population[i])/total_weight for i in individuals]
        
        
        for o in range(self.offsprings):
            
            win = choice(c, 1, p=relative_fitness)
            parent_1 = individuals[win[0]]
            win = choice(c, 1, p=relative_fitness)
            parent_2 = individuals[win[0]]
            
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
        
        # ranks = {}
        # current = 0
        # for i in range(len(sor)):
        #     ranks[(current,current+ i+1)] = sor[i]
        #     current+= i
        
        individuals =  list(self.population.keys())
        
        n = len(individuals)
        total_weight = (n*(n+1))/2
        
        
        c = []
        for i in range(len(individuals)):
            c.append(i)
        
        relative_fitness = [(i+1)/total_weight for i in c]
        
        
        for o in range(self.offsprings):
            
            win = choice(c, 1, p=relative_fitness)
            parent_1 = individuals[win[0]]
            
            win = choice(c, 1, p=relative_fitness)
            parent_2 = individuals[win[0]]
            # num = random.randint(0, math.floor(current))
            
            # parent_1 = list(self.population.keys())[0]
            # parent_2 = list(self.population.keys())[0]
            # for ran in ranks:
            #     if num >= ran[0] and num <= ran[1]:
            #         parent_1 = ranks[ran]
            #         # print(parent_1)
            #         break
                    
            # num = random.randint(0, math.floor(current))
        
            # for ran in ranks:
            #     if num >= ran[0] and num <= ran[1]:
            #         parent_2 = ranks[ran]
            #         break
                
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
        # sum = 0
        # for ind in self.population:
        #     sum += 1/self.population[ind]
        # wheel = {}
        # current = 0
        # for i in self.population:
        #     per = math.floor(100 * ((1/self.population[i])/sum))
        #     wheel[(current,current+per)] = i
        #     current+=per
        # print(wheel)
        
        total_weight = 0
        for ind in self.population:
            total_weight += 1/self.population[ind]
            
        individuals =  list(self.population.keys())
        
        # relative_fitness = [(1/self.population[i])/total_weight for i in individuals]
            
        # num = random.randint(0, math.floor(current))
        
        c = []
        for i in range(len(individuals)):
            c.append(i)
        
        relative_fitness= [(1/self.population[i])/total_weight for i in individuals]
        
        win = choice(c, 1, p=relative_fitness)

        
        new = {}
        
        for s in range(self.generation):
            
            win = choice(c, 1, p=relative_fitness)
            
            sur = individuals[win[0]]
            new[sur] = self.population[sur]
            # for ran in wheel:
            #     if num >= ran[0] and num <= ran[1]:
            #         new[wheel[ran]] = self.population[wheel[ran]]
        
        self.population = new
        return self.population
    
    def survivers_ranked(self):
        pop = self.population.copy()
        sor = sorted(pop.keys(), key=lambda x: pop[x])
        sor.reverse()
        
        # ranks = {}
        # current = 0
        # for i in range(len(sor)):
        #     ranks[(current,current+ i+1)] = sor[i]
        #     current+= i
        # num = random.randint(0, math.floor(current))
        
        individuals =  list(self.population.keys())
        
        n = len(individuals)
        total_weight = (n*(n+1))/2
        
        
        c = []
        for i in range(len(individuals)):
            c.append(i)
        
        relative_fitness = [(i+1)/total_weight for i in c]
        
        new = {}
        
        for s in range(self.generation):
            
            win = choice(c, 1, p=relative_fitness)
            
            sur = individuals[win[0]]
            new[sur] = self.population[sur]
            # win = choice(c, 1, p=relative_fitness)
            # parent_1 = individuals[win[0]]
        
            # for ran in ranks:
            #     if num >= ran[0] and num <= ran[1]:
            #         new[ranks[ran]] = self.population[ranks[ran]]
        
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
        
        # print(winner)
        # print(min)
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
            print(g)
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
            # for o in range(self.offsprings):
            #     parent_1 = self.ranked()
            #     parent_2 = self.fitness_proportional()
            #     child =  self.crossover(parent_1, parent_2)
            #     self.population[child] = self.compute_fitness(child)
            
            # new = {}
            # for t in range(self.size):
            #     surviver = self.truncation()
            #     new[surviver] = self.population[surviver]
            # self.population = new
          
        winner, min = self.best()
        print(winner)
        print(min)
        
    def test(self,k):
        l = k+1
        fitprop = []
        for i in range(self.generation):
            r = []
            for j in range(k+1):
                r.append(0)
            fitprop.append(r)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_fitness_proportional()

                self.survivers_fitness_proportional()
                
                b = self.best()[1]
                fitprop[g][i] = b
                fitprop[g][k] += b
        for g in range(self.generation):
            fitprop[g][k] = fitprop[g][k]/k
        
        fitprop_x = []
        y = []
        for i in range(self.generation):
            y.append(i+1)
            fitprop_x.append(fitprop[i][k])
            
            
        ranked = []
        for i in range(self.generation):
            r = []
            for j in range(k+1):
                r.append(0)
            ranked.append(r)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_ranked()

                self.survivers_ranked()
                
                b = self.best()[1]
                ranked[g][i] = b
                ranked[g][k] += b
        for g in range(self.generation):
            ranked[g][k] = ranked[g][k]/k
        
        ranked_x = []
        for i in range(self.generation):
            ranked_x.append(ranked[i][k])
            
            
            
        tournament = []
        for i in range(self.generation):
            r = []
            for j in range(k+1):
                r.append(0)
            tournament.append(r)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_tournament(self.tournament_size)

                self.survivers_tournament(self.tournament_size)
                
                b = self.best()[1]
                tournament[g][i] = b
                tournament[g][k] += b
        for g in range(self.generation):
            tournament[g][k] = tournament[g][k]/k
        
        tournament_x = []
        for i in range(self.generation):
            tournament_x.append(tournament[i][k])
            
            
            
        truncation = []
        for i in range(self.generation):
            r = []
            for j in range(k+1):
                r.append(0)
            truncation.append(r)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_truncation()

                self.survivers_truncation()
                
                b = self.best()[1]
                truncation[g][i] = b
                truncation[g][k] += b
        for g in range(self.generation):
            truncation[g][k] = truncation[g][k]/k
        
        truncation_x = []
        for i in range(self.generation):
            truncation_x.append(truncation[i][k])
            
            
            
        random = []
        for i in range(self.generation):
            r = []
            for j in range(k+1):
                r.append(0)
            random.append(r)
        
        for i in range(k):
            self.initialize_population()
            for g in range(self.generation):
            # print(g)
                self.create_offsprings_random_selection()

                self.survivers_random_selection()
                
                b = self.best()[1]
                random[g][i] = b
                random[g][k] += b
        for g in range(self.generation):
            random[g][k] = random[g][k]/k
        
        random_x = []
        for i in range(self.generation):
            random_x.append(random[i][k])
        
        print("Fittness propotional table")
        for i in range(len(random)):
            print(fitprop[i])
        print("Ranked table")
        for i in range(len(random)):
            print(ranked[i])
        print("Tournament table")
        for i in range(len(random)):
            print(tournament[i])
        print("Truncation table")
        for i in range(len(random)):
            print(truncation[i])
        print("Random table")
        for i in range(len(random)):
            print(random[i])    
        
        # print(truncation_x)
        ypoints_1 = np.array(fitprop_x)
        ypoints_2 = np.array(ranked_x)
        ypoints_3 = np.array(tournament_x)
        ypoints_4 = np.array(truncation_x)
        ypoints_5 = np.array(random_x)
        xpoints = np.array(y)
        
        # plt.plot(X, y, color='r', label='sin') 
        # plt.plot(X, z, color='g', label='cos')

        plt.plot(xpoints, ypoints_1, color='r', label='fitness proportional')
        plt.plot(xpoints, ypoints_2, color='b', label='ranked')
        plt.plot(xpoints, ypoints_3, color='g', label='tournament')
        plt.plot(xpoints, ypoints_4, color='y', label='truncation')
        plt.plot(xpoints, ypoints_5, color='k', label='random')
        plt.show()
                

            
            
            
                

        
# size = 30, generations = 50 , offsprings =  10, rate = 0.5, iteration = 10, mutation = 1, parent_scheme = 1, surviver_scheme = 1
    
        
Test = EA(size = 100, generations = 100, offsprings =  20, rate = 0.5, mutation = 1, parent_scheme = 1, surviver_scheme = 4, tournament_size= 10)
Test.get_data("qa194.tsp")
# Test.evolution()
Test.test(5)

# # test.get_data("test.tsp")
# # test.tsp_brute_force()
# Test.evolution()

# current = 100
# num = random.randint(0, math.floor(current))
# print(num)
# num = random.randint(0, math.floor(current))
# print(num)
# num = random.randint(0, math.floor(current))
# print(num)

# evol = EA(size = 5)
# evol.get_data("qa194.tsp")
# # print(evol.data)
# evol.initialize_population()
# for i in evol.population:
#     print(i)
# print(evol.population)
# pop = {(1):2,(2):5,(3):4,(4):7,(5):6}

# sor = sorted(pop.keys(), key=lambda x: pop[x])
# print(sor)

# l = [[0]*5]*10
# print(l)
