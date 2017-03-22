#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 18:02:15 2016

@author: carlos
"""

import matplotlib
matplotlib.use('Agg')
import GA as ga
import random as random
import SYSTEMMODEL as systemmodel
import numpy as np
import pickle
from datetime import datetime
import os
import matplotlib.pyplot as plt 
import math as math      
        

executionId= "k"+datetime.now().strftime('%Y%m%d%H%M%S')


file_path = "./"+executionId

if not os.path.exists(file_path):
    os.makedirs(file_path)
    
calculateReliability = True

if calculateReliability:
    result_string = 'nodes;reqs;apps;'+\
        'thr;clus;rel;net'
    result_string += '\n'    
else:
    result_string = 'nodes;reqs;apps;'+\
        'thr;clus;net'
    result_string += '\n'
    


#for n_number in (20,40,80):
#    for n_reqs in (4,8,10):
#        for n_apps in (2,3,4):

outputtotal = open(file_path+'/kubernetes_data.csv', 'wb')
outputtotal.write(result_string)
outputtotal.flush()    
    
for n_nodes in [150, 200, 250, 300, 350, 400]:
    for n_reqs in [1.0,1.5,2.0]:
        for n_apps in [1,2]:
#for n_nodes in [120]:
#    for n_reqs in [1.0]:
#        for n_apps in [1]:    
            
            system = systemmodel.SYSTEMMODEL()
            system.configurationB(nodes=n_nodes, req=n_reqs, apps=n_apps )
        
            g = ga.GA(system)
            g.reliabilityAwarness = calculateReliability
            g.generatePopulation(g.populationPt)
            
            population = g.populationPt.population[0]
            nodesUsages = g.populationPt.nodesUsages[0]

            for i,v in enumerate(population):
                population[i]['allocationList'] = []

            for i,v in enumerate(nodesUsages):
                v['computationalResources'] = 0.0
            

            for i,v in enumerate(system.serviceTupla):
                v['scaleLevel']= int(math.ceil((v['computationalResources']*v['requestNumber']*system.requestPerApp[v['application']])/v['threshold']))
                v['containerUsage']= v['computationalResources']/v['scaleLevel']        
                for j in range(0,v['scaleLevel']):
                    allocated=False
                    while not allocated:
                        pm = random.randint(0,len(nodesUsages)-1)
                        if (system.nodeFeatures[pm]['capacity']-nodesUsages[pm]['computationalResources'])>system.serviceTupla[i]['containerUsage']:
                            population[i]['allocationList'].append(pm)
                            nodesUsages[pm]['computationalResources'] += system.serviceTupla[i]['containerUsage']
                            allocated=True

            #print population
            
            thr=str(g.calculateThreshold(population))

            clus=str(g.calculateClusterBalanceUse(nodesUsages))
            if g.reliabilityAwarness:
                rel=str(g.calculateFailure(population))
            net=str(g.calculateNetwork(population))         
            
            if g.reliabilityAwarness:
                result_string = str(n_nodes)+";"+str(n_reqs)+";"+str(n_apps)+";"+thr+";"+clus+";"+rel+";"+net
            else:
                result_string = str(n_nodes)+";"+str(n_reqs)+";"+str(n_apps)+";"+thr+";"+clus+";"+";"+net
            
            print result_string
            outputtotal.write(result_string+'\n')
            outputtotal.flush()

outputtotal.close()            
       
    


#    plt.plot(networkDistance['min'])
#    plt.plot(networkDistance['max'])
#    plt.plot(networkDistance['mean'])
#    plt.show()
#    
#    plt.plot(reliability['min'])
#    plt.plot(reliability['max'])
#    plt.plot(reliability['mean'])
#    plt.show()
#    
#    plt.plot(clusterbalanced['min'])
#    plt.plot(clusterbalanced['max'])
#    plt.plot(clusterbalanced['mean'])
#    plt.show()
#    
#    plt.plot(thresholdDistance['min'])
#    plt.plot(thresholdDistance['max'])
#    plt.plot(thresholdDistance['mean'])
#    plt.show()
#    
#    plt.plot(fitness['min'])
#    plt.plot(fitness['max'])
#    plt.plot(fitness['mean'])
#    plt.show()



#            chr_fitness["networkDistance"] = float('inf')    
 

   
    #print "[Offsrping generation]: Generation number %i **********************" % i 

#mutate(g.population[2])


#for key, value in g.population[2].iteritems():
#    print key
#    print value['rnode']
#    print g.population[2][key]['rnode']


     

    