from process_rawdata import *
from features import *
import sys
from os import path, mkdir

OUTDIR = 'output'

argv = sys.argv[-1]
if not path.exists(OUTDIR):
	mkdir(OUTDIR)
print(argv)
