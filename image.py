
 # Python program to read
# image using PIL module
 
# importing PIL
from PIL import Image
from numpy.random import choice   
import matplotlib.pyplot as plt
import numpy as np
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
    def __init__(self, size = 30, generations = 50 , offsprings =  10, rate = 0.5, iteration = 10, parent_scheme = 1, surviver_scheme = 1, tournament_size = 2, data = {1:(1,1)}):
        self.data = data
        self.image = list()
        self.size = size
        self.population = {}
        self.generation = generations
        self.offsprings = offsprings
        self.mutation_rate = rate
        self.iterations = iteration
        self.parent_scheme = parent_scheme
        self.surviver_scheme = surviver_scheme
        self.tournament_size = tournament_size
        self.width = int()
        self.height = int()
        

    def get_data(self, file):
        
        img = Image.open(file)
 
        img.show()
 
        print(img.format)
 
        print(img.mode)    
    
        pixels = list(img.getdata())
        width, height = img.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

        self.image = pixels
        
        self.width = width
        self.height = height
        
        return self.image, self.width, self.height
    
    def area(self,x1, y1, x2, y2, x3, y3):
         
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
        
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
        for i in range(self.height):
            for j in range(self.width):
                red = 0
                green = 0 
                blue = 0
                
                for k in ind:
                    if self.is_in((i,j), k[0]) == True:
                        red += k[1][0]*k[2]
                        green += k[1][1]*k[2]
                        blue += k[1][2]*k[2]
                        
                if red >255:
                    red = 255
                    
                if green >255:
                    green = 255
                    
                if blue >255:
                    blue = 255
                    
                total += math.sqrt((self.image[i][j][0] - red)**2 + (self.image[i][j][1] - green)**2 + (self.image[i][j][2] - blue)**2)
        
        return total/(self.width*self.height)              
    
    def initialize_population(self):
        self.population = {}
        for i in range(self.size):
            ind = []
            for j in range(50):
                x1 = random.randint(0,self.width-1)
                y1 = random.randint(0,self.height-1)
                x2 = random.randint(0,self.width-1)
                y2 = random.randint(0,self.height-1)
                x3 = random.randint(0,self.width-1)
                y3 = random.randint(0,self.height-1)
            
                triangle = ((x1,y1),(x2,y2),(x3,y3))
            
                red = random.randint(0,255)
                blue = random.randint(0,255)
                green = random.randint(0,255)
                color = (red, green, blue)
            
                transparency = 0.6 
            
                ind.append((triangle,color,1-transparency))
            print(i)
            individual = tuple(ind)
            self.population[individual] = self.compute_fitness(individual)
            # print(self.population[tuple(ind)])
        return self.population
        
    def crossover(self, p1, p2):
        parent_1 = list(p1)
        parent_2 = list(p2)
        ind = []
        start = random.randint(0, (len(parent_1)//2)-1)
        
        
        for i in range(len(parent_1)//2):
            ind.append(parent_1[i+start])
            
        for j in range(start):
            ind.append(parent_2[j])
            
        for j in range(start+len(parent_1)//2,50):
            ind.append(parent_2[j])
        
        
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
        
        relative_fitness = [i/total_weight for i in c]
        
        
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
            
            child =  self.mutation(self.crossover(parent_1, parent_2))
                
        return self.population
    
    def create_offsprings_truncation(self):
        arr = list(self.population.keys()).copy()
        for o in range(self.offsprings):
            parent_1 = self.truncation(arr)
            arr.remove(parent_1)
            parent_2 = self.truncation(arr)
            
            child =  self.mutation(self.crossover(parent_1, parent_2))

            self.population[child] = self.compute_fitness(child)
                
        return self.population
    
    def create_offsprings_random_selection(self):
        for o in range(self.offsprings):
            parent_1 = self.random_selection()
            parent_2 = self.random_selection()
            
            child =  self.mutation(self.crossover(parent_1, parent_2))

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
        
        relative_fitness = [i/total_weight for i in c]
        
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
    def mutation(self,individual):
        
        r = random.randint(0,100)
        num = 100 * self.mutation_rate
        mutated = list(individual)
        if r <= num:
            i = random.randint(0,49)
            
            x1 = random.randint(0,self.width-1)
            y1 = random.randint(0,self.height-1)
            x2 = random.randint(0,self.width-1)
            y2 = random.randint(0,self.height-1)
            x3 = random.randint(0,self.width-1)
            y3 = random.randint(0,self.height-1)
            
            triangle = ((x1,y1),(x2,y2),(x3,y3))
            
            red = random.randint(0,255)
            blue = random.randint(0,255)
            green = random.randint(0,255)
            color = (red, green, blue)
            
            transparency = 0.6 
            
            mutated[i] = (triangle,color,1-transparency)
            
        return tuple(mutated)
    
    
    def show_image(self,ind):
        image_data = []
        
        # print(self.width,self.height)
        for i in range(self.height):
            for j in range(self.width):
                red = 0
                green = 0 
                blue = 0
                
                for k in ind:
                    if self.is_in((i,j), k[0]) == True:
                        red += k[1][0]*k[2]
                        green += k[1][1]*k[2]
                        blue += k[1][2]*k[2]
                        
                if red >255:
                    red = 255
                    
                if green >255:
                    green = 255
                    
                if blue >255:
                    blue = 255
                    
                # print(red,green,blue)
                image_data.append((int(red),int(green),int(blue)))
                
        # print(image_data)
        img = Image.new("RGB", (self.width,self.height))
        img.putdata(image_data)
        
        img.show()
        # img.save('/imgs')      
        return image_data
    
    
    def best(self):
        winner = list(self.population.keys())[0]
        min = math.inf
        for i in self.population:
            if self.population[i] < min:
                min = self.population[i]
                winner = i
        
        # print(winner)
        # print(min)
        
        self.show_image(winner)
        
        return winner,min
        
    
    def evolution(self):
        self.initialize_population()
        # print("here")
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
            
            
        self.best()
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
        

Test = EA(size = 100, generations = 40, offsprings =  20, rate = 0.5, parent_scheme = 4, surviver_scheme = 4, tournament_size= 10)

# test.get_data("mona_lisa.jpg")
Test.get_data("mona_lisa_smol.jpg")


# Test.evolution()
Test.test(5)

# l = ((((320, 883), (435, 612), (30, 835)), (86, 1, 97), 0.4), (((89, 889), (339, 249), (379, 901)), (51, 102, 233), 0.4), (((605, 659), (245, 548), (280, 97)), (139, 158, 63), 0.4), (((426, 45), (41, 144), (382, 717)), (128, 73, 191), 0.4), (((562, 822), (633, 56), (456, 241)), (85, 118, 247), 0.4), (((629, 286), (156, 540), (100, 203)), (26, 202, 139), 0.4), (((347, 733), (32, 729), (61, 13)), (1, 235, 189), 0.4), (((149, 922), (558, 155), (555, 92)), (71, 72, 144), 0.4), (((549, 773), (540, 297), (92, 814)), (14, 62, 192), 0.4), (((308, 409), (154, 61), (346, 871)), (69, 109, 165), 0.4), (((613, 525), (168, 584), (207, 755)), (101, 165, 180), 0.4), (((513, 842), (607, 886), (28, 128)), (58, 248, 40), 0.4), (((534, 871), (222, 861), (252, 741)), (107, 28, 246), 0.4), (((34, 63), (90, 7), (367, 670)), (100, 178, 1), 0.4), (((465, 77), (247, 891), (169, 23)), (47, 248, 174), 0.4), (((363, 874), (379, 558), (18, 944)), (3, 103, 172), 0.4), (((495, 532), (208, 499), (362, 287)), (70, 230, 229), 0.4), (((434, 704), (448, 234), (208, 466)), (164, 98, 208), 0.4), (((636, 202), (451, 873), (84, 675)), (111, 182, 42), 0.4), (((188, 694), (325, 160), (493, 622)), (102, 141, 186), 0.4), (((265, 774), (474, 15), (17, 821)), (150, 23, 46), 0.4), (((137, 84), (187, 886), (371, 681)), (198, 177, 78), 0.4), (((150, 708), (469, 678), (50, 413)), (161, 74, 74), 0.4), (((179, 712), (132, 11), (169, 29)), (158, 44, 107), 0.4), (((504, 327), (245, 279), (252, 399)), (32, 249, 89), 0.4), (((498, 761), (584, 414), (56, 433)), (118, 250, 206), 0.4), (((261, 134), (227, 169), (384, 68)), (193, 10, 184), 0.4), (((326, 120), (401, 419), (383, 484)), (153, 19, 232), 0.4), (((212, 698), (95, 425), (422, 794)), (86, 120, 28), 0.4), (((163, 812), (287, 122), (496, 64)), (254, 167, 13), 0.4), (((21, 612), (520, 94), (42, 631)), (248, 85, 212), 0.4), (((135, 367), (582, 942), (272, 186)), (193, 58, 212), 0.4), (((434, 36), (162, 689), (527, 112)), (84, 193, 49), 0.4), (((491, 740), (464, 583), (173, 397)), (243, 44, 196), 0.4), (((555, 785), (11, 917), (364, 451)), (136, 4, 253), 0.4), (((230, 336), (620, 265), (534, 429)), (93, 22, 230), 0.4), (((123, 695), (151, 857), (8, 467)), (26, 181, 47), 0.4), (((4, 921), (620, 380), (520, 896)), (90, 182, 53), 0.4), (((4, 189), (285, 182), (58, 792)), (61, 166, 163), 0.4), (((152, 878), (450, 565), (414, 759)), (25, 11, 238), 0.4), (((179, 163), (635, 196), (509, 745)), (65, 81, 108), 0.4), (((367, 826), (550, 551), (472, 773)), (55, 51, 197), 0.4), (((425, 309), (252, 354), (32, 761)), (222, 139, 79), 0.4), (((386, 865), (469, 759), (234, 535)), (173, 60, 255), 0.4), (((174, 307), (464, 811), (597, 720)), (0, 187, 74), 0.4), (((20, 369), (556, 659), (338, 103)), (251, 128, 247), 0.4), (((406, 251), (398, 357), (334, 894)), (22, 206, 1), 0.4), (((192, 91), (357, 759), (326, 682)), (96, 32, 66), 0.4), (((69, 487), (50, 199), (400, 866)), (89, 40, 241), 0.4), (((260, 214), (592, 622), (623, 706)), (70, 1, 251), 0.4))

# test.show_image(l)