# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""
import matplotlib
matplotlib.use('Agg')
import numpy as np
import random as random
import sys
import matplotlib.pyplot as plt 
import matplotlib.cm as cm 
import POPULATION as pop
from decimal import Decimal
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt3d
import SYSTEMMODEL as systemmodel



class GA:
    
    
    
    def __init__(self, system):
        
        
        
        self.system = system
        

        self.populationSize = 200
        self.populationPt = pop.POPULATION(self.populationSize)
        self.mutationProbability = 0.25
        self.rnd = random.Random()




#******************************************************************************************
#   MUTATIONS
#******************************************************************************************

    
    def swapMutation_old(self,child,serviceId):
        
        secondServiceId = serviceId
        while secondServiceId == serviceId:
            secondServiceId = self.rnd.randint(0,len(child)-1)
        child[serviceId]['allocationList'],child[secondServiceId]['allocationList'] = child[secondServiceId]['allocationList'],child[serviceId]['allocationList']
        
    def growthMutation_old(self,child,serviceId):
        
        currentLen = len(child[serviceId]['allocationList'])
        newElements = [self.rnd.randint(0,self.system.nodenumber-1) for r in xrange(self.rnd.randint(1,currentLen))]

        child[serviceId]['allocationList'] += newElements
                       
    def shrinkMutation_old(self,child,serviceId):
        
        child[serviceId]['allocationList'] = self.rnd.sample(child[serviceId]['allocationList'],self.rnd.randint(1,len(child[serviceId]['allocationList'])-1))
    
    def mutate_old(self,child):
        serviceSelected = self.rnd.randint(0,len(child)-1)
        #print "[Offsrping generation]: Mutation of service %s in process**********************" % str(serviceSelected)
        numContainers = len(child[serviceSelected]['allocationList'])
        
        mutationOperators = [] 
        mutationOperators.append(self.swapMutation)
        mutationOperators.append(self.growthMutation)
        if numContainers>1:
            mutationOperators.append(self.shrinkMutation)

        mutationOperators[self.rnd.randint(0,len(mutationOperators)-1)](child,serviceSelected)
    

#******************************************************************************************
#   END MUTATIONS
#******************************************************************************************

#******************************************************************************************
#   MUTATIONS
#******************************************************************************************

    
    def shuffleMutation(self,child):
        
        random.shuffle(child)
        
    def growthMutation(self,child):
        
        for serviceSelected in range(len(child)):
            #currentLen = len(child[serviceSelected]['allocationList'])
            #newElements = [self.rnd.randint(0,self.system.nodenumber-1) for r in xrange(self.rnd.randint(1,currentLen))]
            newElements = self.rnd.randint(0,self.system.nodenumber-1)
            child[serviceSelected]['allocationList'] += newElements
                       
    def shrinkMutation(self,child):
        
        for serviceSelected in range(len(child)):
            if len(child[serviceSelected]['allocationList']) > 1:
                #child[serviceSelected]['allocationList'] = self.rnd.sample(child[serviceSelected]['allocationList'],self.rnd.randint(1,len(child[serviceSelected]['allocationList'])-1))
                child[serviceSelected]['allocationList'] = self.rnd.sample(child[serviceSelected]['allocationList'],len(child[serviceSelected]['allocationList'])-1)
    
    def mutate(self,child):
        #print "[Offsrping generation]: Mutation in process**********************"
        
        mutationOperators = [] 
        mutationOperators.append(self.shuffleMutation)
        mutationOperators.append(self.growthMutation)
        mutationOperators.append(self.shrinkMutation)
        
        mutationOperators[self.rnd.randint(0,len(mutationOperators)-1)](child)
    

#******************************************************************************************
#   END MUTATIONS
#******************************************************************************************


#******************************************************************************************
#   CROSSOVER
#******************************************************************************************


    def crossover(self,f1,f2,offs):
        c1 = f1.copy()
        c2 = f2.copy()
        #crossover of the write/block chromosome
        for key,value in c1.iteritems():
            allocationF1 = c1[key]['allocationList']
            allocationF2 = c2[key]['allocationList']
#            print "before"
#            print allocationF1
#            print allocationF2
            crosspoint = self.rnd.randint(0,min(len(allocationF1),len(allocationF2))) 

            newAllocationCh1 = allocationF1[:crosspoint] + allocationF2[crosspoint:]
            newAllocationCh2 = allocationF2[:crosspoint] + allocationF1[crosspoint:]
#            print "after"
#            print newAllocationCh1
#            print newAllocationCh2
#            print "*****"
            c1[key]['allocationList'] = newAllocationCh1
            c2[key]['allocationList'] = newAllocationCh2


        offs.append(c1)
        #print "[Offsrping generation]: Children 1 added **********************"
        offs.append(c2)
        #print "[Offsrping generation]: Children 2 added **********************"



#******************************************************************************************
#   END CROSSOVER
#******************************************************************************************

#******************************************************************************************
#   nodenumber calculation
#******************************************************************************************



    def calculateNodeNumber(self,solution):
        allNodes = set()
        for key in solution:
            allNodes = allNodes | set(solution[key]['rnode']+solution[key]['wnode'])
        
        return len(allNodes)


#******************************************************************************************
#   END nodenumber calculation
#******************************************************************************************



#******************************************************************************************
#   Cluster Balance use calculation
#******************************************************************************************



    def calculateClusterBalanceUse(self,nodesLoads):
        
        #nodesLoad.append({"cpuload" : 0.0, "memorysize": 0.0, "memoryload": 0.0, "hdsize": 0.0, "hdload": 0.0})

        load = []

        
        for idx,usage in enumerate(nodesLoads):
            if usage['computationalResources']>0.0 :
                load.append(usage['computationalResources'] / self.system.nodeFeatures[idx]['capacity'] )

        return np.std(load) 


#******************************************************************************************
#   END Cluster Balance use calculation
#******************************************************************************************

#******************************************************************************************
#   Failura calculation
#******************************************************************************************



    def calculateServiceFailure(self, serviceId, serviceChromosome):
        totalFailure = 1.0
        
        allocationList = serviceChromosome['allocationList']
        usedNodes = set(allocationList)
        serviceFailure = self.system.serviceTupla[serviceId]['failrate']
        for node in usedNodes:
            failure = serviceFailure * allocationList.count(node) 
            failure = failure + self.system.nodeFeatures[node]['failrate']
            totalFailure = totalFailure * failure
            
        return totalFailure




    def calculateFailure(self,solution):
        failure = 0.0
        for key in solution:
            failure = failure + self.calculateServiceFailure(key,solution[key])
        
        return failure

#******************************************************************************************
#   END Failura calculation
#******************************************************************************************


#******************************************************************************************
#   Container balanced use calculation
#******************************************************************************************



    def calculateServiceBalancedUse(self, serviceId, serviceChromosome):
     
        serviceThr = self.system.serviceTupla[serviceId]['threshold']
        requestNumber = self.system.requestPerApp[self.system.serviceTupla[serviceId]['application']] * self.system.serviceTupla[serviceId]['requestNumber']
        scalabilityLevel = len(serviceChromosome['allocationList'])
        resourcesPerRequest = self.system.serviceTupla[serviceId]['computationalResources']
        
        return abs( (requestNumber * resourcesPerRequest) - ( serviceThr * scalabilityLevel ) )
        
    def calculateThreshold(self,solution):
        thr = 0.0
        for i,service in enumerate(solution):
             thr = thr + self.calculateServiceBalancedUse(i,solution[service])
        
        return thr       

#******************************************************************************************
#   END Container balanced use calculation
#******************************************************************************************

        
        


#******************************************************************************************
#   NetworkLoad calculation
#******************************************************************************************


    def calculateServiceNetwork(self, serviceId, chromosome):
        
        sourceNodes = set(chromosome[serviceId]['allocationList'])
        targetNodes = set()
        
        for i in self.system.serviceTupla[serviceId]['consumeServices']:
            targetNodes = targetNodes | set(chromosome[i]['allocationList'])

        distance = 0.0
        for source in sourceNodes:
            for target in targetNodes:
                distance = distance + self.system.cpdNetwork[source][target]

        return distance
        
        
    def calculateNetwork(self,solution):
        networkLoad = 0.0
        for key in solution:
                networkLoad = networkLoad +  self.calculateServiceNetwork(key, solution)
        
        return networkLoad

#******************************************************************************************
#   END NetworkLoad calculation
#******************************************************************************************


#******************************************************************************************
#   Node Workload calculation
#******************************************************************************************

    def calculateNodesWorkload(self, chromosome):
        
        nodesLoad = []
        for i in range(self.system.nodenumber):
            nodesLoad.append({"computationalResources" : 0.0})

        for key in chromosome:
            requestNumber = self.system.requestPerApp[self.system.serviceTupla[key]['application']]* self.system.serviceTupla[key]['requestNumber']
            scalabilityLevel = len(chromosome[key]['allocationList'])
            resourcesPerRequest = self.system.serviceTupla[key]['computationalResources']
            serviceLoad = requestNumber * resourcesPerRequest / scalabilityLevel
 
            for element in (chromosome[key]['allocationList']):
                nodesLoad[element]['computationalResources']= nodesLoad[element]['computationalResources'] + serviceLoad
        return nodesLoad
        
        
        
    def calculateSolutionsWorkload(self,pop):
        
        for i,citizen in enumerate(pop.population):
            pop.nodesUsages[i]=self.calculateNodesWorkload(citizen)
        

#******************************************************************************************
#   END Node Workload calculation
#******************************************************************************************



#******************************************************************************************
#   Model constraints
#******************************************************************************************

    
    def resourceUsages(self,nodes):
        for idx,v in enumerate(nodes):
            if not (v['computationalResources']<self.system.nodeFeatures[idx]['capacity']):
                return False
        return True
    
    def checkConstraints(self,pop, index):
        
        nodesLoads = pop.nodesUsages[index]
        if not self.resourceUsages(nodesLoads):
            return False
        return True

#******************************************************************************************
#   END Model constraints
#******************************************************************************************


#******************************************************************************************
#   Objectives and fitness calculation
#******************************************************************************************


    def calculateFitnessObjectives(self, pop, index): #TODO
        chr_fitness = {}
        chr_fitness["index"] = index
        #chr_fitness["performance"] = self.rnd.randint(1,100)
        
        chromosome=pop.population[index]
        nodeLoads= pop.nodesUsages[index]
        
        if self.checkConstraints(pop,index):
            chr_fitness["thresholdDistance"] = self.calculateThreshold(chromosome)

            chr_fitness["clusterbalanced"] = self.calculateClusterBalanceUse(nodeLoads)
            #chr_fitness["reliability"] = self.calculateFailure(chromosome)
            chr_fitness["networkDistance"] = self.calculateNetwork(chromosome)
        else:
            chr_fitness["thresholdDistance"] = float('inf')
            chr_fitness["clusterbalanced"] = float('inf')
            #chr_fitness["reliability"] = float('inf')
            chr_fitness["networkDistance"] = float('inf')
            
        return chr_fitness
        
    def calculatePopulationFitnessObjectives(self,pop):   
        for index,citizen in enumerate(pop.population):
            cit_fitness = self.calculateFitnessObjectives(pop,index)
            pop.fitness[index] = cit_fitness
            
        #print "[Fitness calculation]: Calculated **********************"       
        
         
    
#******************************************************************************************
#   END Objectives and fitness calculation
#******************************************************************************************




#******************************************************************************************
#   NSGA-II Algorithm
#******************************************************************************************

            
    def dominates(self,a,b):
        #checks if solution a dominates solution b, i.e. all the objectives are better in A than in B
        Adominates = True
        #### OJOOOOOO Hay un atributo en los dictionarios que no hay que tener en cuenta, el index!!!
        for key in a:
            if key!="index":  #por ese motivo está este if.
                if b[key]<=a[key]:
                    Adominates = False
                    break
        return Adominates        

        
    def crowdingDistancesAssigments(self,popT,front):
        
        for i in front:
            popT.crowdingDistances[i] = float(0)
            
        frontFitness = [popT.fitness[i] for i in front]
        #OJOOOOOO hay un atributo en el listado que es index, que no se tiene que tener en cuenta.
        for key in popT.fitness[0]:
            if key!="index":   #por ese motivo está este if.
                orderedList = sorted(frontFitness, key=lambda k: k[key])
                
                popT.crowdingDistances[orderedList[0]["index"]] = float('inf')
                minObj = orderedList[0][key]
                popT.crowdingDistances[orderedList[len(orderedList)-1]["index"]] = float('inf')
                maxObj = orderedList[len(orderedList)-1][key]
                
                normalizedDenominator = float(maxObj-minObj)
                if normalizedDenominator==0.0:
                    normalizedDenominator = float('inf')
        
                for i in range(1, len(orderedList)-1):
                    popT.crowdingDistances[orderedList[i]["index"]] += (orderedList[i+1][key] - orderedList[i-1][key])/normalizedDenominator

    def calculateCrowdingDistances(self,popT):
        
        i=0
        while len(popT.fronts[i])!=0:
            self.crowdingDistancesAssigments(popT,popT.fronts[i])
            i+=1


    def calculateDominants(self,popT):
        
        for i in range(len(popT.population)):
            popT.dominatedBy[i] = set()
            popT.dominatesTo[i] = set()
            popT.fronts[i] = set()

        for p in range(len(popT.population)):
            for q in range(p+1,len(popT.population)):
                if self.dominates(popT.fitness[p],popT.fitness[q]):
                    popT.dominatesTo[p].add(q)
                    popT.dominatedBy[q].add(p)
                if self.dominates(popT.fitness[q],popT.fitness[p]):
                    popT.dominatedBy[p].add(q)
                    popT.dominatesTo[q].add(p)        

    def calculateFronts(self,popT):

        addedToFronts = set()
        
        i=0
        while len(addedToFronts)<len(popT.population):
            popT.fronts[i] = set([index for index,item in enumerate(popT.dominatedBy) if item==set()])
            addedToFronts = addedToFronts | popT.fronts[i]
            
            for index,item in enumerate(popT.dominatedBy):
                if index in popT.fronts[i]:
                    popT.dominatedBy[index].add(-1)
                else:
                    popT.dominatedBy[index] = popT.dominatedBy[index] - popT.fronts[i]
            i+=1        
            
    def fastNonDominatedSort(self,popT):
        
        self.calculateDominants(popT)
        self.calculateFronts(popT)
             
    def plotFronts(self,popT):  
      
        f = 0
        #fig = plt.figure()
        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
        while len(popT.fronts[f])!=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            a = [thisfront[i]["thresholdDistance"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]

            #ax1 = fig.add_subplot(111)
            
            plt.scatter(a, b, s=10, color=next(colors), marker="o")
            #ax1.annotate('a',(a,b))
            f +=1
        
        plt.show()    
        
    def plot3DFronts(self,popT):  
          
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        f = 0

        colors = iter(cm.rainbow(np.linspace(0, 1, 15)))
    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
        while len(popT.fronts[f])!=0:
            thisfront = [popT.fitness[i] for i in popT.fronts[f]]

            a = [thisfront[i]["balanceuse"] for i,v in enumerate(thisfront)]
            b = [thisfront[i]["network"] for i,v in enumerate(thisfront)]
            c = [thisfront[i]["reliability"] for i,v in enumerate(thisfront)]


            ax.scatter(a, b, c, color=next(colors), marker="o")
            f +=1
    
        ax.set_xlabel('balanceuse')
        ax.set_ylabel('network')
        ax.set_zlabel('reliability')
    
        plt3d.show()  
                
#******************************************************************************************
#   END NSGA-II Algorithm
#******************************************************************************************


#******************************************************************************************
#   Evolution based on NSGA-II 
#******************************************************************************************


    def generatePopulation(self,popT):
        for i in range(self.populationSize):
            chromosome = {}
        
            for msId in range(0,self.system.numberMicroServices):
                    chromosome[msId] = {"allocationList": [self.rnd.randint(0,self.system.nodenumber-1) for r in xrange(self.rnd.randint(1,min(self.system.nodenumber,10)))] }
            popT.population[i]=chromosome
            #print "[Citizen generation]: Number %i generated**********************" % i
            #chr_fitness = self.calculateFitnessObjectives(chromosome,i)
            #popT.fitness[i]=chr_fitness
            #print "[Fitness calculation]: Calculated for citizen %i **********************" % i
            popT.dominatedBy[i]=set()
            popT.dominatesTo[i]=set()
            popT.fronts[i]=set()
            popT.crowdingDistances[i]=float(0)
            
        self.calculateSolutionsWorkload(popT)
        self.calculatePopulationFitnessObjectives(popT)
        self.fastNonDominatedSort(popT)
#        self.plot3DFronts(popT)
        #self.plotFronts(popT)
        self.calculateCrowdingDistances(popT)

    def tournamentSelection(self,k,popSize):
        selected = sys.maxint 
        for i in range(k):
            selected = min(selected,self.rnd.randint(0,popSize-1))
        return selected
           
    def fatherSelection(self, orderedFathers): #TODO
        i = self.tournamentSelection(2,len(orderedFathers))
        return  orderedFathers[i]["index"]
        
    def evolveToOffspring(self):
        
        offspring = pop.POPULATION(self.populationSize)
        offspring.population = []

        orderedFathers = self.crowdedComparisonOrder(self.populationPt)
        

        #offspring generation

        while len(offspring.population)<self.populationSize:
            father1 = self.fatherSelection(orderedFathers)
            father2 = father1
            while father1 == father2:
                father2 = self.fatherSelection(orderedFathers)
            #print "[Father selection]: Father1: %i **********************" % father1
            #print "[Father selection]: Father1: %i **********************" % father2
            
            self.crossover(self.populationPt.population[father1],self.populationPt.population[father2],offspring.population)
        
        #offspring mutation
        
        for index,children in enumerate(offspring.population):
            if self.rnd.uniform(0,1) < self.mutationProbability:
                self.mutate(children)
                #print "[Offsrping generation]: Children %i MUTATED **********************" % index
            
        #print "[Offsrping generation]: Population GENERATED **********************"  
        
        return offspring

        
    def crowdedComparisonOrder(self,popT):
        valuesToOrder=[]
        for i,v in enumerate(popT.crowdingDistances):
            citizen = {}
            citizen["index"] = i
            citizen["distance"] = v
            citizen["rank"] = 0
            valuesToOrder.append(citizen)
        
        f=0    
        while len(popT.fronts[f])!=0:
            for i,v in enumerate(popT.fronts[f]):
                valuesToOrder[v]["rank"]=f
            f+=1
             
        return sorted(valuesToOrder, key=lambda k: (k["rank"],-k["distance"]))

        
       
    def evolveNGSA2(self):
        
        offspring = pop.POPULATION(self.populationSize)
        offspring.population = []

        offspring = self.evolveToOffspring()
        
        self.calculateSolutionsWorkload(offspring)
        self.calculatePopulationFitnessObjectives(offspring)
        
        populationRt = offspring.populationUnion(self.populationPt,offspring)
        
        self.fastNonDominatedSort(populationRt)
        self.calculateCrowdingDistances(populationRt)
        
        orderedElements = self.crowdedComparisonOrder(populationRt)
        
        finalPopulation = pop.POPULATION(self.populationSize)
        
        for i in range(self.populationSize):
            finalPopulation.population[i] = populationRt.population[orderedElements[i]["index"]]
            finalPopulation.fitness[i] = populationRt.fitness[orderedElements[i]["index"]]
            finalPopulation.nodesUsages[i] = populationRt.nodesUsages[orderedElements[i]["index"]]

        for i,v in enumerate(finalPopulation.fitness):
            finalPopulation.fitness[i]["index"]=i        
        
        #self.populationPt = offspring
        self.populationPt = finalPopulation
        
        
        self.fastNonDominatedSort(self.populationPt)
        self.calculateCrowdingDistances(self.populationPt)
        

        #self.plot3DFronts(self.populationPt)
        #self.plotFronts(self.populationPt)
        
        

 
        
       
        

#******************************************************************************************
#  END Evolution based on NSGA-II 
#******************************************************************************************





#blocksPerFilePerMapReduceJobs1 = np.array([[2,3,1],[5,5,0],[3,4,1],[8,3,1]])
#blocksPerFilePerMapReduceJobs = np.array([2,3,1])
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([5,5,0])))
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([3,4,1])))
#blocksPerFilePerMapReduceJobs = np.vstack((blocksPerFilePerMapReduceJobs,np.array([8,3,1])))

#definition of the files for each MapReduce job. 1:1 jobs:files

#nodenumber = 50
#populationSize = 10
#population = []
#
#for i in range(populationSize):
#    chromosome = {}
#    fileId = 0
#    blockId = 0
#    
#    for (MRjobID,MRjobFileID), value in np.ndenumerate(blocksPerFilePerMapReduceJobs):
#        for blockId in range(value): #iteration of the three files of each mapreducejob
#            replicationFactor = int(round(np.random.normal(3.0, 0.4))) # mean and standard deviation
#            if replicationFactor>nodenumber: #when the block replica is bigger than total node number, is set to the maximum
#                replicationFactor=nodenumber        
#            try:
#                allocation=self.rnd.sample(range(1, nodenumber), replicationFactor) #random selection of the node to place the blocks
#                #selection of the nodes to be read by the tasks of the mapreduce job            
#                readallocation=[]
#                readnode = self.rnd.choice(allocation)
#                allocation.remove(readnode)
#                readallocation.append(readnode)
#            except ValueError:
#                print('Sample size exceeded population size.')
#            chromosome[fileId,blockId] = {"filetype": MRjobFileID % 3 , "wnode":allocation,"rnode":readallocation}
#            blockId+=1
#        fileId+=1
#    population.append(chromosome)
#    
#
#chromosome


#
#for fileId,totalBlock in enumerate(blocksPerFile):
#    for blockId in range(totalBlock):
#        chromosome[fileId,b] = {"wnode":[1,2,3],"rnode":[]}

