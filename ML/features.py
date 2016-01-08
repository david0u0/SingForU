# -*- coding: utf8 -*-
import scipy
import librosa
import numpy as np
import wave
from os import path

NMFCC = 13
K = 7

class Char:
	def __init__(self, label, url):
		self.label = label
		self.url = url
		(y, fs) = getSignal(url)	
		self.mfcc = getMFCC(y, fs)
		self.fs = fs
	def getFilename(self):
		return path.split(self.url)[-1]
	def getVideoInfo(self):
		p = self.getFilename()
		[start, end, video] = p.split('_')
		start = float(start)/self.fs
		end = float(end)/self.fs
		video = video.split('.')[0] + '.mp4'
		return (start, end, video)
	@staticmethod
	def createFromSig(y, fs):
		t = type('Char', (), {})()
		t.label = 'unknown'
		t.url = ''
		t.mfcc = getMFCC(y, fs)
		return t

class Dictionary:
	def __init__(self):
		self.max = {}
		self.min = {}
		self.min_chars = {}
	def addChar(self, char, dist):
		label = char.label
		if label not in self.max:
			self.max[label] = dist
			self.min[label] = dist
			self.min_chars[label] = char
		else:
			if dist > self.max[label]:
				self.max[label] = dist
			elif dist < self.min[label]:
				self.min[label] = dist
				self.min_chars[label] = char
	def getClassifiedChar(self):
		min_max_dist = np.inf
		classified_char = None
		for k in self.max:
			if(self.max[k] < min_max_dist):
				min_max_dist = self.max[k]
				classified_char = self.min_chars[k]
		return classified_char

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

def getDTW(mfcc1, mfcc2): #tail free!?
	n = len(mfcc1.T)
	m = len(mfcc2.T)
	d = np.zeros(shape=(n, m))-1
	cnt = np.zeros(shape=(n, m))-1
	recursiveGetDTW(n-1, m-1, d, cnt, mfcc1, mfcc2)

	mini = np.inf
	for i in range(0, n):
		mini = min(mini, d[i][m-1])
	for i in range(0, m):
		mini = min(mini, d[n-1][i])
	return mini

def recursiveGetDTW(i, j, d, cnt, mfcc1, mfcc2):
	if i < 0 or j < 0:
		return np.inf
	if i == j and i == 0:
		cnt[0][0] = 0
		return 0
	if d[i][j] > 0:
		return d[i][j]

	a = recursiveGetDTW(i-1, j, d, cnt, mfcc1, mfcc2)
	b = recursiveGetDTW(i, j-1, d, cnt, mfcc1, mfcc2)
	c = recursiveGetDTW(i-1, j-1, d, cnt, mfcc1, mfcc2)
	dist = getDist(mfcc1.T[i], mfcc2.T[j])
	if i > 0:
		a = (cnt[i-1][j]*a + dist)/(1+cnt[i-1][j])
		if j > 0:
			c = (cnt[i-1][j-1]*c + dist)/(1+cnt[i-1][j-1])
	if j > 0:
		b = (cnt[i][j-1]*b + dist)/(1+cnt[i][j-1])
	d[i][j] = min(a, b, c)
	index = [a, b, c].index(d[i][j])
	if index == 0:
		cnt[i][j] = cnt[i-1][j] + 1
	elif index == 1:
		cnt[i][j] = cnt[i][j-1] + 1
	else:
		cnt[i][j] = cnt[i-1][j-1] + 1
	return d[i][j]

def classify(chars, char):
	d = Dictionary()
	cnt = 0
	label = None
	for c in chars:
		if c.url == char.url:
			continue
		dist = getDTW(c.mfcc, char.mfcc)
		d.addChar(c, dist)
	return d.getClassifiedChar()
