import numpy as np
from matplotlib import pyplot as plt
from WavePy import *
from time import sleep

# Inputs
c = 10              # m/s
L = 100             # m
tTotal = 60         # s
xStep = 1           # m
tStep = 0.1         # s
sings = [Free(0), Half(L/3), Fix(L)]

# Pulse Input
P0 = 10
t1 = 1
pulse = Constant(P0, t1, c, L, tTotal, xStep, tStep, sings)

# Postion Plots
pulse.plot_fixed_position(33, True)
pulse.plot_fixed_position(66, True)
plt.legend()
plt.xlabel("t")
plt.ylabel("P")
plt.grid()
plt.show()

# Time Plots
pulse.plot_fixed_time(10, True)
pulse.plot_fixed_time(20, True)
pulse.plot_fixed_time(30, True)
pulse.plot_fixed_time(40, True)
pulse.plot_fixed_time(50, True)
plt.legend()
plt.xlabel("x")
plt.ylabel("P")
plt.grid()
plt.show()

# Contour Plot
pulse.plot_contourf()
