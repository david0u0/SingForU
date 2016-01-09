#written by PH Chen 2016.1.7
import moviepy.editor as mpy
from os import path

VIDEODIR = 'video_data'

def videoMergeAPI(clipList, outputName='output.mp4'):
	num_clips = len(clipList)
	merged_video = []

	for i in range(1,num_clips):
		# this clip's time
		ctime = clipList[i][3]
		
		# should process previous clip
		clip_info = clipList[i-1]
		start_t   = clip_info[0]
		end_t     = clip_info[1]
		videoPath = path.join(VIDEODIR, clip_info[2])
		ptime     = clip_info[3]

		# cut the clip with respect to (start_t,end_t) pair
		temp_video_clip = mpy.VideoFileClip(videoPath).subclip(start_t, end_t)
		merged_video.append(temp_video_clip)

		# if the duration is larger, compensate the blank time
		duration = ctime - ptime
		if duration >= (end_t-start_t):
			blank_duration = duration - (end_t-start_t) # blank time
			temp_pic = mpy.VideoFileClip(videoPath).get_frame(end_t) # get last frame, which is global
			blank_clip = mpy.ImageClip(temp_pic, duration=blank_duration) # create a blank video
			merged_video.append(blank_clip)

	# process the last clip
	clip_info = clipList[-1]
	start_t   = clip_info[0]
	end_t     = clip_info[1]
	videoPath = path.join(VIDEODIR, clip_info[2])
	# cut the clip with respect to (start_t,end_t) pair
	temp_video_clip = mpy.VideoFileClip(videoPath).subclip(start_t, end_t)
	merged_video.append(temp_video_clip)

	result = mpy.concatenate_videoclips(merged_video)
	result.write_videofile(outputName, fps=24)
	