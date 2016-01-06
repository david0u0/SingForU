from sklearn import svm
import random
from features import *

FRACTION = 0.1

(feats, labels) = readFeats()
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
clf = svm.SVC()
clf.fit(train_f, train_l)

print('start testing...')
predicted_l = clf.predict(val_f)
for i in range(0, len(val_l)):
	print("%d %d", val_l[i], predicted_l[i])

