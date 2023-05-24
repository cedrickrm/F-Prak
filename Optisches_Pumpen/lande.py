# -*- coding: utf-8 -*-
"""
Created on Sat May 13 13:00:38 2023

@author: ckram
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import peak_widths
from matplotlib.gridspec import GridSpec
import csv

class LandeFaktor:
    def __init__(self,path):
        self.path = path
        self.file = open(self.path)
        self.file = csv.reader(self.file,delimiter='\t')
        self.time = []
        self.channel1 = []
        self.channel2 =[]
        for line in self.file:
            self.time.append(float(line[0]))
            self.channel1.append(float(line[1]))
            self.channel2.append(float(line[2]))
        self.time = np.array(self.time)
        self.time_phase = self.time 
        self.channel1 = np.array(self.channel1) 
        self.channel2= np.array(self.channel2)

    def findpeaksauto(self):
        peaks = find_peaks(-self.channel2,prominence=0.0019,distance=5)
        return peaks[0]

    def give_current(self,peaks):
        widerstand = 1.745 + 0.05
        return self.channel1[peaks-26] / widerstand

    def get_b(self,errors=[]):
        current = self.give_current(self.findpeaksauto())
        mu0 = 1.256637061e-6
        N = 80
        r = 0.09
        B = mu0*(4/5)**(3/2) * N/r * current
        return B

    def sweep(self):
        frequenz = 9.875*(self.time[self.findpeaksauto()]-0.012) + 0.5
        print(frequenz)

    def plotwithpeaks(self,peaks,findpeaks = False):
        if findpeaks:
            peaks = self.findpeaksauto()
        fig = plt.figure(figsize=(11,6))
        gs = GridSpec(8,5)
        fig1 = fig.add_subplot(gs[:,:])
        fig1.set_title(str(self.path)[31:], fontsize = 15)

        fig1.set_xlabel('Zeit in s',fontsize = 15)
        fig1.set_ylabel(r'Spannung $U_{HH}$ in V',color = 'r', fontsize = 15)
        fig1.tick_params(axis='y',labelcolor='r')
        fig1.plot(self.time_phase, self.channel1,'r-', label = 'Channel 1')
        fig1.grid(True)

        fig2 = fig1.twinx()
        fig2.set_ylabel(r'Spannung  $U_{RF}$ in V',color='g',fontsize=15)
        fig2.tick_params(axis='y',labelcolor = 'g')
        fig2.plot(self.time,self.channel2,'g',label='Channel 2')
        for peak in peaks:
            plt.plot(self.time[peak],self.channel2[peak],'bo')

lande2500 = LandeFaktor('230508_OptischesPumpen/Resonanz2500kHz')
lande = LandeFaktor('230508_OptischesPumpen/30HZ_Zeitversatz_Induktivitaet')
#lande.sweep()
#print(lande2500.getpeakwidth())
peaks = [988,1076,1423,1512]
lande.plotwithpeaks(peaks,findpeaks=True)
#lande2500.plotwithpeaks(peaks,findpeaks=True)
#print(lande2500.get_b(lande2500.findpeaksauto()))

'''
dateien = np.arange(500,8000,500)
Ru85 = []
Ru185 = []
Ru87 =[]
Ru187=[]
for datei in dateien:
    lande = LandeFaktor('230508_OptischesPumpen/Resonanz'+str(datei)+'kHz')
    b_peaks = lande.get_b()
    Ru85.append(b_peaks[1])
    Ru185.append(b_peaks[-2])
    Ru87.append(b_peaks[2])
    Ru187.append(b_peaks[-3])
plt.plot(dateien*1000,Ru85,'d',label='Ru85')
plt.plot(dateien*1000,Ru87,'o',label='Ru87')
plt.plot(dateien*1000,Ru185,'d',label='Ru85_1')
plt.plot(dateien*1000,Ru187,'o',label='Ru87_1')
plt.xlabel('Frequenz in Hz')
plt.ylabel('Magnetfel in T')

fit,err = np.polyfit(dateien*1000,Ru185,deg=1,cov = True)
da = np.sqrt(err[0,0])
a = fit[0]
b=fit[1]
print(a)
h = 6.626e-34
mub = 9.274e-24
print('g='+str(h/(mub*a)))
print('dg='+str(h*da/(mub*a**2)))
yseq = a*dateien*1000+b
plt.plot(dateien*1000,yseq)
plt.legend()
'''
#plt.xlim(0.475,0.525)
