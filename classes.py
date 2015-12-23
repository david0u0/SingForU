def _isMergable(s1, s2):
	if s1.name == s2.name:
		if s1s2.end == s2.start:
			return True
		elif s1s2.start == s2.end:
			return True
	return False

class Segment:
	def __init__(self, s=None, bp=None, name=None):
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
		if name: #it is in db
			pass
		else: #it is a new input
			pass
	def isMergable(self, sound):
		return _isMergable(self, sound)



class Mfcc:
	def __init__(self, name):
		(self.speech_index, self.index) = name.split('_')
		#read those fuckin properties
	def getDist(self, mfcc):
		pass
		