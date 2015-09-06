# -*- coding: utf-8 -*-
"""
Created on Sun 2014/12/14 11:08:00
@author mbocamazo
Run genetic algorithm for tadpole gait optimization
"""
import random
import math
import csv
import os
import numpy as np

"""
some initial params (tho look in 'learndata.csv' for 4 initials)
float freq = 2;
float amp0 = 60;
float amp1 = 80;
float amp2 = 80;
float phase1 = 1.57;
float phase2 = 1.57; //phases should be relative
selection: 0-.25 is .6, .25-.5 is .3, .5 - 1 is .1
mutation: f: 2, amp: 20, ph: pi/4
"""

def write_back(parameter_list, speed, heading_change, euclid_dist, time_diff):
    """appends new run to data file, parameter_list should be a list of length 6, others should be floats"""
    prev_data = np.genfromtxt('learndata.csv', delimiter=',',dtype=float)
    a = [speed, heading_change, euclid_dist, time_diff]
    a.extend(parameter_list) 
    new_run = np.array(a)
    new_data = np.vstack((prev_data,new_run))
    np.savetxt('learndata.csv', new_data, delimiter=',',fmt="%f")

def get_new_params():
    """returns parameters of next run"""
    prev_data = np.genfromtxt('learndata.csv', delimiter=',',dtype=float)
    #dtype = [('freq',float),('amp0',float),('amp1',float),('amp2',float),('ph1',float),('ph2',float),('speed',float),('heading_change',float),('euclid_dist',float),('time_diff',float)]
    #b = np.array(prev_data, dtype = dtype)
    #instead of this working nicely with fields, just have speed as the first col
    sorted_array= np.sort(prev_data, axis = 0)
    num_runs = np.shape(sorted_array)[0]    
    ind_base = weighted_draw(num_runs)
    ind_second = weighted_draw(num_runs)
    params_base = sorted_array[ind_base, 4:10]
    params_second = sorted_array[ind_second, 4:10]
    combined = recombine_params(params_base, params_second)
    mutated = mutate_params(combined, num_runs)
    return mutated.tolist()
    
def mutate_params(gene, num_runs):
    """modifies the gene by random mutation, final magnitudes set according to freq, amp, phase ranges"""
    mut_prob = 0.25
    mut_mag = anneal_sched_mut_mag(num_runs)
    if random.random() < mut_prob:
        gene[0] += 2*(random.random()-0.5)*mut_mag*2
        gene[0] = range_coerce(gene[0],0.2,6)
    for i in range(1,4):
        if random.random() < mut_prob:
            gene[i] += 2*(random.random()-0.5)*mut_mag*40
            gene[i] = range_coerce(gene[i],20,90)
    for i in range(4,6):
        if random.random() < mut_prob:
            gene[i] += 2*(random.random()-0.5)*mut_mag*(math.pi/4.0)
            gene[i] = range_coerce(gene[i],-math.pi, math.pi)
    return gene

def range_coerce(x, lower, upper):
    if x> upper:
        return upper
    elif x < lower:
        return lower
    else: return x

def anneal_sched_mut_mag(generation_num):
    """calculates appropriate ratio of magnitude of mutation given number of runs"""
    mut_mag = None    
    if 0 <= generation_num < 40:
        mut_mag = (1-float(generation_num)/40.0)
    if 40<= generation_num < 50:
        mut_mag = .2
    if 50<= generation_num:
        mut_mag = 0
    return mut_mag
                
    
def recombine_params(params_base, params_second):
    """brings some part of the second gene into the first"""
    k = random.random()
    if k<.2:
        params_base[0] = params_second[0]
        return params_base
    if k<.4:
        params_base[1] = params_second[1]
        return params_base
    if k<.6:
        params_base[2] = params_second[2]
        return params_base
    if k<.8:
        params_base[3] = params_second[3]
        return params_base
    params_base[4:5] = params_second[4:5]
    return params_base
        
def weighted_draw(num_runs):
    """returns index of previous run to use, based on weighting of different sections"""
    quartile = min(1,math.ceil(float(num_runs)/4.0))
    half = min(1,math.ceil(float(num_runs)/2.0))
    k = random.random()
    if k<.6:        
        return random.randint(num_runs-1-quartile,num_runs-1) #would like to reverse sort, but not built in
    if k<.9:        
        return random.randint(half,num_runs-1-quartile)
    return random.randint(0,half-1)

