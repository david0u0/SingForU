# -*- coding: utf8 -*-
from os import path, listdir, chdir
import sklearn
import numpy
import scipy.io as sio
from features import *

chars = []
chdir('data')
for d in listdir('.'):
	chdir(d)
	for url in listdir('.'):
		char = Char(d, path.abspath(url))
		chars += [char]
	chdir('..')
chdir('..')

# save .mat
size = len(chars)
dists = numpy.zeros((size,size))
urls = []


for row_i in range(size):
	char1 = chars[row_i]
	urls.append(char1.url.split('\\')[-1])
	for col_j in range(row_i+1,size):
		char2 = chars[col_j]
		dist = getDTW(char1.mfcc, char2.mfcc)
		dists[row_i][col_j] = dist
		dists[col_j][row_i] = dist


sio.savemat('urls.mat', mdict={'urls':urls})
sio.savemat('distmtx.mat', mdict={'distmtx':dists})