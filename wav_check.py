#!/usr/bin/python

import sys, os, subprocess
   
def runScript():
	if len(sys.argv) != 2:
			print('wav_check.py <directory to scan>')
			sys.exit(2)

	dir = sys.argv[1]

	# Walk directory tree
	for root_dir, subdir_list, file_list in os.walk(dir):
		for file_name in file_list:
			# WAVs only
			if os.path.splitext(file_name)[1].lower() == '.wav':
				full_path = os.path.join(root_dir,file_name)
				success = checkWAV(full_path)
				
				if success:
					print(full_path + ' - OK')
				else:
					print(full_path + ' - FAIL', file=sys.stderr)

def checkWAV(file_path):
	# Read the file from beginning to end and pipe to null
	process = subprocess.run(['ffmpeg','-i',file_path,'-f','null','-'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	# Get ffmpeg return code
	return (process.returncode == 0)
	
runScript()

