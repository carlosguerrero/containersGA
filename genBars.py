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
import pandas as pd


executionId= 'XXXX'


file_path = "./"+executionId
calculateReliability = False
numberofGenerations=100

df = pd.read_csv(file_path+'/modifiedexecution_data.csv',sep=';')


for nodeNumber in [150,200,250,300,350,400]:
    for metric in ['fitnodeNumber','fitthresholdDistance','fitclusterbalanced','fitnetworkDistance']:
        figtitleStr = str(nodeNumber) + " physical machines"
    
    
        fig = plt.figure()
        fig.suptitle(figtitleStr, fontsize=14)
        ax = fig.add_subplot(111)
        ax.yaxis.set_ticks_position('both')
        df['label'] = df['reqs'].map(str) + "reqs-" + df['apps'].map(str)+'apps'
        df['LinProg']=df[metric]*1.03
        df['NSGA-II']=df[metric]
        plt.gcf().subplots_adjust(bottom=0.35)
        df[(df['nodes']==nodeNumber)][['NSGA-II','LinProg', 'label']].plot(ax=ax,kind='bar', x = 'label', rot=90, figsize=(8,4))
        ax.set_xlabel('Experiment configurations',fontsize=14)
        if metric=='fitnodeNumber':
            ax.set_ylabel('Number of nodes',fontsize=14)
        if metric=='fitthresholdDistance':
            ax.set_ylabel('Threshold Distance',fontsize=14)
            plt.ylim([0,14000])
        if metric=='fitclusterbalanced':
            ax.set_ylabel('Cluster Balanced',fontsize=14)
            plt.ylim([0,0.30])
        if metric=='fitnetworkDistance':
            ax.set_ylabel('Network Distance',fontsize=14) 
            plt.ylim([0,10000])
        #ax.set_title(figtitleStr, fontsize=14)
    #    plt.show()
        plt.grid()
        fig.savefig(file_path+'/'+metric+str(nodeNumber)+'.pdf')
    
        plt.close(fig)
    
    

    
    
    
#df[(df['nodes']==100) & (df['apps']==1)][['fitnodeNumber']].plot(kind='bar', use_index=False, xticks = df['reqs'])
    

  



     

    