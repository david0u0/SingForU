# -*- coding: utf8 -*-
from os import path, listdir, chdir
import sklearn
from features import *
from sklearn import svm

class Char:
	def __init__(self, name, url):
		self.name = name.encode('big5')
		self.url = url
		(y, fs) = getSignal(url)	
		self.mfcc = getMFCC(y, fs)
class CharPair:
	def __init__(self, c1, c2):
		if c1.name == c2.name:
			self.label = 1
		else:
			self.label = -1
		self.url1 = c1.url
		self.url2 = c2.url
		self.feat = getDTW(c1.mfcc, c2.mfcc)

chars = []
chdir('data')
for d in listdir('.'):
	d = d.decode('big5')
	chdir(d)
	for url in listdir('.'):
		char = Char(d, path.abspath(url))
		chars += [char]
	chdir('..')
chdir('..')
pairs = []
cnt = 0
print(len(chars))
for i in range(0, len(chars)):
	for j in range(i+1, len(chars)):
		pair = CharPair(chars[i], chars[j])
		pairs += [pair]
		saveFeats(pair.feat, pair.label, cnt)
		cnt += 1
feats = [p.feat for p in pairs]
labels = [p.label for p in pairs]

clf = svm.SVC()
clf.fit(feats, labels)