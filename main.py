from videoMergeAPI import *
from voice_activity import getActivity, isActive
from process_rawdata import *
import sys
sys.path.append('ML')
from features import *
from os import path, mkdir, chdir, listdir

OUTDIR = 'output'

arg = sys.argv[-1]
if not path.exists(OUTDIR):
	mkdir(OUTDIR)

chars = []
chdir('ML/data')
for d in listdir('.'):
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

print('===')
(active, window) = getActivity(wave_data, framerate)

bp = breakDown(wave_data, framerate)
bp = bp + [len(wave_data)]
chdir(OUTDIR)
for i in range(0, len(bp)-1):
	y = wave_data[bp[i]:bp[i+1]]
	a = active[int(bp[i]/window):int(bp[i+1]/window)]
	if not isActive(a):
		print("%d inactive" % i)
		continue # or add some cirtain thing
	char = Char.createFromSig(y, framerate)
	c = kNN(chars, char)
	call(['cp', c.url, 'matched%d.wav' % i])
	scipy.io.wavfile.write('%d.wav'%i, framerate, y)
	print("%d matched" % i)