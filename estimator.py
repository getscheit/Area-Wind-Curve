import os
import pygrib
import matplotlib.pyplot as plt
import pandas as pd
import paramiko
import math
import numpy as np

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

#Wind Turbine Max Generation Capacity Data
gcap= pd.read_excel('WPlace/WPplace_'+'chubu'+'.xlsx',skiprows = 1, usecols=[7], header = None )
print(gcap)

#Wind data 
wind_speed = pd.read_csv('WSpeed/wind_speed-'+'chubu'+'2019.csv',  skiprows = 1 , index_col= 0, header = None)
print(wind_speed)

#Observed Area Power
observed = pd.read_excel('APower/AreaPower_'+'chubu'+'2019.xlsx', usecols=[2],  header = None)
observed.index = wind_speed.index.copy()
print(observed)

#Estimated Power Matrix Set-up
time = len(wind_speed)
place = len(wind_speed.columns)
estimated = pd.DataFrame(np.zeros((time,place)))
estimated.index = observed.index.copy()

### 5PL Parameters ###
fivePL =   [0.78647209, -7.65987677, 11.17183755,  0.05629719,  0.3522118]

### Linear Parameters ###
linear = [2.71291815, 15.3625476,  19.99231292]

### 5PL Function ###
#for p in range(place):
#        estimated.iloc[:,p] = gcap.iat[p,0]*.001*(five_logistic(wind_speed.iloc[:,p], fivePL))

### Linear Function ###
for p in range(place):
    estimated.iloc[:,p] = gcap.iat[p,0]*.001*(wind_speed.iloc[:,p].apply(lambda x: linear_function(x, linear)))
    
print(estimated)
print(estimated.iloc[:,1:38].sum(axis=1))

### RMSE ###
SE = (np.square(observed.iloc[:,0] - estimated.sum(axis=1).iloc[:])).tolist()
RMSE = math.sqrt((sum(SE))/time)
print("RMSE:" + str(RMSE))
### MAE ###
abs_diff = (abs(observed.iloc[:,0] - estimated.sum(axis=1).iloc[:])).tolist()
MAE = sum(abs_diff)/time
print("MAE: "+ str(MAE))

# Observed - Estimated error
error = observed.iloc[:,0] - estimated.sum(axis=1).iloc[:]
print(error.head)

### OUTPUT ###
os.makedirs('chubu/Estimated', exist_ok=True)
os.makedirs('chubu/Error', exist_ok=True)
estimated.to_excel('chubu/Estimated/LF Local 01.xlsx')
error.to_excel('chubu/Error/LF Error 01.xlsx')