#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:56:02 2017

@author: carlos
"""
import copy
import random as random
import math as math

class SYSTEMMODEL:
    
    def __init__(self):
        
        self.numberMicroServices = 0
        self.nodenumber = 0
        self.requestPerApp = []
        self.serviceTupla= []
        self.plantillasMaquinas = []
        self.nodeFeatures = []
        self.cpdNetwork = []
        self.rnd = random.Random()
        self.rnd.seed(100)
        
    def normalizeConfiguration(self):
        for i,v in enumerate(self.serviceTupla):
            self.serviceTupla[i]['scaleLevel']= int(math.ceil((self.serviceTupla[i]['computationalResources']*self.serviceTupla[i]['requestNumber']*self.requestPerApp[self.serviceTupla[i]['application']])/self.serviceTupla[i]['threshold']))
            self.serviceTupla[i]['containerUsage']= self.serviceTupla[i]['computationalResources']/self.serviceTupla[i]['scaleLevel'] 

        
    def configurationA(self,nodes, apps, req):

        self.nodenumber = nodes
        self.requestPerApp = []
        self.serviceTupla= []
        for i in range(apps):
            self.requestPerApp.append(4.0*float(req))

            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [0]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [1,0]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [2]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [2,0]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 0.01, "computationalResources": 0.2, "threshold": 0.04, "failrate": 0.08, "consumeServices": [2,3,4]})

        self.numberMicroServices = len(self.serviceTupla)

        #definimos las "plantillas" de máquinas
        self.plantillasMaquinas = []
        self.plantillasMaquinas.append({"name": "tinny", "capacity" : 10.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "small", "capacity" : 20.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "medium", "capacity" : 40.0, "failrate": 0.01})
        self.plantillasMaquinas.append({"name": "big", "capacity" : 80.0, "failrate": 0.01})
        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        #igual número de máquinas de cada tipo
        self.nodeFeatures = []
        for n in range(self.nodenumber):
            self.nodeFeatures.append(self.plantillasMaquinas[n % len(self.plantillasMaquinas)])
            #self.nodeFeatures.append(self.plantillasMaquinas[self.rnd.randint(0,len(self.plantillasMaquinas)-1)])
            
       

        #******************************************************************************************
        #   Definición de la red del CPD
        #******************************************************************************************



        self.cpdNetwork = [[0 for x in range(self.nodenumber)] for y in range(self.nodenumber)]
        
        #las máquinas se distribuyen en dos racks.
                            
        for r in range(0,self.nodenumber/2):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0            
        for r in range(0,self.nodenumber/2):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0   
        #******************************************************************************************
        #   END Definición de la red del CPD
        #******************************************************************************************
        
        #******************************************************************************************
        #   BEGIN cálculo del escalado ajustado a threshold
        #******************************************************************************************



        self.normalizeConfiguration()        
                                        
        #******************************************************************************************
        #   END cálculo del escalado ajustado a threshold
        #******************************************************************************************
 


           
            
    def configurationB(self,nodes, apps, req):

        self.nodenumber = nodes
        self.requestPerApp = []
        self.serviceTupla= []
        for i in range(apps):
            self.requestPerApp.append(4.0*float(req))

            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":   0.1 , "threshold":   1.0 , "failrate": 0.04   , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  1.8 , "computationalResources":  11.7 , "threshold":  25.0 , "failrate": 0.02   , "consumeServices": [12]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  20.0 , "threshold": 200.0 , "failrate": 0.02   , "consumeServices": [1,3]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  1.4 , "computationalResources":   0.1 , "threshold":  10.0 , "failrate": 0.0002 , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  2.3 , "computationalResources":  27.1 , "threshold":  80.0 , "failrate": 0.02   , "consumeServices": [2,3,9,10,11]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  0.8 , "computationalResources":   2.8 , "threshold":  30.0 , "failrate": 0.0001 , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" : 15.1 , "computationalResources":   3.8 , "threshold":  50.0 , "failrate": 0.003  , "consumeServices": [4,5,8]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 15.1 , "computationalResources":   0.5 , "threshold":  10.0 , "failrate": 0.0001 , "consumeServices": [6]})
            self.serviceTupla.append({"application" : i, "requestNumber" : 12.0 , "computationalResources":   0.2 , "threshold":   3.0 , "failrate": 0.0006 , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  41.3 , "threshold": 100.0 , "failrate": 0.02   , "consumeServices": [11]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  0.1 , "computationalResources":  45.1 , "threshold": 100.0 , "failrate": 0.003  , "consumeServices": [11]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  26.3 , "threshold":  80.0 , "failrate": 0.04   , "consumeServices": []})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":   4.0 , "threshold":  40.0 , "failrate": 0.0006 , "consumeServices": [0,2]})
            self.serviceTupla.append({"application" : i, "requestNumber" :  3.2 , "computationalResources":  13.2 , "threshold": 100.0 , "failrate": 0.0003 , "consumeServices": []})

        self.numberMicroServices = len(self.serviceTupla)

        #definimos las "plantillas" de máquinas
        self.plantillasMaquinas = []
        self.plantillasMaquinas.append({"name": "tinny", "capacity" : 100.0, "failrate": 0.025})
        self.plantillasMaquinas.append({"name": "small", "capacity" : 200.0, "failrate": 0.025})
        self.plantillasMaquinas.append({"name": "medium", "capacity" : 400.0, "failrate": 0.025})
        self.plantillasMaquinas.append({"name": "big", "capacity" : 800.0, "failrate": 0.025})
        
        #asignamos un tipo/plantilla de máquina a cada uno de los nodos del sistema
        #igual número de máquinas de cada tipo
        self.nodeFeatures = []
        for n in range(self.nodenumber):
            self.nodeFeatures.append(self.plantillasMaquinas[n % len(self.plantillasMaquinas)])
            #self.nodeFeatures.append(self.plantillasMaquinas[self.rnd.randint(0,len(self.plantillasMaquinas)-1)])

            
            
        #******************************************************************************************
        #   Definición de la red del CPD
        #******************************************************************************************
        


        self.cpdNetwork = [[0 for x in range(self.nodenumber)] for y in range(self.nodenumber)]
        
        #las máquinas se distribuyen en dos racks.
                            
        for r in range(0,self.nodenumber/2):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0            
        for r in range(0,self.nodenumber/2):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(0,self.nodenumber/2):
                self.cpdNetwork[r][s]=4.0
                self.cpdNetwork[s][r]=4.0     
        for r in range(self.nodenumber/2,self.nodenumber):
            for s in range(self.nodenumber/2,self.nodenumber):
                self.cpdNetwork[r][s]=1.0
                self.cpdNetwork[s][r]=1.0        
        #******************************************************************************************
        #   END Definición de la red del CPD
        #******************************************************************************************
        
        #******************************************************************************************
        #   BEGIN cálculo del escalado ajustado a threshold
        #******************************************************************************************
        


        self.normalizeConfiguration()   
                            

        #******************************************************************************************
        #   END cálculo del escalado ajustado a threshold
        #******************************************************************************************
        

   
