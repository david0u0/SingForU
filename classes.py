class Word:
	def __init__(self, start, end, speech_index, index):
		this.start = start
		this.end = end
		this.speech_index = speech_index
		this.index = index
	def getName(self):
		return str(self.speech_index) + '_' + str(self.index)

class Mfcc:
	def __init__(self, name):
		(self.speech_index, self.index) = name.split('_')
		#read those fuckin properties
	def getDist(self, mfcc):
		pass
		