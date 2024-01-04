import os
import pygrib
import matplotlib.pyplot as plt
import pandas as pd
import paramiko
import math
import numpy as np

area_name = input('Input area name:\n') #\n ----> newline 
    #[choose from 10 areas: 
    # chubu, chugoku, hokkaido  
    # hokuriku, kansai, kyushu,                                  
    # okinawa, shikoku, tohoku, tokyo]

function_name = input('Input function to be used:(5PLF, 4PLF, LF)\n')
    #[choose from functions: five logistic, linear, four logistic]

simul_num = input('Input simulation number:\n')

def five_logistic(u, params):
    [A, B, C, D, G] = params 
    return ((A - D) / ((1 + (u / C) ** B) ** G)) + D 

def linear_function(u, params):
    [cutin, rated, cutout] = params
    if u <= cutin:
        return 0.0
    elif u > cutin and u < rated:
        return  (u-cutin) / (rated-cutin)
    elif u >= rated and u < cutout:
        return  1.0
    elif u >= cutout:
        return  0.0

def four_logistic(u, params):
    [A, B, C, D] = params
    return ((A - D) / ((1 + (u / C) ** B))) + D 

#Wind Turbine Max Generation Capacity Data
gcap= pd.read_excel('WPlace/WPplace_'+ area_name +'.xlsx',skiprows = 1, usecols=[7], header = None )
print(gcap)

#Wind data 
wind_speed = pd.read_csv('WSpeed/wind_speed-'+ area_name +'2019.csv',  skiprows = 1 , index_col= 0, header = None)
print(wind_speed)

#Observed Area Power
observed = pd.read_excel('APower/AreaPower_'+ area_name +'2019.xlsx', usecols=[2],  header = None)
observed.index = wind_speed.index.copy()
print(observed)

#Estimated Power Matrix Set-up
time = len(wind_speed)
place = len(wind_speed.columns)
estimated = pd.DataFrame(np.zeros((time,place)))
estimated.index = observed.index.copy()

### 5PL Parameters ###
fivePL = []

### Linear Parameters ###
linear = []

### 4PLF Parameters ###
fourPL = []


if function_name == '5PLF':
    for p in range(place):
            estimated.iloc[:,p] = gcap.iat[p,0]*.001*(five_logistic(wind_speed.iloc[:,p], fivePL))
elif function_name == 'LF':
    for p in range(place):
        estimated.iloc[:,p] = gcap.iat[p,0]*.001*(wind_speed.iloc[:,p].apply(lambda x: linear_function(x, linear)))
elif function_name == '4PLF':
    for p in range(place):
        estimated.iloc[:,p] = gcap.iat[p,0]*.001*(four_logistic(wind_speed.iloc[:,p], fourPL))
    
print(estimated)
print(estimated.iloc[:,1:38].sum(axis=1))

### RMSE ###
SE = (np.square(observed.iloc[:,0] - estimated.sum(axis=1).iloc[:])).tolist()
RMSE = math.sqrt((sum(SE))/time)
print(area_name + " RMSE:" + str(RMSE))
### MAE ###
abs_diff = (abs(observed.iloc[:,0] - estimated.sum(axis=1).iloc[:])).tolist()
MAE = sum(abs_diff)/time
print(area_name + " MAE: "+ str(MAE))

# Observed - Estimated error
error = observed.iloc[:,0] - estimated.sum(axis=1).iloc[:]
print(error.head)

### OUTPUT ###
os.makedirs(area_name + '/Estimated', exist_ok=True)
os.makedirs(area_name + '/Error', exist_ok=True)

estimated.to_excel(area_name + '/Estimated/' + function_name + ' Local ' + simul_num + '.xlsx')
error.to_excel(area_name + '/Error/' + function_name + ' Error ' + simul_num +'.xlsx')

