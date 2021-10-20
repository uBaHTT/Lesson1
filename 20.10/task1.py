import numpy as np
import matplotlib.pyplot as plt

with open("data.txt", "r") as data: 
    data_array = [float(i) for i in data.read().split("\n")]

settings_array = np.loadtxt("settings.txt", dtype = float)
time_array = np.arange(settings_array.size) / 10
settings_array = settings_array * 3.3 / 256

fig, ax = plt.subplots(figsize = (16, 10), dpi = 100)

plt.figtext(0.5, -0.1, "figtext")
plt.xlabel("Time, s")
plt.ylabel("Voltage, v")
plt.minorticks_on()
plt.text(8, 0.9, "Время заряда 48,3 с", fontsize = 15)
plt.text(8, 0.5, "Время разряда 35,7 с", fontsize = 15)
ax.plot(time_array, settings_array, 'g', alpha=0.4, label="Напряжение", lw=2, mew=1, ms=2, marker = '.', ls = '-')
plt.legend()
ax.grid(which='minor', color = 'k', linestyle = ':')
plt.savefig("test.png")