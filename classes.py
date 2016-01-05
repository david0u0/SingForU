import os

DATADIR = 'rawdata'
PROCESSDIR = 'processed_data'

class Segment:
	def __init__(self, bp=None, s=None, name=None):
		count = start = end = 1
		if bp:
			count = len(bp)+1
			start = bp[0]
			end = bp[-1]
		else:
			[start, end, count] = [int(e) for e in s.split('_')]
		self.start = start
		self.end = end
		self.count = count
		self.name = name
		if name: #it is in db, read mfcc
			self.mfcc = Mfcc(name, start, end, count)
		else: #it is a new input, compute mfcc
			pass
	def isMergable(self, seg):
		if s1.name == s2.name:
			return (s1.end == s2.start)
		return False
	def merge(self, seg):
		if self.isMergable(seg):
			self.count += seg.count
			self.end = seg.end
			self.mfcc = Mfcc(self.name, self.start, self.end, self.count)

class Mfcc:
	def readFromData(name, start, end, count):
		t_name = os.path.join(PROCESSDIR, name, "%d_%d_%d"%(start, end, count))
		f = open(t_name, 'r')
		t = f.readline()
		mfcc = 1
		mfcc.data = []
		while(t != ''):
			a = [int(e) for e in t.split(',')]
			mfcc.data += [a]
			t = f.readline()
		return mfcc
	def __init__(self, sig):
		t_name = os.path.join(PROCESSDIR, name, "%d_%d_%d"%(start, end, count))
		f = open(t_name, 'r')
		t = f.readline()
		self.data = []
		while(t != ''):
			a = [int(e) for e in t.split(',')]
			self.data += [a]
			t = f.readline()

	def getDist(self, mfcc):
		pass
		
