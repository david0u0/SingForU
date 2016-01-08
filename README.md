*Created by lturtsmuel & hank821017*

*Make the president of the United State speak for you!!*

# Data Preparing
Put .mp4 files in __video_data/__, and the corresponding .wav files in __rawdata/__. For example:

* video_data/
	- KP.mp4
	- Obama.mp4
* rawdata/
	- KP.wav
	- Obama.wav

Now run __$ python process_rawdata.py__, and u'll see all pieces of audio in __segmented_data/__.

*Note: When segmenting data, our program can visualize the process. Just look at functions __breakDown__ and __getActivity__!*


# Clustering
B4 audio matching, we have to cluster all pieces of audio. Just move all the segmented data you want into __ML/data/__.

Go to __ML/cluster/__ and run __$ python genDistMat.py__ to generate __distmtx.mat__ and __urls.mat__.

Than run complete cluster to generate a list of labels. The number of clusters is parametrized by the variable __threshold__.

The clustering may take long, but hell yeah, it's worth it (hopefully).

If u like to view the clusters directly, you may go to __ML/__ and run __$ python move_stuffs.py__


# Audio Matching
Record a sentence and save it somewhere, say __rawdata/yeee.wav__, then run

	$ python main.py rawdata/yeee.wav

And you will see an output video, __output.mp4__, where your sentence is composed of pieces of videos, sampled from KP or Obama. If not, try again, until u can finally persuade yourself: This is absolutely the sentence I spoke!

Have fun!


# reference
1. http://research.ijcaonline.org/volume40/number3/pxc3877167.pdf
1. http://statweb.stanford.edu/~dlsun/papers/voice_activity_detection_full.pdf
1. http://ms12.voip.edu.tw/~paul/Papper/Steganography/iLBC/%28VAD%29Real-Time_VAD_Algorithm.pdf