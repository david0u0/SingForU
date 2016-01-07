#written by PH Chen 2016.1.7
from moviepy.editor import *

def videoMergeAPI(clipList, outputName):
	num_clips = len(clipList)
	merged_video = []


	for clip_index in range(num_clips):
		clip_info = clipList[clip_index]
		start_t   = clip_info[0]
		end_t     = clip_info[1]
		videoPath = clip_info[2]
		temp_video_clip = VideoFileClip(videoPath).subclip(start_t, end_t)
		merged_video.append(temp_video_clip)

	result = concatenate_videoclips(merged_video)
	result.write_videofile(outputName)