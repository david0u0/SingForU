from subprocess import call
from features import *
import os

CDATA = 'clustered_data'
if not os.path.exists(CDATA):
	os.mkdir(CDATA)
chars = getCharArray('.')

os.chdir(CDATA)
for c in chars:
	dir_name = str(c.label)
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
	os.chdir(dir_name)
	call(['cp', c.url, c.getFilename()])
	os.chdir('..')