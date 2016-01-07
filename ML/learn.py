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
