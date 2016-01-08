# -*- coding: utf8 -*-
from os import path, listdir, chdir
import sklearn
import numpy
import scipy.io as sio
import sys
sys.path.append('..')
from features import *

chars = []
chdir('../data')
for url in listdir('.'):
	char = Char(None, path.abspath(url))
	chars += [char]
chdir('../clustering')

# save .mat
size = len(chars)
dists = numpy.zeros((size,size))
urls = []


for row_i in range(size):
	char1 = chars[row_i]
	urls.append(char1.getFilename)
	for col_j in range(row_i+1, size):
		char2 = chars[col_j]
		dist = getDTW(char1.mfcc, char2.mfcc)
		dists[row_i][col_j] = dist
		dists[col_j][row_i] = dist
	print("%d char DONE" % row_i)


sio.savemat('urls.mat', mdict={'urls':urls})
sio.savemat('distmtx.mat', mdict={'distmtx':dists})