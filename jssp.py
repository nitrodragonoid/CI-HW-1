import numpy as np
import random
import math
 
def initialization(file_path): #Problem Formulation
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
   
 
 
# file_path = r'C:\Users\Student\OneDrive - Habib University\Sem 8\CI\abz5.txt'
    x = first_line_tuples
    jsspdata = result_dict
 
    if x is not None:
        no_of_jobs = x[0][0]
        # print(no_of_jobs)
        no_of_machines = x[0][1]
        # print(no_of_machines)
    # print(jsspdata)
 
 
    #Dataset:abz5  
 
    #jobs_list
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
        
        # print(Machines_operating_times)
        Machines_operating_times=tuple(Machines_operating_times_tuple)
        # print(Machines_operating_times)
        # return True
        population[tuple(Machines_operating_times)] = fitness_computation(Machines_operating_times)
    return population
 
 
def fitness_computation(individual):        
    # fitness_value=[]
    # for i in population:
    #     print(i)
        all_machine_times=[]
        for j in range(len(individual)):
            machine_max_time = individual[j][-1][3]
            all_machine_times.append(machine_max_time)
        y =  max(all_machine_times)
        return y
       
 
#     return fitness_value
 
# file_path = r'C:\Users\Student\OneDrive - Habib University\Sem 8\CI\abz5.txt'
file_path = r'abz5.txt'

jssp_data = initialization(file_path)
print(jssp_data)
 
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
   
 
# # mutation schemes
#     def swap_mutation(individual,mutation_rate):
#         r = random.randint(0,100)
#         num = 100 * mutation_rate
#         mutated = list(individual)
#         if r <= num:
#             i = random.randint(0,len(mutated)-1)
#             j = random.randint(0,len(mutated)-1)
#             temp = mutated[i]
#             mutated[i] = mutated[j]
#             mutated[j] = temp
           
#         return tuple(mutated)
   
#     def best(population):
#         winner = list(population.keys())[0]
#         min = math.inf
#         for i in population:
#             if population[i] < min:
#                 min = population[i]
#                 winner = i
       
#         print(winner)
#         print(min)
#         return winner,min
 
# # selection schemes
#     def fitness_proportional(population):
#         sum = 0
#         for ind in population:
#             sum += 1/population[ind]
#         wheel = {}
#         current = 0
#         for i in population:
#             per = math.floor(100 * ((1/population[i])/sum))
#             wheel[(current,current+per)] = i
#             current+=per
#         # print(wheel)
           
#         num = random.randint(0, math.floor(current))
       
#         for ran in wheel:
#             if num >= ran[0] and num <= ran[1]:
#                 return wheel[ran]
       
#         r = random.randint(0, len(population)-1)
#         return population.keys()[r]
   
#     def ranked(population):
#         pop = population.copy()
#         sor = sorted(pop.keys(), key=lambda x: pop[x])
#         sor.reverse()
#         ranks = {}
#         current = 0
#         for i in range(1,len(sor)-1):
#             ranks[(current,current+ i)] = sor[i]
#             current+= i
#         num = random.randint(0, math.floor(current))
       
#         for ran in ranks:
#             if num >= ran[0] and num <= ran[1]:
#                 return ranks[ran]
           
#         return sor[0]
   
#     def tournament(population,size):
#         participants = {}
#         for i in range(size):
#             p = random.choice(list(population.keys()))
#             participants[p] = population[p]
           
#         min = math.inf
#         winner = p
#         for i in participants:
#             if participants[i] < min:
#                 min = participants[i]
#                 winner = i
#         return winner
   
#     sols = list(population.keys())
#     def truncation(population,sols):
       
       
#         winner = sols[0]
#         min = math.inf
#         for i in population.values():
#             if population[i] < min:
#                 min = population[i]
#                 winner = i
#         return winner
   
#     def random_selection(population):
#         return random.choice(list(population.keys()))
   
 
 
 
 
 
 
 
 
 
#     # selection schemes for parents selection
#     def create_offsprings_fitness_proportional(population,offsprings,mutation):
#         sum = 0
#         for ind in population:
#             sum += 1/population[ind]
#         wheel = {}
#         current = 0
#         for i in population:
#             per = math.floor(100 * ((1/population[i])/sum))
#             wheel[(current,current+per)] = i
#             current+=per
#         # print(wheel)
           
       
#         for o in range(offsprings):
           
#             num = random.randint(0, math.floor(current))
           
#             for ran in wheel:
#                 if num >= ran[0] and num <= ran[1]:
#                     parent_1 = wheel[ran]
                   
#             num = random.randint(0, math.floor(current))
           
#             for ran in wheel:
#                 if num >= ran[0] and num <= ran[1]:
#                     parent_2 = wheel[ran]
           
#             if mutation == 1:                    
#                 child =  swap_mutation(crossover(parent_1, parent_2))
               
#         return population
   
#     def create_offsprings_ranked(population,size,offsprings,mutation,fitness):
#         pop = population.copy()
#         sor = sorted(pop.keys(), key=lambda x: pop[x])
#         sor.reverse()
       
#         ranks = {}
#         current = 0
#         for i in range(len(sor)):
#             ranks[(current,current+ i+1)] = sor[i]
#             current+= i
       
       
#         for o in range(offsprings):
#             num = random.randint(0, math.floor(current))
           
#             parent_1 = list(population.keys())[0]
#             parent_2 = list(population.keys())[0]
#             for ran in ranks:
#                 if num >= ran[0] and num <= ran[1]:
#                     parent_1 = ranks[ran]
#                     # print(parent_1)
#                     break
                   
#             num = random.randint(0, math.floor(current))
       
#             for ran in ranks:
#                 if num >= ran[0] and num <= ran[1]:
#                     parent_2 = ranks[ran]
#                     break
               
#             if mutation == 1:                    
#                 child =  swap_mutation(crossover(parent_1, parent_2))
 
#             population[child] = fitness[child]
               
#         return population
   
#     def create_offsprings_tournament(population,size,offsprings,mutation,fitness):
#         for o in range( offsprings):
#             parent_1 =  tournament(size)
#             parent_2 =  tournament(size)
           
#             if mutation == 1:                    
#                 child = swap_mutation(crossover(parent_1, parent_2))
#             population[child] = fitness[child]
               
#         return population
   
#     def create_offsprings_truncation(population,offsprings,mutation,fitness):
#         arr = list(population.keys()).copy()
#         for o in range(offsprings):
#             parent_1 = truncation(arr)
#             arr.remove(parent_1)
#             parent_2 = truncation(arr)
           
#             if mutation == 1:                    
#                 child =  swap_mutation(crossover(parent_1, parent_2))
#             population[child] = fitness[child]
               
#         return population
   
#     def create_offsprings_random_selection(population,offsprings,mutation,fitness):
#         for o in range(offsprings):
#             parent_1 =  random_selection()
#             parent_2 =  random_selection()
           
#             if mutation == 1:                    
#                 child =  swap_mutation(crossover(parent_1, parent_2))
#             population[child] = fitness[child]
               
#         return population