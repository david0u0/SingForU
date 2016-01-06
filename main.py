from process_rawdata import *
from features import *
import sys
from os import path, mkdir, chdir, listdir

OUTDIR = 'output'

arg = sys.argv[-1]
if not path.exists(OUTDIR):
	mkdir(OUTDIR)

chars = []
chdir('ML/data')
for d in listdir('.'):
	d = d.decode('big5')
	chdir(d)
	for url in listdir('.'):
		char = Char(d, path.abspath(url))
		chars += [char]
	chdir('..')
chdir('../..')

f = wave.open(arg, "rb")
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes)
f.close()
wave_data = np.fromstring(str_data, dtype=np.short)
if nchannels == 2:
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    wave_data = wave_data[0]

bp = breakDown(wave_data, framerate)
bp = bp + [len(wave_data)]

for i in range(0, len(bp)-1):
	y = wave_data[bp[i]:bp[i+1]]
	char = Char.createFromSig(y, framerate)
	kNN(chars, char)
	