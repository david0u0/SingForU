# -*- coding: utf8 -*-
import scipy
import librosa
import numpy as np
import wave
from os import path, listdir

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
		return [start, end, video]
	@staticmethod
	def createFromSig(y, fs):
		t = type('Char', (), {})()
		t.label = 'unknown'
		t.url = ''
		t.mfcc = getMFCC(y, fs)
		return t

class Dictionary:
	def __init__(self):
		self.sum = {}
		self.cnt = {}
		self._min = {}
		self._min_chars = {}
	def addChar(self, char, dist):
		label = char.label
		if label not in self._min:
			self.sum[label] = dist
			self.cnt[label] = 1
			self._min[label] = dist
			self._min_chars[label] = char
		else:
			self.sum[label] += dist
			self.cnt[label] += 1
			if dist < self._min[label]:
				self._min[label] = dist
				self._min_chars[label] = char
	def getClassifiedChar(self):
		min_avg_dist = np.inf
		classified_char = None
		for k in self._min:
			if(self.sum[k]/self.cnt[k] < min_avg_dist):
				min_avg_dist = self.sum[k]/self.cnt[k]
				classified_char = self._min_chars[k]
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
	mfcc = librosa.feature.mfcc(y, framerate, n_mfcc=NMFCC)
	mfcc_delta = librosa.feature.delta(mfcc)
	mfcc_2delta = librosa.feature.delta(mfcc_delta)
	return mfcc + mfcc_delta*0.6 + mfcc_2delta*0.3

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
	if m > n: # I want n to be bigger!
		[mfcc1, mfcc2] = [mfcc2, mfcc1]
		[m, n] = [n, m]
	d = np.zeros(shape=(n, m)) + np.inf
	wall = int(m/2)
	new_n = m-1+wall
	if new_n > n-1:
		new_n = n-1
	recursiveGetDTW(new_n, m-1, d, mfcc1, mfcc2, wall)
	mini = np.inf
	for i in range(0, new_n):
		mini = min(mini, d[i][m-1])
	for i in range(0, m):
		mini = min(mini, d[n-1][i])
	return mini/(m+n+1)

def recursiveGetDTW(i, j, d, mfcc1, mfcc2, wall):
	if abs(i-j) > wall or i < 0 or j < 0:
		return np.inf
	if i == j and i == 0:
		return 0
	if d[i][j] != np.inf:
		return d[i][j]
	a = recursiveGetDTW(i-1, j, d, mfcc1, mfcc2, wall)
	b = recursiveGetDTW(i, j-1, d, mfcc1, mfcc2, wall)
	c = recursiveGetDTW(i-1, j-1, d, mfcc1, mfcc2, wall)
	d[i][j] = min(a, b, c) + getDist(mfcc1.T[i], mfcc2.T[j])
	return d[i][j]

def classify(chars, char):
	d = Dictionary()
	label = None
	for c in chars:
		if c.url == char.url:
			continue
		dist = getDTW(c.mfcc, char.mfcc)
		d.addChar(c, dist)
	return d.getClassifiedChar()

def getCharArray(url):
	chars = []
	for name in listdir(path.join(url, 'data')):
		p = path.join(url, 'data', name)
		chars += [Char(name[0], path.abspath(p))]
	return chars