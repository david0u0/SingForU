import numpy as np
import pylab as pl

LEN = 0.01 # sec
ENERGY_PRIME_THRES = 10**5
F_PRIME_THRES = 50
SMF_PRIME_THRES = 7

def getActivity(y, fs, visualize=False):
	window = int(fs*LEN)
	(energy, smf, f) = ([], [], [])
	for i in range(0, len(y)-window, window):
		tmp = y[i:window+i]
		energy.append(getEnergy(tmp))
		tmp = np.fft.fft(tmp)
		tmp = abs(tmp[0:window/2])
		#smf.append(getSMF(tmp))
		f.append(getF(tmp))
	min_e = min(energy[1:])
	min_f = min(f[1:])
	#min_s = min(smf[1:])
	thresh_e = ENERGY_PRIME_THRES*np.log10(min_e)
	thresh_f = F_PRIME_THRES
	#thresh_s = SMF_PRIME_THRES
	active = [True] * len(f)
	count_silence = 0
	for i in range(0, len(f)):
		count = 0
		if(energy[i]-min_e >= thresh_e):
			count += 1
		if(f[i]-min_f <= thresh_f):
			count += 1
		'''if(smf[i]-min_s >= thresh_s):
			count += 1'''
		if count <= 1:
			count_silence += 1
			active[i] = False
			min_e = ((count_silence*min_e)+energy[i])/(count_silence+1)
			thresh_e = ENERGY_PRIME_THRES*np.log10(min_e)
	start = -1
	for i in range(0, len(active)):
		if active[i] and start == -1:
			start = i
		elif not active[i]:
			if(i - start < 4):
				for j in range(start, i):
					active[j] = False
			start = -1
	if visualize:
		time = np.arange(0, len(energy)) * LEN
		pl.subplot(513)
		pl.plot(time, energy)
		pl.title('Energy')
		pl.subplot(512)
		pl.plot(time, f)
		pl.title('F')
		#pl.subplot(511)
		#pl.plot(time, smf)
		#pl.title('SMF')
		pl.subplot(515)
		active = [100 if a else 0 for a in active]
		active[0] = 150
		active[-1] = -50
		pl.plot(time, active)
		pl.subplot(514)
		time = np.arange(0, len(y))*1.0/fs
		pl.plot(time, y)
		pl.show()
	return (active, window)

def getEnergy(y):
	return sum([int(t)**2 for t in y])/len(y)

def getF(f):
	f = list(f)
	return f.index(max(f))

def getSMF(f):
	am = sum(f)/len(f)
	log_gm = sum(np.log10(f))/len(f)
	return 10*(log_gm-np.log10(am))

def isActive(active): #for a char
	cnt = 0
	for a in active:
		if a:
			cnt += 1
	return (cnt > len(active)/3)