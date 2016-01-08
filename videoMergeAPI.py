#written by PH Chen 2016.1.7
from moviepy.editor import *
from os import path

VIDEODIR = 'video_data'

def videoMergeAPI(clipList, outputName='output.mp4'):
	num_clips = len(clipList)
	merged_video = []

	for clip_info in clipList:
		start_t   = clip_info[0]
		end_t     = clip_info[1]
		videoPath = path.join(VIDEODIR, clip_info[2])
		temp_video_clip = VideoFileClip(videoPath).subclip(start_t, end_t)
		merged_video.append(temp_video_clip)

	result = concatenate_videoclips(merged_video)
	result.write_videofile(outputName)