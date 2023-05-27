# -*- coding: utf-8 -*-
"""
Created on Sat May 27 12:04:58 2023

@author: ckram
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.signal import peak_widths
from matplotlib.gridspec import GridSpec
import csv
import os

class LaserData:
    def __init__(self,path):
        self.wavelenghts = np.array([229,233,237,241,245,249,253]) +780
        self.file = open(path)
        self.file = csv.reader(self.file, delimiter='\t')
        self.time =[]
        self.piezo_voltage = []
        self.fabry_perot = []
        self.probe_laser = []
        self.laser_voltage =[]
        for line in self.file:
            self.time.append(float(line[0]))
            self.piezo_voltage.append(float(line[1]))
            self.fabry_perot.append(float(line[2]))
            self.probe_laser.append(float(line[3]))
            self.laser_voltage.append(float(line[4]))
        self.time = np.array(self.time)
        self.laser_voltage = np.array(self.laser_voltage)
        self.piezo_voltage = np.array(self.piezo_voltage)
        self.fabry_perot = np.array(self.fabry_perot)
        self.probe_laser = np.array(self.probe_laser)
    
    def plot(self,with_peaks = False):
        fig = plt.figure(figsize=(11,6))
        gs = GridSpec(8,5)
        fig1 = fig.add_subplot(gs[:,:])
        fig1.plot(self.piezo_voltage,self.probe_laser,'-')
        #fig1.plot(self.time,self.piezo_voltage)
        if with_peaks:
            peaks,_ = find_peaks(self.fabry_perot,prominence=0.3,height=0.8)
            print(len(peaks))
            for peak in peaks:
                fig1.plot(self.piezo_voltage[peak],self.fabry_perot[peak],'go')
        fig1.set_xlabel('Zeit in s',fontsize = 15)
        fig1.set_ylabel('Spannung in V',fontsize = 15)
    
    def slice_data(self):
        # deletes the data outside the given index_range
        idx_start = list(self.piezo_voltage).index(np.max(self.piezo_voltage))
        idx_stop = list(self.piezo_voltage).index(np.min(self.piezo_voltage))
        self.time = self.time[idx_start:idx_stop] - self.time[idx_start]
        self.piezo_voltage = self.piezo_voltage[idx_start:idx_stop]
        self.fabry_perot = self.fabry_perot[idx_start:idx_stop]
        self.probe_laser = self.probe_laser[idx_start:idx_stop]
        self.laser_voltage = self.laser_voltage[idx_start:idx_stop]

laser = LaserData('Data/spektrum_dopplerfrei_mit_pump_freq1.dat') 
laser.slice_data()