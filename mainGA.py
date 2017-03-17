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

def calculateServiceNumber(solution):
    mylen=0
    for i in solution:
        mylen += len(solution[i]['allocationList'])
    return mylen
    
def calculateNodeNumber(solution):
    nodenum=0
    for i in solution:
        if i['computationalResources'] > 0.0:
            nodenum +=1
    return nodenum

def generarGraficas(file_path,paretoResults, n_number, n_reqs, n_apps, numberofGenerations):
    

    thresholdDistance={}
    clusterbalanced={}
    if g.reliabilityAwarness:
        reliability={}
    networkDistance={}
    fitness={}
    serviceNumber={}
    nodeNumber={}
    
    thresholdDistance['min'] = []
    thresholdDistance['max'] = []
    thresholdDistance['mean'] = []
    thresholdDistance['sfit'] = []
    clusterbalanced['min'] = []
    clusterbalanced['max'] = []
    clusterbalanced['mean'] = []
    clusterbalanced['sfit'] = []
    if g.reliabilityAwarness:
        reliability['min'] = []
        reliability['max'] = []
        reliability['mean'] = []
        reliability['sfit'] = []
    networkDistance['min'] = []
    networkDistance['max'] = []
    networkDistance['mean'] = []
    networkDistance['sfit'] = []
    fitness['min'] = []
    fitness['max'] = []
    fitness['mean'] = []
   
    serviceNumber['min'] = []
    serviceNumber['max'] = []
    serviceNumber['mean'] = []
    serviceNumber['sfit'] = []    
    
    nodeNumber['min'] = []
    nodeNumber['max'] = []
    nodeNumber['mean'] = []
    nodeNumber['sfit'] = []  


    netDiff = 1.0
    thrDiff = 1.0
    relDiff = 1.0
    cluDiff = 1.0      
    
    for paretoGeneration in paretoResults:
        
        seqserv = [calculateServiceNumber(x) for x in paretoGeneration.population if len(x)>0]
        smin = min(seqserv)
        smax = max(seqserv)
        serviceNumber['min'].append(smin)
        serviceNumber['max'].append(smax)
        serviceNumber['mean'].append(np.mean(seqserv))                   
        
        seqnode = [calculateNodeNumber(x) for x in paretoGeneration.nodesUsages if len(x)>0]
        pmin = min(seqnode)
        pmax = max(seqnode)
        nodeNumber['min'].append(pmin)
        nodeNumber['max'].append(pmax)
        nodeNumber['mean'].append(np.mean(seqnode))                   

        
        seqthr = [x['thresholdDistance'] for x in paretoGeneration.fitness if len(x)>0]
    
        tmin = min(seqthr)
        tmax = max(seqthr)
        thresholdDistance['min'].append(tmin)
        thresholdDistance['max'].append(tmax)
        thresholdDistance['mean'].append(np.mean(seqthr))

        
        seqclus = [x['clusterbalanced'] for x in paretoGeneration.fitness if len(x)>0]
        
        cmin = min(seqclus)
        cmax = max(seqclus)
        clusterbalanced['min'].append(cmin)
        clusterbalanced['max'].append(cmax)
        clusterbalanced['mean'].append(np.mean(seqclus))
      
        if g.reliabilityAwarness:
            seqrel = [x['reliability'] for x in paretoGeneration.fitness if len(x)>0]
        
            rmin = min(seqrel)
            rmax = max(seqrel)
            reliability['min'].append(rmin)
            reliability['max'].append(rmax)
            reliability['mean'].append(np.mean(seqrel))
      
    
        seqnet = [x['networkDistance'] for x in paretoGeneration.fitness if len(x)>0]
        
        nmin = min(seqnet)
        nmax = max(seqnet)
        networkDistance['min'].append(nmin)
        networkDistance['max'].append(nmax)
        networkDistance['mean'].append(np.mean(seqnet))
      
        if (nmax - nmin) > 0:
            netDiff = nmax - nmin
        if (tmax - tmin) > 0:
            thrDiff = tmax - tmin
        if g.reliabilityAwarness:
            if (rmax - rmin) > 0:
                relDiff = rmax - rmin
        if (cmax - cmin) > 0:
            cluDiff = cmax - cmin
            
        if g.reliabilityAwarness:
            seqfit = [ ( (x['thresholdDistance']/(thrDiff))*0.25 + (x['clusterbalanced']/(cluDiff))*0.25 + (x['reliability']/(relDiff))*0.25 + (x['networkDistance']/(netDiff))*0.25 )  for x in paretoGeneration.fitness if len(x)>0]
        else:
            seqfit = [ ( (x['thresholdDistance']/(thrDiff))*(1.0/3.0) + (x['clusterbalanced']/(cluDiff))*(1.0/3.0) + (x['networkDistance']/(netDiff))*(1.0/3.0) )  for x in paretoGeneration.fitness if len(x)>0]
        fitness['min'].append(min(seqfit))
        fitness['max'].append(max(seqfit))
        fitness['mean'].append(np.mean(seqfit))
        
        smallerFitIndex = seqfit.index(min(seqfit))

        serviceNumber['sfit'].append(seqserv[smallerFitIndex])   
        nodeNumber['sfit'].append(seqnode[smallerFitIndex])          
        thresholdDistance['sfit'].append(seqthr[smallerFitIndex])        
        clusterbalanced['sfit'].append(seqclus[smallerFitIndex])
        if g.reliabilityAwarness:
            reliability['sfit'].append(seqrel[smallerFitIndex])  
        networkDistance['sfit'].append(seqnet[smallerFitIndex])      
        

    figtitleStr = str(n_number)+' nodes, '+str(n_apps)+' apps, '+str(n_reqs)+' app requests'


#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Services number', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(serviceNumber['max'], label='max')
    ax.plot(serviceNumber['mean'], label='mean')
    ax.plot(serviceNumber['min'], label='min')
    ax.plot(serviceNumber['sfit'], label='fitness')    
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'services.pdf')
    plt.close(fig)
    

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Nodes number', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(nodeNumber['max'], label='max')
    ax.plot(nodeNumber['mean'], label='mean')
    ax.plot(nodeNumber['min'], label='min')
    ax.plot(nodeNumber['sfit'], label='fitness')    
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'nodes.pdf')
    plt.close(fig)
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Network Distance', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(networkDistance['max'], label='max')
    ax.plot(networkDistance['mean'], label='mean')
    ax.plot(networkDistance['min'], label='min')
    ax.plot(networkDistance['sfit'], label='fitness')    
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'net.pdf')
    plt.close(fig)
    

    if g.reliabilityAwarness:    
    #ejemplo sacado de http://matplotlib.org/users/text_intro.html    
        fig = plt.figure()
    #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
        fig.suptitle(figtitleStr, fontsize=14)
        ax = fig.add_subplot(111)
    #    fig.subplots_adjust(top=0.85)
    #    ax.set_title('axes title')
        ax.set_xlabel('Generations', fontsize=14)
        ax.set_ylabel('System Failure', fontsize=14)
        plt.gcf().subplots_adjust(left=0.15)
        ax.plot(reliability['max'], label='max')
        ax.plot(reliability['mean'], label='mean')
        ax.plot(reliability['min'], label='min')
        ax.plot(reliability['sfit'], label='fitness')      
        #    plt.legend(loc="upper left") 
    #upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
        plt.legend()
    #    plt.show()
        fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'reliability.pdf')
        plt.close(fig)
    

    
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Cluster Balanced', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(clusterbalanced['max'], label='max')
    ax.plot(clusterbalanced['mean'], label='mean')
    ax.plot(clusterbalanced['min'], label='min')
    ax.plot(clusterbalanced['sfit'], label='fitness')      
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'cluster.pdf')
    plt.close(fig)
    

    
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Threshold Distance', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(thresholdDistance['max'], label='max')
    ax.plot(thresholdDistance['mean'], label='mean')
    ax.plot(thresholdDistance['min'], label='min')
    ax.plot(thresholdDistance['sfit'], label='fitness')     
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'thr.pdf')
    plt.close(fig)
    

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Fitness', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(fitness['max'], label='max')
    ax.plot(fitness['mean'], label='mean')
    ax.plot(fitness['min'], label='min')
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'fit.pdf')
    plt.close(fig)    

#########SIN LOS MÁXIMOS!!!!

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Services number', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(serviceNumber['mean'], label='mean')
    ax.plot(serviceNumber['min'], label='min')
    ax.plot(serviceNumber['sfit'], label='fitness')    
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/minnodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'services.pdf')
    plt.close(fig)
    

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Nodes number', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(nodeNumber['mean'], label='mean')
    ax.plot(nodeNumber['min'], label='min')
    ax.plot(nodeNumber['sfit'], label='fitness')    
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/minnodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'nodes.pdf')
    plt.close(fig)
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Network Distance', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(networkDistance['mean'], label='mean')
    ax.plot(networkDistance['min'], label='min')
    ax.plot(networkDistance['sfit'], label='fitness')    
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/minnodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'net.pdf')
    plt.close(fig)
    

    
    
    if g.reliabilityAwarness:
    #ejemplo sacado de http://matplotlib.org/users/text_intro.html    
        fig = plt.figure()
    #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
        fig.suptitle(figtitleStr, fontsize=14)
        ax = fig.add_subplot(111)
    #    fig.subplots_adjust(top=0.85)
    #    ax.set_title('axes title')
        ax.set_xlabel('Generations', fontsize=14)
        ax.set_ylabel('System Failure', fontsize=14)
        plt.gcf().subplots_adjust(left=0.15)
        ax.plot(reliability['mean'], label='mean')
        ax.plot(reliability['min'], label='min')
        ax.plot(reliability['sfit'], label='fitness')      
        #    plt.legend(loc="upper left") 
    #upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
        plt.legend()
    #    plt.show()
        fig.savefig(file_path+'/minnodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'reliability.pdf')
        plt.close(fig)
        

    
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Cluster Balanced', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(clusterbalanced['mean'], label='mean')
    ax.plot(clusterbalanced['min'], label='min')
    ax.plot(clusterbalanced['sfit'], label='fitness')      
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/minnodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'cluster.pdf')
    plt.close(fig)
    

    
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Threshold Distance', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(thresholdDistance['mean'], label='mean')
    ax.plot(thresholdDistance['min'], label='min')
    ax.plot(thresholdDistance['sfit'], label='fitness')     
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/minnodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'thr.pdf')
    plt.close(fig)
    

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Fitness', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(fitness['mean'], label='mean')
    ax.plot(fitness['min'], label='min')
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/minnodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'fit.pdf')
    plt.close(fig)    

#########SIN LOS FITS



#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Services number', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(serviceNumber['mean'], label='mean')
    ax.plot(serviceNumber['min'], label='min')  
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/min2nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'services.pdf')
    plt.close(fig)
    

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Nodes number', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(nodeNumber['mean'], label='mean')
    ax.plot(nodeNumber['min'], label='min')   
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/min2nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'nodes.pdf')
    plt.close(fig)
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Network Distance', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(networkDistance['mean'], label='mean')
    ax.plot(networkDistance['min'], label='min') 
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/min2nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'net.pdf')
    plt.close(fig)
    

    
    if g.reliabilityAwarness:
    #ejemplo sacado de http://matplotlib.org/users/text_intro.html    
        fig = plt.figure()
    #    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
        fig.suptitle(figtitleStr, fontsize=14)
        ax = fig.add_subplot(111)
    #    fig.subplots_adjust(top=0.85)
    #    ax.set_title('axes title')
        ax.set_xlabel('Generations', fontsize=14)
        ax.set_ylabel('System Failure', fontsize=14)
        plt.gcf().subplots_adjust(left=0.15)
        ax.plot(reliability['mean'], label='mean')
        ax.plot(reliability['min'], label='min')
        
        #    plt.legend(loc="upper left") 
    #upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
        plt.legend()
    #    plt.show()
        fig.savefig(file_path+'/min2nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'reliability.pdf')
        plt.close(fig)
        
    
        
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Cluster Balanced', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(clusterbalanced['mean'], label='mean')
    ax.plot(clusterbalanced['min'], label='min')   
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/min2nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'cluster.pdf')
    plt.close(fig)
    

    
    

#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Threshold Distance', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(thresholdDistance['mean'], label='mean')
    ax.plot(thresholdDistance['min'], label='min')    
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/min2nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'thr.pdf')
    plt.close(fig)
    

    
#ejemplo sacado de http://matplotlib.org/users/text_intro.html    
    fig = plt.figure()
#    fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    fig.suptitle(figtitleStr, fontsize=14)
    ax = fig.add_subplot(111)
#    fig.subplots_adjust(top=0.85)
#    ax.set_title('axes title')
    ax.set_xlabel('Generations', fontsize=14)
    ax.set_ylabel('Fitness', fontsize=14)
    plt.gcf().subplots_adjust(left=0.15)
    ax.plot(fitness['mean'], label='mean')
    ax.plot(fitness['min'], label='min')
    #    plt.legend(loc="upper left") 
#upper, arriba    lower, abajo   center, centro    left, izquierda y    right, derecha
    plt.legend()
#    plt.show()
    fig.savefig(file_path+'/min2nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'fit.pdf')
    plt.close(fig)    



    if g.reliabilityAwarness:

 
        for i in xrange(0,numberofGenerations,10):
            
            fig = plt.figure()
            fig.suptitle("Generation "+str(i), fontsize=14)
            ax.set_title(figtitleStr)
            ax = fig.add_subplot(111)
            ax.set_xlabel('Threshold Distance', fontsize=14)
            ax.set_ylabel('System Failure', fontsize=14)
            a = [v["thresholdDistance"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
            b = [v["reliability"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
    
                #ax1 = fig.add_subplot(111)
            plt.gcf().subplots_adjust(left=0.15)    
            plt.scatter(a, b, s=10, marker="o")
            fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'thr-reli-g'+str(i)+'.pdf')
                #ax1.annotate('a',(a,b))
    
            
            plt.close(fig)    
    
        for i in xrange(0,numberofGenerations,10):
            
            fig = plt.figure()
            fig.suptitle("Generation "+str(i), fontsize=14)
            #fig,ax = plt.subplots()
            ax.set_title(figtitleStr)
            ax = fig.add_subplot(111)
            ax.set_xlabel('Cluster Balanced', fontsize=14)
            ax.set_ylabel('Network Distance', fontsize=14)
            a = [v["clusterbalanced"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
            b = [v["networkDistance"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
    
                #ax1 = fig.add_subplot(111)
            #plt.tight_layout()    
            plt.gcf().subplots_adjust(left=0.15)
            plt.scatter(a, b, s=10, marker="o")
            fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'clus-net-g'+str(i)+'.pdf')
                #ax1.annotate('a',(a,b))
    
            
            plt.close(fig)    
            
    else:
 
        for i in xrange(0,numberofGenerations,10):
            
            fig = plt.figure()
            fig.suptitle("Generation "+str(i), fontsize=14)
            ax.set_title(figtitleStr)
            ax = fig.add_subplot(111)
            ax.set_xlabel('Threshold Distance', fontsize=14)
            ax.set_ylabel('Cluster Balanced', fontsize=14)
            a = [v["thresholdDistance"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
            b = [v["clusterbalanced"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
    
                #ax1 = fig.add_subplot(111)
            plt.gcf().subplots_adjust(left=0.15)    
            plt.scatter(a, b, s=10, marker="o")
            fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'thr-clus-g'+str(i)+'.pdf')
                #ax1.annotate('a',(a,b))
    
            
            plt.close(fig)    
    
        for i in xrange(0,numberofGenerations,10):
            
            fig = plt.figure()
            fig.suptitle("Generation "+str(i), fontsize=14)
            #fig,ax = plt.subplots()
            ax.set_title(figtitleStr)
            ax = fig.add_subplot(111)
            ax.set_xlabel('Cluster Balanced', fontsize=14)
            ax.set_ylabel('Network Distance', fontsize=14)
            a = [v["clusterbalanced"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
            b = [v["networkDistance"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
    
                #ax1 = fig.add_subplot(111)
            #plt.tight_layout()    
            plt.gcf().subplots_adjust(left=0.15)
            plt.scatter(a, b, s=10, marker="o")
            fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'clus-net-g'+str(i)+'.pdf')
                #ax1.annotate('a',(a,b))
    
            
            plt.close(fig)    
    
        for i in xrange(0,numberofGenerations,10):
            
            fig = plt.figure()
            fig.suptitle("Generation "+str(i), fontsize=14)
            #fig,ax = plt.subplots()
            ax.set_title(figtitleStr)
            ax = fig.add_subplot(111)
            ax.set_xlabel('Threshold Distance', fontsize=14)
            ax.set_ylabel('Network Distance', fontsize=14)
            a = [v["thresholdDistance"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
            b = [v["networkDistance"] for f,v in enumerate(paretoResults[i].fitness) if len(v) > 0]
    
                #ax1 = fig.add_subplot(111)
            #plt.tight_layout()    
            plt.gcf().subplots_adjust(left=0.15)
            plt.scatter(a, b, s=10, marker="o")
            fig.savefig(file_path+'/nodes'+str(n_number)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'thr-net-g'+str(i)+'.pdf')
                #ax1.annotate('a',(a,b))
    
            
            plt.close(fig)    


    lastR = len(thresholdDistance['min'])-1


    strToreturn=str(n_number)+';'+ \
        str(n_reqs)+';'+ \
        str(n_apps)+';'+ \
        str(networkDistance['max'][lastR])+';'+ \
        str(networkDistance['mean'][lastR])+';'+ \
        str(networkDistance['min'][lastR])+';'+ \
        str(networkDistance['sfit'][lastR])+';'+ \
        str(clusterbalanced['max'][lastR])+';'+ \
        str(clusterbalanced['mean'][lastR])+';'+ \
        str(clusterbalanced['min'][lastR])+';'+ \
        str(clusterbalanced['sfit'][lastR])+';'+ \
        str(thresholdDistance['max'][lastR])+';'+ \
        str(thresholdDistance['mean'][lastR])+';'+ \
        str(thresholdDistance['min'][lastR])+';'+ \
        str(thresholdDistance['sfit'][lastR])+';'+ \
        str(fitness['max'][lastR])+';'+ \
        str(fitness['mean'][lastR])+';'+ \
        str(fitness['min'][lastR])+';'+ \
        str(nodeNumber['max'][lastR])+';'+ \
        str(nodeNumber['mean'][lastR])+';'+ \
        str(nodeNumber['min'][lastR])+';'+ \
        str(nodeNumber['sfit'][lastR])+';'+ \
        str(serviceNumber['max'][lastR])+';'+ \
        str(serviceNumber['mean'][lastR])+';'+ \
        str(serviceNumber['min'][lastR])+';'+ \
        str(serviceNumber['sfit'][lastR])
        
    return strToreturn        
        

executionId= datetime.now().strftime('%Y%m%d%H%M%S')


file_path = "./"+executionId

if not os.path.exists(file_path):
    os.makedirs(file_path)
    
calculateReliability = True

if calculateReliability:
    result_string = 'nodes;reqs;apps;'+\
        'maxnetworkDistance;meannetworkDistance;minnetworkDistance;fitnetworkDistance;'+\
        'maxclusterbalanced;meanclusterbalanced;minclusterbalanced;fitclusterbalanced;'+\
        'maxreliability;meanreliability;minreliability;fitreliability;'+\
        'maxthresholdDistance;meanthresholdDistance;minthresholdDistance;fitthresholdDistance;'+\
        'maxfitness;meanfitness;minfitness;'+\
        'maxnodeNumber;meannodeNumber;minnodeNumber;fitnodeNumber;'+\
        'maxserviceNumber;measerviceNumber;minserviceNumber;fitserviceNumber'
    result_string += '\n'    
else:
    result_string = 'nodes;reqs;apps;'+\
        'maxnetworkDistance;meannetworkDistance;minnetworkDistance;fitnetworkDistance;'+\
        'maxclusterbalanced;meanclusterbalanced;minclusterbalanced;fitclusterbalanced;'+\
        'maxthresholdDistance;meanthresholdDistance;minthresholdDistance;fitthresholdDistance;'+\
        'maxfitness;meanfitness;minfitness;'+\
        'maxnodeNumber;meannodeNumber;minnodeNumber;fitnodeNumber;'+\
        'maxserviceNumber;measerviceNumber;minserviceNumber;fitserviceNumber'
    result_string += '\n'
    
numberofGenerations = 100


#for n_number in (20,40,80):
#    for n_reqs in (4,8,10):
#        for n_apps in (2,3,4):

outputlog = open(file_path+'/log.txt', 'wb')
outputtotal = open(file_path+'/execution_data.csv', 'wb')
outputtotal.write(result_string)
outputtotal.flush()    
    
for n_nodes in [150, 200, 250, 300, 350, 400]:
    for n_reqs in [1.0,1.5,2.0,3.0,4.0]:
        for n_apps in [1,2,4]:
#for n_nodes in [120]:
#    for n_reqs in [1.0]:
#        for n_apps in [1]:    
            
            system = systemmodel.SYSTEMMODEL()
            system.configurationB(nodes=n_nodes, req=n_reqs, apps=n_apps )
        
            g = ga.GA(system)
            g.scaleLevel='SOFT'
            g.reliabilityAwarness = calculateReliability
            g.generatePopulation(g.populationPt)
            paretoResults = []
            
            paretoResults = []

            paretoGeneration=g.populationPt.paretoExport()
            paretoResults.append(paretoGeneration)
            
            for i in range(numberofGenerations):
                g.evolveNGSA2()
                paretoGeneration=g.populationPt.paretoExport()
                paretoResults.append(paretoGeneration)
                logstr = '[Generation number '+str(i)+' for nodes'+str(n_nodes)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+']'
                print logstr
                outputlog.write(logstr+'\n')
                outputlog.flush()
                           
            output = open(file_path+'/nodes'+str(n_nodes)+'reqs'+str(n_reqs)+'apps'+str(n_apps)+'data.pkl', 'wb')
            pickle.dump(paretoResults, output)
            output.close()  
            
        #    pkl_file = open(file_path+'data.pkl','rb')  
        #    paretoResults = pickle.load(pkl_file)
        #    pkl_file.close()
        
            result_string = generarGraficas(file_path,paretoResults, n_nodes, n_reqs, n_apps,numberofGenerations)
            result_string += '\n'
            outputtotal.write(result_string)
            outputtotal.flush()

outputlog.close()
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


     

    