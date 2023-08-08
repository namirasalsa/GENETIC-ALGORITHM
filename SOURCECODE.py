import random
import math

def generateChromosome(chr_size):
    result = []
    for _ in range(chr_size):
        result.append(random.randint(0, 1))
    return result

def generatePopulation(pop_size, chr_size):
    pop = []
    for _ in range(pop_size):
        pop.append(generateChromosome(chr_size))
    return pop

def decodeChromosome(chr, chr_size):
    xMin, xMax = (-5, 5)
    yMin, yMax = (-5, 5)

    N, x, y = 0, 0, 0
    n = (chr_size) // 2

    for i in range(0, n):
        N += 2**-(i+1)
    for i in range(0, n):
        x += chr[i] * 2**-(i+1)
        y += chr[i+n] * 2**-(i+1)
    x = xMin + ((xMax - xMin)/ N) * x
    y = yMin + ((yMax - yMin) /N) * y
    return [x, y]

def fungsiobj(x, y):
    return ((math.cos(x) +  math.sin(y)) **2 ) / (x**2 + y**2) 

def objectiveFunc(x, y):
    return 1 / (0.001 + ((math.cos(x) +  math.sin(y)) **2 ) / (x**2 + y**2) )

def fitness(pop, chr_size):
    result = []
    for i in pop:
        result.append(objectiveFunc(*decodeChromosome(i, chr_size)))
    return result

def tournament(pop, pop_size, tour_size, chr_size):
    result = []
    for _ in range(tour_size):
        temp = pop[random.randint(0, pop_size-1)]
        if result == [] or objectiveFunc(decodeChromosome(temp, chr_size)[0], decodeChromosome(temp, chr_size)[0]) < objectiveFunc(decodeChromosome(result, chr_size)[0], decodeChromosome(result, chr_size)[0]):
            result = temp
    return result

def crossover(parentA, parentB, pc, chr_size):
    val = random.uniform(0,1)
    if val< pc:
        pindah = random.randint(0, chr_size-1)
        for i in range(pindah):
            parentA[i], parentB[i] = parentB[i], parentA[i]
    return parentA, parentB

def mutation(offspring, pm, chr_size):
    val = random.uniform(0,1)
    if val < pm:
        offspring[0][random.randint(0, chr_size-1)] = random.randint(0,1)
        offspring[1][random.randint(0, chr_size-1)] = random.randint(0,1)
    return offspring

def elitism(fit):
    idx1, idx2 = 0, 0
    for i in range(1, len(fit)):
        if fit[i] > fit[idx1]:
            idx2 = idx1
            idx1 = i
    return [idx1, idx2]

def generationalReplacement():
    chr_size, pop_size, pc, pm, generation = (10, 100, 0.8, 0.2, 100)
    tour_size = 5
    pop = generatePopulation(pop_size, chr_size)

    for _ in range(generation):
        fit = fitness(pop, chr_size)
        newPop = []
        elite1, elite2 = elitism(fit)
        newPop.append(pop[elite1])
        newPop.append(pop[elite2])

        for _ in range(0, pop_size-2, 2):
            parentA = tournament(pop, pop_size, tour_size, chr_size)
            parentB = tournament(pop, pop_size, tour_size, chr_size)
            while(parentA == parentB):
                parentB = tournament(pop, pop_size, tour_size, chr_size)
            offspring = crossover(parentA[:], parentB[:], pc, chr_size)
            offspring = mutation(offspring, pm, chr_size)
            newPop.extend(offspring)
    pop = newPop
    printNilaiMin(pop, chr_size, fit)

def printNilaiMin(pop, chr_size, fit):
    idx = fit.index(max(fit))
    decode = decodeChromosome(pop[idx], chr_size)

    print("==============HASIL GENETIC ALGORITHM==============")
    print("Kromosom Terbaik\t: ", pop[idx])
    print("Nilai fitness\t\t: ", (fit[idx]/10))
    print("Nilai fungsi\t\t: ", fungsiobj(decode[0], decode[1]))
    print("Nilai x\t\t\t: ", decode[0])
    print("Nilai y\t\t\t: ", decode[1])

generationalReplacement()


