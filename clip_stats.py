#!/usr/bin/python

import sys, os, subprocess

file_count = 0
total_size = 0
total_duration = 0
no_estimate = False

def runScript():
	global file_count, total_size, total_duration, no_estimate

	if len(sys.argv) < 2:
		print('clip_stats.py [--no-estimate] <directory to scan or CSV file>')
		sys.exit(2)

	if "--no-estimate" in sys.argv:
		no_estimate = True

	dir = sys.argv[-1]
	split_ext = os.path.splitext(dir)

	if len(split_ext) > 0 and split_ext[1].lower() == '.csv':
		# Parse CSV
		with open(dir) as f:  			
			for line in f:
				components = line.split(",")

				if len(components) != 3:
					print("Invalid line")
					continue
				
				if os.path.exists(components[0]):
					checkFile(components[0])
	else:
		# Walk directory tree
		for root_dir, subdir_list, file_list in os.walk(dir):
			for file_name in file_list:
				# WAVs only
				if os.path.splitext(file_name)[1].lower() == '.wav':
					full_path = os.path.join(root_dir,file_name)				
					checkFile(full_path)

	# Print final total without carriage return
	print("Found {0} files, {1:.2f} MB, {2:.2f} hours".format(file_count,total_size,(total_duration/60/60)))

def getDuration(file_path):
	global no_estimate

	if not no_estimate:
		# Assume 16-bit, 16000 Hz mono
		file_size = os.path.getsize(file_path)
		return file_size/(2*16000)
	else:
		# Actually get the file's duration
		return float(str(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',file_path]),"utf-8"))

def checkFile(file_path):
	global file_count, total_size, total_duration

	file_count += 1
	total_duration += getDuration(file_path)
	total_size += os.path.getsize(file_path)/1024/1024

	print("Found {0} files, {1:.2f} MB, {2:.2f} hours".format(file_count,total_size,(total_duration/60/60)), end="\r")

	
runScript()

