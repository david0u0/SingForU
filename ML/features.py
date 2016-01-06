# -*- coding: utf8 -*-
import librosa
import numpy as np
import wave
from os import listdir, path

NMFCC = 39

def getSignal(url):
	f = wave.open(url, "rb")
	params = f.getparams()
	nchannels, sampwidth, framerate, nframes = params[:4]
	str_data = f.readframes(nframes)
	f.close()
	y = np.fromstring(str_data, dtype=np.short)
	if nchannels == 2:
		y.shape = -1, 2
		y = y.T
		y = y[0]
	return (y, framerate)

def getMFCC(y, framerate, path=None):
	return librosa.feature.mfcc(y, framerate, n_mfcc=NMFCC)

def get2dDist(p1, p2, i):
	if i == 0 or i == NMFCC-1:
		a = p1[i]
		b = p2[i]
	else:
		a = (p1[i]-p1[i-1] + (p1[i+1]-p1[i-1])/2)/2
		b = (p2[i]-p2[i-1] + (p2[i+1]-p2[i-1])/2)/2
	return (p1[i]-p2[i])**2

def getDist(p1, p2):
	#Both of dimention NMFCC
	t = 0
	for i in range(0, NMFCC):
		t += get2dDist(p1, p2, i)
	return t**0.5

(LEFT, DOWN, DIA) = (0, 1, 2)
def getDTW(mfcc1, mfcc2):
	n = len(mfcc1.T)
	m = len(mfcc2.T)
	d = np.zeros(shape=(n, m))
	trace = np.zeros(shape=(n, m))
	recurdiveGetDTW(n-1, m-1, d, trace, mfcc1, mfcc2)
	mini = np.inf
	#### tail free?? ####
	#for i in range(0, n):
	#	mini = min(mini, d[i][m-1])
	#for i in range(0, m):
	#	mini = min(mini, d[n-1][i])
	features = np.zeros(NMFCC)
	(i, j, cnt) = (n-1, m-1, 0)
	while(True):
		cnt += 1
		for k in range(0, NMFCC):
			x = (mfcc1[k][i]-mfcc2[k][j])**2
			features[k] += x
		if(i == j and i == 0):
			break
		if trace[i][j] == LEFT or j == 0:
			i -= 1
		elif trace[i][j] == DOWN or i == 0:
			j -= 1
		else:
			i -= 1
			j -= 1
	return features/cnt

def recurdiveGetDTW(i, j, d, trace, mfcc1, mfcc2):
	if d[i][j] != 0:
		return d[i][j]
	if i == j and i == 0:
		return 0
	if i < 0 or j < 0:
		return np.inf
	a = recurdiveGetDTW(i-1, j, d, trace, mfcc1, mfcc2)
	b = recurdiveGetDTW(i, j-1, d, trace, mfcc1, mfcc2)
	c = recurdiveGetDTW(i-1, j-1, d, trace, mfcc1, mfcc2)
	tmp = min(a, b, c)
	d[i][j] = tmp + getDist(mfcc1.T[i], mfcc2.T[j])
	trace[i][j] = [a, b, c].index(tmp)
	return d[i][j]

def saveFeats(feat, label, i):
	f = open(path.join('feats', str(i)), 'w')
	f.write(str(label)+' ')
	for t in feat:
		f.write(str(t)+' ')
	f.close()

def readFeats():
	feats = []
	labels = []
	for fname in listdir('feats'):
		f = open(path.join('feats', fname), 'r')
		s = f.read()
		a = s.split(' ')
		labels += [int(a[0])]
		feat = [float(t) for t in a[1:-1]]
		feats += [feat]
		
	return (feats, labels)