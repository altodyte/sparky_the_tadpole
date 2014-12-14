# -*- coding: utf-8 -*-
"""
Created on Sun 2014/12/14 11:08:00
@author mbocamazo
Run genetic algorithm for tadpole gait optimization
"""
import random
import pygame
import math
import pickle as p
import csv
import os
import numpy as np

#np.savetxt("foo.csv", test_output, delimiter=",",fmt="%s")

def write_back(parameter_list, speed, heading_change, euclid_dist, time_diff):
    """appends new run to data file, parameter_list should be a tuple of length 6, others should be floats"""
    prev_data = genfromtxt('foo.csv', delimiter=',',dtype=None)
    #whatever concatenation needs to happen here
    new_run = np.array(parameter_list, speed, heading_change, euclid_dist, time_diff)
    new_data = np.vstack((prev_data,new_run))
    np.savetxt("foo.csv", new_data, delimiter=",",fmt="%s")

def get_new_params():
    """returns parameters of next run"""
    prev_data = genfromtxt('train.csv', delimiter=',',dtype=None)
    #sort 

    f = open(filename,'w')
    f.write(x)
    f.close()
    """
    recom prob 
    mut prob
    mut mag calc 
    mut mag list 
    generations? - just length of list
    ...histogram of past 
    and other measures of central tendency of past runs, statistical measures, etc
    annealing Schedule
    mutation probs over all, tuple of mutation mags over all parameters, should be different mags for different params
    selection: 0-.25 is .6, .25-.5 is .3, .5 - 1 is .1

    sort
    draw 2
    recombine func 
    mutate func 
    return
    """

    self.AI_list.sort(key=lambda x: x.tournament_score, reverse=True)
    dtype = [('name', 'S10'), ('height', float), ('age', int)]
    values = [('Arthur', 1.8, 41), ('Lancelot', 1.9, 38), ('Galahad', 1.7, 38)]
    a = np.array(values, dtype=dtype)       # create a structured array
    np.sort(a, order='height')                        
    res: array([('Galahad', 1.7, 38), ('Arthur', 1.8, 41), ('Lancelot', 1.8999999999999999, 38)], dtype=[('name', '|S10'), ('height', '<f8'), ('age', '<i4')])    


    def recombine_genes(self,AI_list):
        """doesnt modify order of AI list"""
        AI_num = len(AI_list)
        quartile = AI_num/4         
        for i in range(0,quartile):
            better_AI = AI_list[i]
            worse_AI = AI_list[-(i+1)]
            better_genome = better_AI.piece_weights
            worse_genome = worse_AI.piece_weights          
            for piece,score in better_genome.iteritems():
                if rand() < self.recom_prob:
                    worse_genome[piece] = score
        
    def mutate_genes(self,AI_list,generation_num):
        """doesnt modify order of AI list"""
        for i in range(1,len(AI_list)): #mutate everything but the best AI
            genome = AI_list[i].piece_weights            
            for piece,score in genome.iteritems():
                if rand() < self.mut_prob:
                    mut_mag = self.mut_mag_calc_func(generation_num)
                    print mut_mag
                    score += 2*(rand()-0.5)*mut_mag
                    
def anneal_sched_mut_mag(generation_num):
    mut_mag = None    
    if 0 <= generation_num < 40:
        mut_mag = 1-generation_num/40.0
    if 40<= generation_num < 50:
        mut_mag = .1
    if 50<= generation_num <= 55:
        mut_mag = 0
    return mut_mag
                
            
            
    
def build_random_pair_piece_dict():
    """generates a random pair piece dictionary that is used by the
    pair material eval function. AI will store and pass this
    dictionary/attribute to the pair material eval func. currently no distinguishing
    between different bishops and only takes presence of pieces of board into account
    (ex. doesn't distinguish between the enemy having two rooks or one rook when
    weighting the value of my queen)"""
    piece_list = ['r','n','b','q','R','N','B','Q']
    pair_piece_dict = {}
    for p in piece_list:
        no_p = list(piece_list)
        no_p.remove(p) #create copy of list without the piece in it
        inner_piece_dict = {}
        for n in no_p:
            inner_piece_dict[n] = random.uniform(-.5,.5) #random double between -1 and 1 for pair piece vals          
        pair_piece_dict[p] = inner_piece_dict
    return pair_piece_dict     
    
def build_random_piece_dict():
    """generates a random piece dictionary that is used by the
    material eval function. AI will store and pass this
    dictionary/attribute to the material eval func.king and pawn weights
    are defined elsewhere in the evaluate simple material func
    since they aren't uniquely determined"""
    piece_score_dict = {}
    b_piece_list = ['r','n','b','q']
    for b in b_piece_list:
        rand_num = random.uniform(-10,0)
        piece_score_dict[b] = rand_num  
        piece_score_dict[b.upper()] = -rand_num 
    return piece_score_dict
