#!/usr/bin/python

import sys, getopt, os
   
def runScript():
	source_file = ""
	dest_file = ""
	purge_file = ""
	purge_list = []
	purge_count = 0

	try:
		opts, args = getopt.getopt(sys.argv[1:], "s:d:p", ["source=", "dest=", "purge-list="])
	except getopt.GetoptError:
		print(os.path.basename(sys.argv[0]) + " --source <source csv file> --dest <dest csv file> --purge-list <txt or csv of filenames to purge>")
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(os.path.basename(sys.argv[0]) + " --source <source csv file> --dest <dest csv file> --purge-list <txt or csv of filenames to purge>")
			sys.exit()
		elif opt in ("-s", "--source"):
			source_file = arg
		elif opt in ("-d", "--dest"):
			dest_file = arg
		elif opt in ("-p", "--purge-list"):
			purge_file = arg

	# Cache purge filenames in array
	with open(purge_file) as f:  			
		for line in f:
			items = line.split(",")

			if len(items) > 0 and len(items[0].strip()) > 0:
				purge_list.append(items[0].strip().lower())

		f.close()

	# Open output CSV
	f_out = open(dest_file,"w")

	# Loop through input CSV
	with open(source_file) as f:  			
		for line in f:
			items = line.split(",")
			
			if len(items) != 3:
				print("Invalid line")
				continue

			file_path = items[0].strip().lower()

			if file_path in purge_list:
				purge_count += 1
				continue
			
			# Compare just the filename
			file_name = os.path.basename(file_path)

			if file_name in purge_list:
				purge_count += 1
				continue
			
			# No match so write out the line
			f_out.write(line)

		f.close()
	
	f_out.close()

	print("{} line{} purged".format(purge_count,"s" if purge_count != 1 else ""))
	
runScript()

