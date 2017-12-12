from .pulse import Pulse
from ..singularities import *
import numpy as np
from matplotlib import pyplot as plt

class Square:
    def __init__(self, P0, t1, c, L, tTotal, xStep, tStep, sings):
        self.P0 = P0
        self.t1 = t1
        self.c = c
        self.L = L
        self.tTotal = tTotal
        self.xStep = xStep
        self.tStep = tStep
        self.sings = sings
        
        self.x = np.arange(0, L, xStep)
        self.t = np.arange(0, tTotal, tStep)
        self.P = np.zeros((len(self.t), len(self.x)))

        self.pulses = [Pulse(0, P0, sings[1], 1, c, t1)]
        self.propagate()

    def propagate(self):
        for row, t in zip(range(len(self.t)), self.t):
            print(t)
            for i in range(len(self.pulses)):   # Change to for i in self.pulses
                # Check if it is alive
                if not self.pulses[i].alive:
                    continue
                
                # Update position
                self.pulses[i].pos = round(self.pulses[i].pos + self.pulses[i].vel * self.tStep, 4)
                # Calculate area of effect of the pulse
                aoe = [self.pulses[i].pos - self.t1*self.pulses[i].vel, self.pulses[i].pos]
                aoe = [min(aoe), max(aoe)]
                if self.pulses[i].vel > 0:
                    aoe[0] = max(aoe[0], self.sings[self.pulses[i].targetid-1].pos)
                    aoe[1] = min(aoe[1], self.pulses[i].target.pos)
                else:
                    aoe[0] = max(aoe[0], self.pulses[i].target.pos)
                    aoe[1] = min(aoe[1], self.sings[self.pulses[i].targetid+1].pos)
                # Find which degrees of freedom are affected
                dof_effect = [i for i in self.x if min(aoe) <= i <= max(aoe)]
                for j in dof_effect:
                    # Update P
                    column = np.where(self.x==j)[0][0]
                    self.P[row, column] += self.pulses[i].mag

                if self.pulses[i].has_reached():
                    if isinstance(self.pulses[i].target, Fix) or isinstance(self.pulses[i].target, Free):
                        pos = self.pulses[i].target.pos - (self.pulses[i].pos - self.pulses[i].target.pos)
                        mag = self.pulses[i].mag * self.pulses[i].target.Nb
                        vel = self.pulses[i].vel * (-1)
                        if vel > 0:
                            targetid = self.pulses[i].targetid + 1
                        else:
                            targetid = self.pulses[i].targetid - 1
                        target = self.sings[targetid]
                        t1 = self.pulses[i].t1
                        self.pulses.append(Pulse(pos, mag, target, targetid, vel, t1))
                    else:
                        # Reflection
                            pos = self.pulses[i].target.pos - (self.pulses[i].pos - self.pulses[i].target.pos)
                            if self.pulses[i].vel > 0:
                                mag = self.pulses[i].mag * self.pulses[i].target.Nb
                            else:
                                mag = self.pulses[i].mag * self.pulses[i].target.Nb_
                            vel = self.pulses[i].vel * (-1)
                            if vel > 0:
                                targetid = self.pulses[i].targetid + 1
                            else:
                                targetid = self.pulses[i].targetid - 1
                            target = self.sings[targetid]
                            t1 = self.pulses[i].t1
                            self.pulses.append(Pulse(pos, mag, target, targetid, vel, t1))
                        # Refraction
                            pos = self.pulses[i].target.pos
                            if self.pulses[i].vel > 0:
                                mag = self.pulses[i].mag * self.pulses[i].target.Nc
                            else:
                                mag = self.pulses[i].mag * self.pulses[i].target.Nc_
                            vel = self.pulses[i].vel
                            if vel > 0:
                                targetid = self.pulses[i].targetid + 1
                            else:
                                targetid = self.pulses[i].targetid - 1
                            target = self.sings[targetid]
                            t1 = self.pulses[i].t1
                            self.pulses.append(Pulse(pos, mag, target, targetid, vel, t1))

                # Try to kill
                self.pulses[i].has_passed()
                

    def plot_fixed_position(self, posX, hold=False):
        xi = np.where(self.x==posX)

        if not hold:
            plt.figure()

        plt.plot(self.t.T, self.P[:, xi].flatten(), label=f"x={posX}")
        

    def plot_fixed_time(self, time, hold=False):
        ti = np.where(self.t==time)

        if not hold:
            plt.figure()
        
        plt.plot(self.x, self.P[ti, :].flatten(), label=f"t = {time}")


    def plot_contourf(self, cbarl=-20, cbaru=20, cbarpoints=50, cbarticks=5, cmap="bwr"):
        cbar_range = np.linspace(cbarl, cbaru, cbarpoints, endpoint=True)
        cbar_ticks = np.linspace(cbarl, cbaru, cbarticks, endpoint=True)

        xGrid, tGrid = np.meshgrid(self.x, self.t)

        plt.figure()
        plt.contourf(xGrid, tGrid, self.P, cbar_range, cmap=cmap)
        plt.xlabel("x (m)")
        plt.ylabel("t (s)")
        plt.colorbar(ticks=cbar_ticks)
        plt.show()