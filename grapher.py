import os
import matplotlib.pyplot as plt
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


x = np.linspace(0, 100, 100000)

fivePL = [11.65873468, -5.00452583, 20.37694124,  0.61086232,  0.40594975]

### 5PLF Grapher ###
#y = five_logistic(x, fivePL)

linear = [2.46684696, 16.43110041, 20.14536817]

### Linear Grapher ###
y = np.zeros(100000)
for t in range(len(y)):
    y[t] = linear_function(x[t], linear)



fig , ax = plt.subplots()

plt.title("OPSO Power Curve shikoku")
plt.xlabel("Wind Speed [m/s]")
plt.ylabel("Power Output [MW]")
ax.grid()

ax.set_ylim([0,1.2])
ax.set_xlim([0,30])

#plt.plot(x, y, label= '5PLF')
plt.plot(x, y, label = 'LF')

plt.legend()
os.makedirs('shikoku/PCurves', exist_ok=True)
plt.savefig('shikoku/PCurves/LF01.png')

