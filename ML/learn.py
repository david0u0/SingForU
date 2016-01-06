# -*- coding: utf8 -*-
from os import path, listdir, chdir
import sklearn
from features import *

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

'''for i in range(0, len(chars)):
	for j in range(i+1, len(chars)):
		CharPair(chars[i], chars[j])
#	print(char.name)'''
print('=====')
kNN(chars, chars[0])
print('=====')
kNN(chars, chars[1])
print('=====')
kNN(chars, chars[2])
print('=====')
kNN(chars, chars[3])
print('=====')
kNN(chars, chars[4])
print('=====')
kNN(chars, chars[5])
print('=====')
kNN(chars, chars[6])
print('=====')
kNN(chars, chars[7])
print('=====')
kNN(chars, chars[8])
