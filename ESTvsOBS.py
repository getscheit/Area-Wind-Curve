import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

error = pd.read_excel('shikoku/Error/LF Error 01.xlsx', skiprows = 1, header = None)
estimated = pd.read_excel('shikoku/Estimated/LF Local 01.xlsx', skiprows = 1, header = None)
estimated.set_index([0])
observed = pd.read_excel('APower/AreaPower_'+'shikoku'+'2019.xlsx', usecols=[2],  header = None)
observed.index = error.index.copy()


print(estimated.head)
print(observed.head)


fig, ax = plt.subplots()

plt.title("shikoku Wind Power (Estimated vs Observed)")
plt.xlabel("Observed [MWh]")
plt.ylabel("Estimated [MWh]")
ax.grid()

x = np.linspace(0,400)
y = np.linspace(0,400)

ax.set_ylim([0,400])
ax.set_xlim([0,400])


plt.scatter(observed[2], estimated.iloc[:,1:38].sum(axis=1), s=1)
plt.plot(x,y, linewidth=1, color = 'red')
os.makedirs('shikoku/ESTvsOBS', exist_ok=True)
plt.savefig('shikoku/ESTvsOBS/LF ESTvsOBS 01.png')