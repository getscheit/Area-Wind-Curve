import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

error = pd.read_excel('Chuubu Results/Chuubu Error 11.xlsx', skiprows = 1, header = None)
P_local = pd.read_excel('Chuubu Results/Chuubu Local 11.xlsx', skiprows = 1, header = None)
observed_area = pd.read_excel('AreaPower_chubu2019.xlsx', usecols = [2], header = None)
observed_area.index = error.index.copy()

print(error.head)
print(P_local.head)
print(observed_area.head)

x = 0
y = np.linspace(0,8760)

fig, ax = plt.subplots()
fig = plt.figure(figsize=(40,2))

plt.title("OPSO Power Curve Chuubu Error")
plt.xlabel("Time [hr]")
plt.ylabel("Power Generated [MWh]")
plt.grid()
plt.xlim((0,8760))

plt.plot(error.index, observed_area[2], label = "Observed", linewidth = 1.5, color = "red")
plt.plot(error.index, P_local.iloc[:,1:38].sum(axis=1), label = "Estimated", linewidth = 1.5)
plt.legend()

plt.savefig('Chuubu Results/Error 11.png')