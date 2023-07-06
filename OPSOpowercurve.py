import os
import pygrib
import matplotlib.pyplot as plt
import pandas as pd
import paramiko
import math
import numpy as np
from mealpy.swarm_based.PSO import OriginalPSO


#Wind data
wind_speed = pd.read_csv('wind_speed-chubu2019.csv', skiprows = 10 , index_col= 0, header = None)
print(wind_speed)


#Observed Area Power
P_area = pd.read_excel('AreaPower_chubu2019.xlsx', usecols= [2] , nrows = 8751 , header = None)
P_area.index = wind_speed.index.copy()
print(P_area)

#Setting P_local Dataframe
P_local = pd.DataFrame(np.zeros((len(wind_speed),len(wind_speed.columns))))
print(P_local)



#Fitness function
def fitness_function(solution): 
    
    #Defining five parameter logistic function
    def five_logistic(u, A, B, C, D, G):
        return (A - D) / ((1 + (u / C) ** B) ** G) + D  
    
    #Calculating P_local with five logistic
    for t in range(len(wind_speed)):
        for place in range(len(wind_speed.columns)):
            P_local.iat[t,place] = five_logistic(wind_speed.iat[t,place], solution[0], solution[1], solution[2], solution[3], solution[4])
    
    difference = []
    for t in range(8751):
        difference.append(np.square(P_area.iat[t,0] - P_local.sum(axis=1).iat[t]))
    
    return difference


#Minimize fitness function with lb and ub as parameter bounds
problem_dict1 = {
    "fit_func": fitness_function,
    "lb": [0, 0, 0, 0, 0],
    "ub": [100, 100, 100, 100, 100],
    "minmax": "min",
    "obj_weights":[1]*8751
}

#PSO algorithm parameters
epoch = 100
pop_size = 50
c1 = 2.05
c2 = 2.05
w_min = 0.4
w_max = 0.9
model = OriginalPSO(epoch, pop_size, c1, c2, w_min, w_max)
best_position, best_fitness = model.solve(problem_dict1)
print(f"Solution: {best_position}, Fitness: {best_fitness}")
