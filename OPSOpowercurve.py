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


    

#Fitness function
def fitness_function(mse):
    #Five parameter logistic function
    def five_logistic(u, A, B, C, D, G):
        return (A - D) / ((1 + (u / C) ** B) ** G) + D

    #P_local
    P_local = pd.DataFrame(np.zeros((8751, len(wind_speed.columns))), index = wind_speed.index.copy())
    for t in range(8751):
            for place in range(len(wind_speed.columns)):
                a, b ,c ,d, g = ()
                P_local.iat[t, place] = five_logistic(wind_speed.iat[t, place], a, b, c, d, g)
                
    Sum_P_local = P_local.sum()
    mse = np.mean(np.square(P_area - Sum_P_local)) #Calculate the mean squared error
    return mse

#Minimize fitness function with lb and ub as parameter bounds
problem_dict1 = {
    "fit_func": fitness_function,
    "lb": [-5, -5, -5, -5, -5],
    "ub": [5, 5, 5, 5, 5],
    "minmax": "min",
}

#PSO algorithm parameters
epoch = 1000
pop_size = 50
c1 = 2.05
c2 = 2.05
w_min = 0.4
w_max = 0.9
model = OriginalPSO(epoch, pop_size, c1, c2, w_min, w_max)
best_position, best_fitness = model.solve(problem_dict1)
print(f"Solution: {best_position}, Fitness: {best_fitness}")