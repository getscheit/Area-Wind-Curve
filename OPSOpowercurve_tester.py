import os
import pygrib
import matplotlib.pyplot as plt
import pandas as pd
import paramiko
import math
import numpy as np
from mealpy.swarm_based.PSO import OriginalPSO

#Wind Turbine Max Generation Capacity Data
gcap = pd.read_excel('WPplace_chubu.xlsx',skiprows = 1, usecols=[7], header = None )
gcap_t = gcap.transpose()
print(gcap_t)

#Wind data
wind_speed = pd.read_csv('wind_speed-chubu2019.csv', skiprows = 10 , index_col= 0, header = None)
print(wind_speed)

#Observed Area Power
P_area = pd.read_excel('AreaPower_chubu2019.xlsx', usecols= [2] , nrows = 8751 , header = None)
P_area.index = wind_speed.index.copy()
print(P_area)

#Matrix Dimensions
time = len(wind_speed)
place = len(wind_speed.columns)

#Setting P_local Dataframe
P_local = pd.DataFrame(np.zeros((time,place)))
print(P_local)


#Fitness function
def fitness_function(solution): 
    
    #Defining five parameter logistic function
    def five_logistic(u, A, B, C, D, G):
        return (A - D) / ((1 + (u / C) ** B) ** G) + D  
    
    #Setting constraints for logistic function output
    def violate(value):
        if value <= 0:
            return 0
        elif value >= gcap_t.iloc[0,p]*0.001:
            return gcap_t.iloc[0,p]*0.001
        else:
            return value
    
    #Calculating P_local with five logistic
    for p in range(place):
        P_local.iloc[0,p] = violate(five_logistic(wind_speed.iloc[0,p], solution[0], solution[1], solution[2], solution[3], solution[4]))
    
    difference = []
    difference.append(np.square(P_area.iat[0,0] - P_local.sum(axis=1).iat[0]))
    
    return difference


#Minimize fitness function with lb and ub as parameter bounds
problem_dict1 = {
    "fit_func": fitness_function,
    "lb": [0, -8, 9, -2, 0.4],
    "ub": [4000, -5, 25, 15, 0.6],
    "minmax": "min",
    "obj_weights":[1]*8751
}

#PSO algorithm parameters
epoch = 100
pop_size = 50
c1 = 2.0
c2 = 2.0
w_min = 0.4
w_max = 0.6
model = OriginalPSO(epoch, pop_size, c1, c2, w_min, w_max)
best_position, best_fitness = model.solve(problem_dict1)
print(f"Solution: {best_position}, Fitness: {best_fitness}")
print(P_local)

#Visualization
model.history.save_global_objectives_chart(filename="Five Parameter Logistic Function/goc")
model.history.save_local_objectives_chart(filename="Five Parameter Logistic Function/loc")

model.history.save_global_best_fitness_chart(filename="Five Parameter Logistic Function/gbfc")
model.history.save_local_best_fitness_chart(filename="Five Parameter Logistic Function/lbfc")

model.history.save_runtime_chart(filename="Five Parameter Logistic Function/rtc")

model.history.save_exploration_exploitation_chart(filename="Five Parameter Logistic Function/eec")

model.history.save_diversity_chart(filename="Five Parameter Logistic Function/dc")
