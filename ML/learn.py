# -*- coding: utf8 -*-
from os import path, listdir, chdir
import sklearn
from features import *

class Char:
	def __init__(self, name, url):
		self.name = name.encode('big5')
		self.url = url
		(y, fs) = getSignal(url)	
		self.mfcc = getMFCC(y, fs)
class CharPair:
	def __init__(self, c1, c2):
		self.label = (c1.name == c2.name)
		self.url1 = c1.url
		self.url2 = c2.url
		self.dist = getDTW(c1.mfcc, c2.mfcc)
		print("%f %s %s %s" % (self.dist, c1.name, c2.name, self.label))

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

for char in chars:
	print(char.name)
	kNN(chars, char)