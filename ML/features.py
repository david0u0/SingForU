# -*- coding: utf8 -*-
import librosa
import numpy as np
import wave

NMFCC = 39
K = 20

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

def getDist(p1, p2):
	#Both of dimention NMFCC
	t = 0
	for i in range(1, NMFCC-1):
		a = (p1[i]-p1[i-1] + (p1[i+1]-p1[i-1])/2)/2
		b = (p2[i]-p2[i-1] + (p2[i+1]-p2[i-1])/2)/2
		t += (a-b)**2
	return t**0.5

def getDTW(mfcc1, mfcc2): #tail free!
	n = len(mfcc1.T)
	m = len(mfcc2.T)
	d = np.zeros(shape=(n, m))
	recurdiveGetDTW(n-1, m-1, d, mfcc1, mfcc2)
	mini = np.inf
	for i in range(0, n):
		mini = min(mini, d[i][m-1])
	for i in range(0, m):
		mini = min(mini, d[n-1][i])
	return mini/(m+n)

def recurdiveGetDTW(i, j, d, mfcc1, mfcc2):
	if d[i][j] != 0:
		return d[i][j]
	if i == j and i == 0:
		return 0
	if i < 0 or j < 0:
		return np.inf
	a = recurdiveGetDTW(i-1, j, d, mfcc1, mfcc2)
	b = recurdiveGetDTW(i, j-1, d, mfcc1, mfcc2)
	c = recurdiveGetDTW(i-1, j-1, d, mfcc1, mfcc2)
	d[i][j] = min(a, b, c) + getDist(mfcc1.T[i], mfcc2.T[j])
	return d[i][j]

def classify(chars, char):
	d = {}
	cnt = 0
	name = None
	for c in chars:
		if c.url == char.url:
			continue
		dist = getDTW(c.mfcc, char.mfcc)
		if c.name not in d:
			if name:
				d[name] /= cnt
			d[c.name] = 0
			cnt = 0
		cnt += 1
		name = c.name
		d[name] += dist

	for k in d:
		print("%s, %f" % (k, d[k]))
	print("%s, %f" % (char.name, d[char.name]))
