import os
from subprocess import call
import wave
import pylab as pl
import numpy as np
import scipy.io.wavfile
import sys
from voice_activity import isActive, getActivity
sys.path.append('ML')
from features import *

DATADIR = 'rawdata'
PROCESSDIR = 'segmented_data'
MAXWORDS = 1
NMFCC = 55
WINDOW = 100
MOVINGAVG = 30
INTERVAL = 0.2 # at least 0.2 sec a word?
MAX_INTERVAL = 1
THRESHOLD = 0.75
OFFSET = 1000 # moving average induces a phase shift

def getEnergy(sig): #sig be a numpy array
    e = 0
    for s in sig:
        e += (s**2)/len(sig)
    return e
def movingAvg(sig, size):
    f = np.ones(size)/size
    return np.convolve(sig, f, 'same')
def getThreshold(sig, size):
    return movingAvg(sig, size)*THRESHOLD
def visualize(energy, threshold, bp, framerate):
    time = np.arange(0, len(energy)) * (100.0 / framerate)
    bp = np.array(bp)
    tmp = np.zeros(len(time))
    for b in bp:
        b = b/WINDOW
        tmp[b] = 100
    pl.figure()
    pl.subplot(211)
    pl.plot(time, energy, time, threshold)
    pl.subplot(212)
    pl.plot(time, tmp)
    pl.show()
def findMin(a, left, right):
    m = a[left]
    min_i = left
    for i in range(left, right):
        if a[i] > m:
            m = a[i]
            min_i = i
    return min_i
def breakDown(wave_data, fs, dovisualize=False):        
    energy = []
    for i in range(0, len(wave_data), WINDOW):
        e = 0
        if len(wave_data)-i < WINDOW:
            e = getEnergy(wave_data[i:])
        else:
            e = getEnergy(wave_data[i:i+WINDOW])
        energy += [e]
    energy = movingAvg(energy, MOVINGAVG)
    interval = int(fs*INTERVAL/WINDOW)
    max_interval = int(fs*MAX_INTERVAL/WINDOW)
    threshold = getThreshold(energy, interval)
    bp = [OFFSET/WINDOW]
    i = interval/2
    while(i < len(energy) - interval/2):
        if(i-bp[-1] > max_interval):
            bp += [i]
            i += interval
        elif(energy[i] < threshold[i]):
            min_i = findMin(energy, i-interval/2, i+interval/2)
            if(min_i == i):
                bp += [i]
                i += interval
            elif(min_i > i):
                i = min_i
                bp += [i]
                i += interval
        i += 1
    bp = [b*WINDOW-OFFSET for b in bp]
    if dovisualize:
        visualize(energy, threshold, bp, fs)
    return bp

if __name__ == '__main__':
    if not os.path.exists(PROCESSDIR):
        os.mkdir(PROCESSDIR)
    data = []
    for (dirpath, dirnames, filenames) in os.walk(DATADIR):
        data.extend(filenames)
        break
    for name in data:
        if os.path.exists(os.path.join(PROCESSDIR, name)):
            print("%s is already processed" % name)
            continue
        ext = name.split('.')[-1]
        if ext != 'wav':
            continue
        (wave_data, framerate) = getSignal(os.path.join(DATADIR, name))
        (active, window) = getActivity(wave_data, framerate, True)
        bp = breakDown(wave_data, framerate, True)
        bp = bp + [len(wave_data)]
        os.makedirs(os.path.join(PROCESSDIR, name))
        for i in range(0, len(bp)-1):
            a = active[int(bp[i]/window):int(bp[i+1]/window)]
            if not isActive(a):
                continue
            y = wave_data[bp[i]:bp[i+1]]
            t_name = os.path.join(PROCESSDIR, name, "%d_%d_%s" % (bp[i], bp[i+1], name))      
            scipy.io.wavfile.write(t_name, framerate, y)
        print("processing %s DONE!" % name)