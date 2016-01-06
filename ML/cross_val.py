from sklearn import svm
import random
from features import *

FRACTION = 0.1

(feats, labels) = readFeats()
feats = feats[0:7000]
labels = labels[0:7000]

n = len(labels)
n_val = int(n*FRACTION)
a = [(random.random(), i) for i in range(0, n)]
a = sorted(a, key=lambda x : x[0])
a = [t[1] for t in a[0:n_val]]

train_f = []
train_l = []
val_f = []
val_l = []
for i in range(0, n):
	if(i in a):
		val_f += [feats[i]]
		val_l += [labels[i]]
	else:
		train_f += [feats[i]]
		train_l += [labels[i]]

print('start training...')
clf = svm.SVC(class_weight={1: 0.001})
clf.fit(train_f, train_l)
#clf.fit(feats, labels)

print('start testing...')
predicted_l = clf.predict(val_f)
confs = clf.decision_function(val_f)
pos = true_pos = neg = false_pos = 0
for i in range(0, len(val_l)):
	print("%d %d %f" % (val_l[i], predicted_l[i], confs[i]))
	# The goal is true positive rate!!
	if(val_l[i] == 1):
		pos += 1
		if(predicted_l[i] == 1):
			true_pos += 1
	else:
		neg += 1
		if(predicted_l[i] == 1):
			false_pos += 1

print('tp rate: %d/%d' % (true_pos, pos))
print('fp rate: %d/%d' % (false_pos, neg))