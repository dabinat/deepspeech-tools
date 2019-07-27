#!/usr/bin/python

import sys, getopt, os
   
def runScript():
	dest_file = ''

	try:
		opts, args = getopt.getopt(sys.argv[1:],"d",["dest="])
	except getopt.GetoptError:
		print(sys.argv[0] + ' --dest <combined csv file> <input file(s)>')
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(sys.argv[0] + ' --dest <combined csv file> <input file(s)>')
			sys.exit()
		elif opt in ("-d", "--dest"):
			dest_file = arg

	# Open output CSV
	f_out = open(dest_file,"w")
	f_out.write("wav_filename,wav_filesize,transcript\n")

	# Loop through all files on command-line
	for opt in sys.argv[1:]:
		if os.path.exists(opt) and not opt == dest_file:
			with open(opt) as f:  			
				for line in f:
					# Skip headers
					if line.strip() == "wav_filename,wav_filesize,transcript":
						continue

					# Make sure paths are absolute
					components = line.split(",")
					
					if len(components) != 3:
						print("Invalid line")
						continue

					file_path = components[0]
					
					if not file_path[0:1] == "/":
						# Is not absolute
						parent_path = os.path.dirname(opt)

						if not parent_path[0:1] == "/":
							# Parent path is not absolute either
							parent_path = os.path.abspath(parent_path)
						
						file_path = os.path.join(parent_path,file_path)

						line = file_path + "," + components[1] + "," + components[2]

					f_out.write(line)

				f.close()
	
	f_out.close()
	
runScript()

