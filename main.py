
import pandas as pd
import math
import numpy as np
from mealpy.swarm_based.PSO import OriginalPSO

area_name = input('Input area name:\n') #\n ----> newline 
    #[choose from 10 areas: 
    # chubu, chugoku, hokkaido, 
    # hokuriku, kansai, kyushu,                                  
    # okinawa, shikoku, tohoku, tokyo]

function_name = input('Input function to be used:\n')
    #[choose from functions: five logistic, linear, four logistic]

target_objective = input('Input target objective:\n')
    #[choose fitness evaluation method: RMSE, MAE]

#Wind Turbine Max Generation Capacity Data
gcap= pd.read_excel('WPlace/WPplace_'+area_name+'.xlsx',skiprows = 1, usecols=[7], header = None )
print(gcap)

#Wind data 
wind_speed = pd.read_csv('WSpeed/wind_speed-'+area_name+'2019.csv',  skiprows = 1 , index_col= 0, header = None)
print(wind_speed)

#Observed Area Power
observed = pd.read_excel('APower/AreaPower_'+area_name+'2019.xlsx', usecols=[2],  header = None)
observed.index = wind_speed.index.copy()
print(observed)

#Estimated Power Matrix Set-up
time = len(wind_speed)
place = len(wind_speed.columns)
estimated = pd.DataFrame(np.zeros((time,place)))
estimated.index = observed.index.copy()


#Fitness function
def fitness_function(solution): 
 ### Linear function ###
    def linear_function(u, cutin, rated, cutout):
        if u <= cutin and u >= cutout:
            return 0.0
        if u > cutin and u < rated:
            return  (u-cutin) / (rated-cutin)
        if u >= rated and u < cutout:
            return  1.0
 ### Five parameter logistic function ###
    def five_logistic(u, A, B, C, D, G):
        return ((A - D) / ((1 + (u / C) ** B) ** G)) + D 
 ### Four parameter logistic function ###
    def four_logistic(u, A, M, T, N):
        return A * ((1 + M*math.exp(-u/T))/(1 + N*math.exp(-u/T))) 

    if function_name == 'five logistic':
        for p in range(place):
            estimated.iloc[:,p] = gcap.iat[p,0]*.001*(five_logistic(wind_speed.iloc[:,p], solution[0], solution[1], solution[2], solution[3], solution[4]))
    elif function_name == 'linear':
        for p in range(place):
            estimated.iloc[:,p] = gcap.iat[p,0]*.001*(wind_speed.iloc[:,p].apply(lambda x: linear_function(x, solution[0], solution[1], solution[2])))
    elif function_name == 'four logistic':
        for p in range(place):
            estimated.iloc[:,p] = gcap.iat[p,0]*.001*(wind_speed.iloc[:,p].apply(lambda x: four_logistic(x, solution[0], solution[1], solution[2], solution[3])))

    ### Root Mean Squared Error ###
    SE = (np.square(observed.iloc[:,0] - estimated.sum(axis=1).iloc[:])).tolist()
    RMSE = math.sqrt((sum(SE))/time)
    
    ### Mean Absolute Error ###
    abs_diff = (abs(observed.iloc[:,0] - estimated.sum(axis=1).iloc[:])).tolist()
    MAE = sum(abs_diff)/time
    
    if target_objective == 'RMSE':
        return RMSE
    elif target_objective == 'MAE':
        return MAE


#Minimize fitness function with lb and ub as parameter bounds
if function_name == 'five logistic':
    problem_dict = {
        "fit_func": fitness_function,
        "lb": [0, -30, 0, -10, -10], #lower bounds for a, b, c, d, g
        "ub": [2, 30, 50, 10, 10], #upper bounds for a, b, c, d, g
        "minmax": "min",
        "obj_weights":[1]*8760
    }
elif function_name == 'linear':
    problem_dict = {
        "fit_func": fitness_function,
        "lb": [0, 0, 0], #lower bounds for cut-in, rated, cut-out
        "ub": [30, 30, 50], #upper bounds for cut-in, rated, cut-out
        "minmax": "min",
        "obj_weights":[1]*8760
    }
elif function_name == 'four logistic':
    problem_dict = {
        "fit_func": fitness_function,
        "lb": [0, -30, 0, -10], #lower bounds for a, b, c, d
        "ub": [2, 30, 50, 10], #upper bounds for a, b, c, d
        "minmax": "min",
        "obj_weights":[1]*8760
    }


#Stopping conditions
term_dict = {

    "max_early_stop": 5000,
    
}

#PSO algorithm parameters
epoch = 10000

if function_name == 'five logistic':
    pop_size = 250
elif function_name == 'linear':
    pop_size = 50
elif function_name == 'four logistic':
    pop_size = 125

c1 = 2.0
c2 = 2.0
w = 0.4
model = OriginalPSO(epoch, pop_size, c1, c2, w)
best_solution, best_fitness = model.solve(problem_dict, termination = term_dict)

#Results Output
print("")
print(area_name + '' + function_name + ' results:')
print(f"Solution: {best_solution}, Fitness: {best_fitness}")
print(str(pop_size))




