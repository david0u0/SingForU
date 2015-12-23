import os
from subprocess import call
import wave
import pylab as pl
import numpy as np
import scipy.io.wavfile
import librosa

DATADIR = 'rawdata'
PROCESSDIR = 'processed_data'
MAXWORDS = 2
WINDOW = 100
MOVINGAVG = 30
INTERVAL = 0.1 # at least 0.1 sec a word?
THRESHOLD = 0.8
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
def breakDown(wave_data, dovisualize=False):        
    energy = []
    for i in range(0, len(wave_data), WINDOW):
        e = 0
        if len(wave_data)-i < WINDOW:
            e = getEnergy(wave_data[i:])
        else:
            e = getEnergy(wave_data[i:i+WINDOW])
        energy += [e]
    energy = movingAvg(energy, MOVINGAVG)
    interval = int(framerate*INTERVAL/WINDOW)
    threshold = getThreshold(energy, interval)
        
    bp = []
    i = interval/2
    while(i < len(energy) - interval/2):
        if(energy[i] < threshold[i]):
            min_i = findMin(energy, i-interval/2, i+interval/2)
            if(min_i == i):
                bp += [i*WINDOW-OFFSET]
                i += interval
            elif(min_i > i):
                i = min_i
                bp += [i*WINDOW-OFFSET]
                i += interval
        i += 1
    if dovisualize:
        visualize(energy, threshold, bp, framerate)
    return bp

if __name__ == '__main__':
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
        
        f = wave.open(os.path.join(DATADIR, name), "rb")
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        str_data = f.readframes(nframes)
        f.close()
        wave_data = np.fromstring(str_data, dtype=np.short)
        #wave_data.shape = -1, 2
        #wave_data = wave_data.T
        #if nchannels == 2:
        #    wave_data = wave_data[0]
        bp = breakDown(wave_data)
        bp = [0] + bp + [len(wave_data)]
        os.makedirs(os.path.join(PROCESSDIR, name))
        for i in range(0, len(bp)-1):
            left = bp[i]
            for j in range(1, MAXWORDS+1):
                if i+j >= len(bp):
                    break
                right = bp[i+j]
                out = np.int16(wave_data[left:right])
                t_name = os.path.join(PROCESSDIR, name, "%d_%d_%d.%s" % (left, right, j, ext))      
                scipy.io.wavfile.write(t_name, framerate, out)
                t = librosa.feature.mfcc(out, framerate)
                #print(t)
            
        print("processing %s DONE!" % name)
