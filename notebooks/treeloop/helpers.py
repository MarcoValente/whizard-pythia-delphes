import numpy as np
from treeloop import configtree as ct
import logging as log

def getHistErrors(edges,v,w):
    sumw2 = np.zeros(len(edges)-1)
    for i in range(len(edges)-1): 
        iv = np.where((v >= edges[i]) & (v < edges[i+1]))[0]
        sumw2[i] = np.sum(w[iv] ** 2) if len(w[iv])>0 else 0.
    return np.sqrt(sumw2)

def getLumi(filename,lumi_dict=ct.lumi_periods):
    lumi = 1.0
    for lumi_key in lumi_dict.keys(): 
        if lumi_key in filename or lumi_key.replace('mc','MC') in filename:
            lumi = lumi_dict[lumi_key]
            break
    return lumi

def getLuminosities(file_list):
    lumis=[]
    for filename in file_list: 
        lumis+=[getLumi(filename)]
    return lumis

def getTotalLumi(lumis=ct.lumi_periods.values()):
    tot_lumi=0.
    for lumi in lumis: tot_lumi+=lumi
    return tot_lumi


def addToDict(name,variable,dicti):
    variable.__name__=name
    dicti.update({name:variable})