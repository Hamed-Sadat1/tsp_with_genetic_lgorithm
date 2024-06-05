from random import randint,choices,sample
from sklearn.preprocessing import minmax_scale
from os import system

class genetic:
    def __init__(self,count:int,adj_matrix) -> None:
        """index of genome represent number of step(0 is starting city)"""
        self.adj_matrix=adj_matrix
        self.cities_count=len(adj_matrix)
        self.genome_count_min=int(count*0.8)
        self.genome_count_max=int(count*1.2)
        self.genome_count=count
        self.best=[]
        self.best_fitness=float('inf')
        self.genomes=[]
        random_path=list(range(self.cities_count))
        for _ in range(count):
            self.genomes.append(sample(random_path,self.cities_count))
            

    def fitness(self):
        result=[]
        
        for i in range(self.genome_count):
            result.append(0)
            current_step=self.genomes[i][0]
            for next_step in self.genomes[i][1:]:
                result[i]+=self.adj_matrix[current_step][next_step]
                current_step=next_step
            result[i]+=self.adj_matrix[current_step][self.genomes[i][0]]
            if result[i]<self.best_fitness:
                self.best_fitness=result[i]
                self.best=self.genomes[i]
            result[i]=-result[i]
        result=list(minmax_scale(result,(1,10)))
        return result
    
    
    
    def crossover(self):
        next_gen=[]
        
        fitness_result=self.fitness()
        child_population=randint(self.genome_count_min,self.genome_count_max)
        parent1=choices(list(range(self.genome_count)),weights=fitness_result,k=child_population)
        parent2=choices(list(range(self.genome_count)),weights=fitness_result,k=child_population)
        
        
        for x,y in tuple(zip(parent1,parent2)):
            crossover_point =randint(1, self.cities_count - 2)
            child=self.genomes[x][:crossover_point]
            remaining_cities = set(self.genomes[y]) - set(child)
            for i in range(self.cities_count):
                city = self.genomes[y][i]
                if self.genomes[y][i] in remaining_cities:
                    child.append(city)
                    remaining_cities.remove(city)
            
            index_1=randint(0,self.cities_count-1)
            index_2=randint(0,self.cities_count-1)
            child[index_1],child[index_2]=child[index_2],child[index_1]
            
            next_gen.append(child)
            
        self.genomes=next_gen
        self.genome_count=child_population
        
    def train(self,generations:int):
        
        for i in range(generations):
            system('cls')
            percent=(i*100)//generations
            print(f"training_progress:{percent}%\n{percent*'='}")
            self.crossover()
        print("training Done")
        result=self.best
        current_step=result[0]
        path=f"path is: {current_step}"
        for next_step in result[1:]:
            path=path+f" --> {next_step}"
            current_step=next_step
        path=path+f" --> {result[0]}"
        print(path)
        print(self.best_fitness)
        return self.best
        
            
        
cities_matrix=[
    [0,29,20,21,16],
    [29,0,15,19,28],
    [20,15,0,13,25],
    [21,19,13,0,17],
    [16,28,25,17,0]
]

dist = [
    [0,  0,  0,  0, 0],
    [0,  0,10, 15, 20],
    [0, 10, 0, 25, 25],
    [0, 15, 25, 0, 30],
    [0, 20, 25, 30, 0]]
population=genetic(200,cities_matrix)
result=population.train(1000)

