import os
import matplotlib.pyplot as plt
import numpy as np

function_name = input('Input function to be used:(5PLF, 4PLF, LF)\n')
    #[choose from functions: five logistic, linear, four logistic]

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

x = np.linspace(0, 100, 100000)

fivePL = []
linear = []
fourPL = []

### 5PLF Grapher ###
if function_name == '5PLF':
    y = five_logistic(x, fivePL)
### Linear Grapher ###
elif function_name == 'LF':
    y = np.zeros(100000)
    for t in range(len(y)):
        y[t] = linear_function(x[t], linear)
#### 4PLF Grapher ###
elif function_name == '4PLF':
    y = four_logistic(x, fourPL)

fig , ax = plt.subplots()

plt.title("OPSO Power Curve shikoku")
plt.xlabel("Wind Speed [m/s]")
plt.ylabel("Power Output [MW]")
ax.grid()

ax.set_ylim([0,1.2])
ax.set_xlim([0,30])


plt.plot(x, y, label = 'LF')

#plt.legend()
os.makedirs('shikoku/PCurves', exist_ok=True)
plt.savefig('shikoku/PCurves/LF01.png')

