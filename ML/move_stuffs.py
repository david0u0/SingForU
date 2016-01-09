from subprocess import call
from features import *
import os
import sys

CDATA = 'clustered_'+sys.argv[-1]
if os.path.exists(CDATA):
	call(['rm', CDATA, '-rf'])
os.mkdir(CDATA)
chars = getCharArray('.', sys.argv[-1])

os.chdir(CDATA)
for c in chars:
	dir_name = str(c.label)
	if not os.path.exists(dir_name):
		os.mkdir(dir_name)
	os.chdir(dir_name)
	call(['cp', c.url, c.getFilename()])
	os.chdir('..')