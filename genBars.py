#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 18:02:15 2016

@author: carlos
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import pandas as pd
import random as rand





executionId= 'xxx'


file_path = "./"+executionId
calculateReliability = False
numberofGenerations=300

df = pd.read_csv(file_path+'/execution_data.csv',sep=';')
df2 = pd.read_csv(file_path+'/kubernetes_data.csv',sep=';')


for nodeNumber in [250,300,350,400]:
    for metric in ['fitnodeNumber','fitthresholdDistance','fitclusterbalanced','fitnetworkDistance','fitreliability']:
        figtitleStr = str(nodeNumber) + " physical machines"
    
        if metric=='fitnodeNumber':
            kmetric = 'usednodes'
        if metric=='fitthresholdDistance':
            kmetric = 'thr'
        if metric=='fitclusterbalanced':
            kmetric = 'clus'
        if metric=='fitnetworkDistance':
            kmetric = 'net'
        if metric=='fitreliability':
            kmetric = 'rel'
            
#        if metric=='fitnodeNumber':
#            tmetric = 'min4thrnodeNumber'
#        if metric=='fitthresholdDistance':
#            tmetric = 'min4thrthresholdDistance'
#        if metric=='fitclusterbalanced':
#            tmetric = 'min4thclusterbalanced'
#        if metric=='fitnetworkDistance':
#            tmetric = 'min4thrnetworkDistance'
#        if metric=='fitreliability':
#            tmetric = 'min4thrreliability'

            
        fig = plt.figure()
        fig.suptitle(figtitleStr, fontsize=18)
        ax = fig.add_subplot(111)
        ax.yaxis.set_ticks_position('both')
        df['label'] = df['reqs'].map(str) + "reqs-" + df['apps'].map(str)+'apps'
        df['Kubernetes']=df2[kmetric]

        df['NSGA-II']=df[metric]
        plt.gcf().subplots_adjust(bottom=0.38)
        df[(df['nodes']==nodeNumber)][['NSGA-II','Kubernetes', 'label']].plot(ax=ax,kind='bar', x = 'label', rot=90, figsize=(8,4))
        ax.set_xlabel('Experiment configurations',fontsize=18)
        if metric=='fitnodeNumber':
            ax.set_ylabel('Number of nodes',fontsize=18)
        if metric=='fitthresholdDistance':
            ax.set_ylabel('Threshold Distance',fontsize=18)
            plt.ylim([0,2000])
        if metric=='fitclusterbalanced':
            ax.set_ylabel('Cluster Balanced',fontsize=18)
            plt.ylim([0,0.38])
        if metric=='fitnetworkDistance':
            ax.set_ylabel('Network Distance',fontsize=18) 
            plt.ylim([0,60])
        if metric=='fitreliability':
            ax.set_ylabel('System Failure',fontsize=18) 
            plt.ylim([0,0.025])            
        #ax.set_title(figtitleStr, fontsize=18)
    #    plt.show()
        plt.grid()
        fig.savefig(file_path+'/'+metric+str(nodeNumber)+'.eps',format='eps')
    
        plt.close(fig)
    
    

    
    
    
#df[(df['nodes']==100) & (df['apps']==1)][['fitnodeNumber']].plot(kind='bar', use_index=False, xticks = df['reqs'])
    

  



     

    