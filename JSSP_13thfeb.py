
import numpy as np
import random
import math
 
#Analysis of the problem ,chromosome representation and fitness function.

def initialization(file_path): 
    result_dict = {}
    first_line_tuples = None
   
    with open(file_path, 'r') as file:
        first_line_skipped = False
       
        for line in file:
            if not first_line_skipped:
                values = line.strip().split()  
                first_line_tuples = [(int(values[i]), int(values[i+1])) for i in range(0, len(values)-1, 2)]
               
                first_line_skipped = True
                continue
           
            values = line.strip().split()  
            tuples = [(int(values[i]), int(values[i+1])) for i in range(0, len(values)-1, 2)]
            result_dict[len(result_dict)] = tuples
   

    x = first_line_tuples
    jsspdata = result_dict
 
    if x is not None:
        no_of_jobs = x[0][0]
        no_of_machines = x[0][1]

    population = {}
 
    for i in range(30):
 
        operations = []
        machines_current_times = []
        for i in range(no_of_jobs):
            operations.append(0)
        # print(operations)
        for i in range(no_of_machines):
            machines_current_times.append(0)
 
        # print(machines_current_times)
 
        Machines_operating_times = []
 
        for i in range(no_of_machines):
            Machines_operating_times.append([])
        prev_operations_time = []
        for i in range(no_of_machines):
            prev_operations_time.append(0)
 
        completed_jobs = 0
 
        while (completed_jobs<no_of_jobs):
            job = random.randint(0,no_of_jobs-1)
 
            while operations[job] == no_of_machines:
                job = random.randint(0,no_of_jobs-1)
 
            operation = operations[job]
            curr_job = jsspdata[job]
            machine_num = curr_job[operation][0]
            time_for_operation = curr_job[operation][1]
            start_time = max(prev_operations_time[job],machines_current_times[job])
            end_time = start_time + time_for_operation
            machines_current_times[machine_num] = end_time
            prev_operations_time[job] = end_time
 
            operations[job]+=1
            if operations[job] == no_of_machines:
                completed_jobs += 1
 
            Machines_operating_times[machine_num].append((job,operation,start_time,end_time))
        Machines_operating_times_tuple = []
        for i in Machines_operating_times:
            Machines_operating_times_tuple.append(tuple(i))
        
        Machines_operating_times=tuple(Machines_operating_times_tuple)

        population[tuple(Machines_operating_times)] = fitness_computation(Machines_operating_times)
    return population
 
 
def fitness_computation(individual):        
    # fitness_value=[]
    # for i in population:
    #     print(i)
        all_machine_times=[]
        # if type(individual) == int():
        print(type(individual),individual)
        for j in range(len(individual)):
            # print(j)
            machine_max_time = individual[j][-1][3]
            all_machine_times.append(machine_max_time)
        y =  max(all_machine_times)
        return y
       
 
#     return fitness_value
 
# file_path = r'C:\Users\Student\OneDrive - Habib University\Sem 8\CI\abz5.txt'
file_path = r'C:\Users\Student\OneDrive - Habib University\Sem 8\CI\abz5.txt' 
 
jssp_data = initialization(file_path)
# print(jssp_data)
 
# # def parent_selection(population,scheme,fitness,parent_size):
# #     if scheme == "Truncation":
# #         parents=[]
# #         fit = np.argsort(fitness)
# #         for i in range(parent_size):
# #             x = fit[i]
# #             parents.append(population[x])
# #         return parents
 
 
   
# def crossover(parents,offspring_size,no_of_machines):
 
#     offspring=[]
#     for i in range(len(parents)):
#         par1 = parents[i]
#         par2 = parents[i+1]
#         child_dict = {}
#         random = []
#         for i in range(5):
#             random.append(random.randint(0,no_of_machines-1))
#         for j in par1:
#             if j in random:
#                 child_dict[j] = (par1[j]).copy()
#             else:
#                 child_dict[j] = (par2[j]).copy()
#         offspring.append(child_dict)
   
 

def crossover(p1, p2):
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

# mutation schemes
def swap_mutation(individual,mutation_rate):
    r = random.randint(0,100)
    num = 100 * mutation_rate
    mutated = list(individual)
    m = False
    if r <= num:
        i = random.randint(0,len(mutated)-1)
        j = random.randint(0,len(mutated)-1)
        temp = mutated[i]
        mutated[i] = mutated[j]
        mutated[j] = temp
        m = True
        
    individual = tuple(mutated)
    return m

# def best(population):
#     winner = list(population.keys())[0]
#     min = math.inf
#     for i in population:
#         if population[i] < min:
#             min = population[i]
#             winner = i
    
#     print(winner)
#     print(min)
#     return winner,min
 
# # selection schemes
def fitness_proportional(population):
    sum = 0
    for ind in population:
        sum += 1/population[ind]
    wheel = {}
    current = 0
    for i in population:
        per = math.floor(100 * ((1/population[i])/sum))
        wheel[(current,current+per)] = i
        current+=per
    # print(wheel)
        
    num = random.randint(0, math.floor(current))
    
    for ran in wheel:
        if num >= ran[0] and num <= ran[1]:
            return wheel[ran]
    
    r = random.randint(0, len(population)-1)
    return population.keys()[r]
   
def ranked(population):
    pop = population.copy()
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
   
def tournament(population,size):
    participants = {}
    for i in range(size):
        p = random.choice(list(population.keys()))
        participants[p] = population[p]
        
    min = math.inf
    winner = p
    for i in participants:
        if participants[i] < min:
            min = participants[i]
            winner = i
    return winner
   
sols = list(jssp_data.keys())

def truncation(population,sols):
    
    
    winner = sols[0]
    min = math.inf
    for i in sols:
        if population[i] < min:
            min = population[i]
            winner = i
    return winner


# nner = truncation(jssp_data,sols)
# sols.remove(winner)
# winner0 = truncation(jssp_data,sols)
# print(winner)
   

# winner1 = tournament(jssp_data,10)
# print(winner1)  
def random_selection(population):
    return random.choice(list(population.keys()))
   
# winner2 = ranked(jssp_data)
# print(winner2) 
 
# winner3 = fitness_proportional(jssp_data)
# print(winner3) 
 
 
 
# offspring = crossover(winner,winner0)
# print(offspring)

# mut = swap_mutation(offspring,0.5)
# print(mut)

 
 


def survivers_fitness_proportional(population,generation):
        sum = 0
        for ind in population:
            sum += 1/population[ind]
        wheel = {}
        current = 0
        for i in  population:
            per = math.floor(100 * ((1/population[i])/sum))
            wheel[(current,current+per)] = i
            current+=per
        # print(wheel)
            
        num = random.randint(0, math.floor(current))
        
        new = {}
        
        for s in range(generation):
        
            for ran in wheel:
                if num >= ran[0] and num <= ran[1]:
                    new[wheel[ran]] = population[wheel[ran]]
        
        population = new
        return  population
    
def survivers_ranked(population,generation):
    pop =  population.copy()
    sor = sorted(pop.keys(), key=lambda x: pop[x])
    sor.reverse()
    
    ranks = {}
    current = 0
    for i in range(len(sor)):
        ranks[(current,current+ i+1)] = sor[i]
        current+= i
    num = random.randint(0, math.floor(current))
    
    new = {}
    
    for s in range(generation):
    
        for ran in ranks:
            if num >= ran[0] and num <= ran[1]:
                new[ranks[ran]] =  population[ranks[ran]]
    
    population = new
    return  population

def survivers_tournament(population,size,generation):
    new = {}
    
    for s in range(generation):
        
        survivor =  tournament(size)
        new[survivor] =  population[survivor]
    
    population = new
    return  population

def survivers_truncation(population,size,generation):
    sols = list(jssp_data.keys())
    new = {}
    arr = population
    if len(arr) ==    generation:
        return    population
    for s in range(size):
        
        survivor =    truncation(arr,sols)
        sols.remove(survivor)
            # print("here")

        new[survivor] =    population[survivor]
        
    population = new

    return    population

def survivers_random_selection(generation):
    new = {}
    
    for s in range(generation):
        
        survivor =    random_selection()
        new[survivor] =  population[survivor]
    
    population = new
    return  population

surv = survivers_truncation(jssp_data,30,50)





file_path = r'C:\Users\Student\OneDrive - Habib University\Sem 8\CI\abz5.txt'
population = initialization(file_path)
# print(population)
Generations = 50
pop_size = 30
mutation_rate = 0.95
Current_Gen = 0
fit_lst_gen = []
pop_lst_gen = []
off_spr = 10
while Current_Gen<Generations:
    
    fitness_lst = []
    for i in range(off_spr):
        sols = list(population.keys())
        parent_1 = truncation(population,sols)
        sols.remove(parent_1)
        parent_2 = truncation(population,sols)
    # offsprings 
    # for i in range(0,len(parents),2):
        offspringss = crossover(parent_1,parent_2)
    # for i in offspringss:
    #     print("off", offspringss)
    #     print("before",i)
        swap_mutation(offspringss,mutation_rate)
        # if mutated == True:
        #     print("mutated",i)
    # for i in offspringss:
    #     print("offsprings")
        fitness_lst.append(fitness_computation(offspringss))
        population[i] = offspringss
        new_pop = population
    for i in pop_size:
        survivorss = survivers_truncation(new_pop,pop_size,Generations)
        population = survivorss.copy()
        fit_lst_gen.append(fitness_lst)
        pop_lst_gen.append(population)
        Current_Gen+=1
        print(Current_Gen)

print("fit_lst_gen",fit_lst_gen)
Avg_fit_lst = [(sum(i)/(len(i))) for i in fit_lst_gen]
best_fit_lst = [min(i) for i in fit_lst_gen]
# print("population",population)




