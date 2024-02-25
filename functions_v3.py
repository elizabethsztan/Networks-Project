#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:04:00 2023

FUNCTIONS v3 (cleaner)

@author: liz
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx
import scipy.stats as stats
import scipy.special as spec

color_cycler =['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

marker_cycler = ['o', 'x', 'v', 's', '*', '+']

params = {
    'axes.labelsize': 23,
    'font.size': 23,
    'legend.fontsize': 20,
    'figure.figsize': [10,8],
    'xtick.labelsize': 23,
    'ytick.labelsize': 23
    }
plt.rcParams.update(params)

M_array = [4,8,16,32,64,128,256]
N_array = [100, 1000, 10000, 100000, 1000000]

def get_uncertainties (covariance_matrix):
    uncertainties = []
    for i in range (len(covariance_matrix)):
        uncertainties.append(covariance_matrix[i][i])
    return uncertainties

def make_starter_network_edges(m):
    nodes = []
    for i in range(m+1):
        for j in range (m):
            nodes.append(i)
    return nodes

def unpack_npz(file, integer = False):
    unpacked = []
    if integer == False:
        for arr in file:
            unpacked.append(file[arr])
    if integer == True:
        for arr in file:
            unpacked.append(file[arr].astype(int))
    return unpacked

def theoretical_k_dist_PA (m, k_array, cum = False):
    k_uniques, y = logbin(k_array.astype(int))
    pk = []
    for k in k_uniques:
        pk.append((2*m*(m+1))/((k)*(k+1)*(k+2)))
    
    if cum == True:
        pk=np.cumsum(pk)
        
    return k_uniques, pk

def find_theoretical_k1_PA(N,m, mod = False):
    if mod == False:
        return (-1+np.sqrt(1+4*N*m*(m+1)))/2
    if mod == True:
        return m*np.sqrt(N/(m+1))


def find_theoretical_pk_PA(k_array,m):
    pk=[]
    for k in k_array:
        pk.append((2*m*(m+1))/((k)*(k+1)*(k+2)))
    return pk

def theoretical_k_dist_RA (m, k_array, cum = False): 
    k_uniques, y = logbin(k_array.astype(int))
    log_pk = []
    for k in k_uniques:
        log_pk.append((k-m)*np.log(m)-(1+k-m)*np.log(1+m))
    
    pk = np.exp(log_pk)
    
    if cum == True: 
        pk=np.cumsum(pk)
        
    return k_uniques, pk

def find_theoretical_k1_RA(N,m, mod = False):
    if mod == False:
        return m - (np.log(N)/(np.log(m)-np.log(m+1)))
    if mod == True:
        return m*(1+np.log(N/(m+1)))

def find_theoretical_pk_RA(k_array,m):
    log_pk=[]
    for k in k_array:
        log_pk.append((k-m)*np.log(m)-(1+k-m)*np.log(1+m))
    pk = np.exp(log_pk)
    return pk

def theoretical_k_dist_EV(m,k_array, cum = False):
    r = int(m/3)
    k_uniques, y = logbin(k_array.astype(int))
    pk = []
    for k in k_uniques:
        pk.append((2*r*m-r**2)/(m+2*r*m-r**2)*spec.gamma(1+m/(m-r)) / spec.beta(m*r/(m-r)+r+1, m/(m-r))*np.exp(spec.gammaln(k+m*r/(m-r))-spec.gammaln(k+1+m*r/(m-r)+m/(m-r))))
    
    if cum == True:
        pk = np.cumsum(pk)
    
    return k_uniques, pk

def find_theoretical_k1_EV (N, m):
    r=m/3
    return (r*m/(m-r)+m)*((N/(m+1))**((m-r)/m))-r*m/(m-r)


def find_theoretical_pk_EV(k, m, cdf = False):
    r = int(m/3)
    pk = (2*r*m-r**2)/(m+2*r*m-r**2)*spec.gamma(1+m/(m-r)) / spec.beta(m*r/(m-r)+r+1, m/(m-r))*np.exp(spec.gammaln(k+m*r/(m-r))-spec.gammaln(k+1+m*r/(m-r)+m/(m-r)))
    if cdf == False:
        return pk

    if cdf == True:
        return np.cumsum(pk)

