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

chars = getCharArray('ML')

(wave_data, framerate) = getSignal(arg)

print('===')
(active, window) = getActivity(wave_data, framerate)

bp = breakDown(wave_data, framerate)
bp = bp + [len(wave_data)]
chdir(OUTDIR)
clip_list = []
for i in range(0, len(bp)-1):
	y = wave_data[bp[i]:bp[i+1]]
	a = active[int(bp[i]/window):int(bp[i+1]/window)]
	if not isActive(a):
		print("%d inactive" % i)
		continue # or add some cirtain thing
	char = Char.createFromSig(y, framerate)
	c = classify(chars, char)
	clip_list += [c.getVideoInfo()]
	call(['cp', c.url, 'matched%d.wav' % i])
	scipy.io.wavfile.write('%d.wav'%i, framerate, y)
	print("%d matched" % i)
chdir('..')
videoMergeAPI(clip_list)