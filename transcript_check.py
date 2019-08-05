#!/usr/bin/python

import sys, getopt, os, subprocess

csv_path = ""
model_dir = ""
model_path = ""
alphabet_path = ""
lm_path = ""
trie_path = ""
threshold = 0.3
min_word_diff = 2
start_line = 1
   
def runScript():
	global csv_path, model_dir, model_path, alphabet_path, lm_path, trie_path, threshold, min_word_diff, start_line

	try:
		opts, args = getopt.getopt(sys.argv[1:], [], ["input=", "model-dir=", "model=", "alphabet=", "lm=", "trie=", "threshold=", "min-word-diff=", "start-line="])
	except getopt.GetoptError:
		print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model-dir <dir> [--threshold <float>] [--min-word-diff <int>] [--start-line <int>]\n")
		print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model <model> --alphabet <alphabet> --lm <lm> --trie <trie> " + \
		"[--threshold <float>] [--min-word-diff <int>] [--start-line <int>]")
		print("\n--model-dir: A directory containing a mode, alphabet, language model and trie")
		print("--threshold: Percentage difference in trancript word count required to flag up a file (default is 0.3)")
		print("--min-word-diff: Minimum number of words to have changed in order to flag up a file (default is 2)")
		print("--start-line: Start processing at a specific line in the file. The first line starts at 1.")
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model-dir <dir> [--threshold <float>] [--min-word-diff <int>] [--start-line <int>]\n")
			print(os.path.basename(sys.argv[0]) + " --input <CSV path> --model <model> --alphabet <alphabet> --lm <lm> --trie <trie> " + \
			"[--threshold <float>] [--min-word-diff <int>] [--start-line <int>]")
			print("\n--model-dir: A directory containing a mode, alphabet, language model and trie")
			print("--threshold: Percentage difference in trancript word count required to flag up a file (default is 0.3)")
			print("--min-word-diff: Minimum number of words to have changed in order to flag up a file (default is 2)")
			print("--start-line: Start processing at a specific line in the file. The first line starts at 1.")
			sys.exit()
		elif opt == "--input":
			csv_path = arg
		elif opt == "--model-dir":
			model_dir = arg
		elif opt == "--model":
			model_path = arg
		elif opt == "--alphabet":
			alphabet_path = arg
		elif opt == "--lm":
			lm_path = arg
		elif opt == "--trie":
			trie_path = arg
		elif opt == "--threshold":
			threshold = float(arg)
		elif opt == "--min-word-diff":
			min_word_diff = int(arg)
		elif opt == "--start-line":
			start_line = int(arg)
			if start_line <= 0:
				start_line = 1 

	if model_dir != "":
		# Figure out paths from directory
		if trie_path == "" and os.path.exists(os.path.join(model_dir,"trie")):
			trie_path = os.path.join(model_dir,"trie")

		if lm_path == "":
			lm_path = firstFileWithExtension("binary",model_dir)

		if alphabet_path == "":
			alphabet_path = firstFileWithExtension("txt",model_dir)

		if model_path == "":
			model_path = firstFileWithExtension("pbmm",model_dir)

			# Use non-memory-mapped model instead
			if model_path == "":
				model_path = firstFileWithExtension("pb",model_dir)

		
	# Sanity checks
	if not os.path.exists(trie_path):
		print("Trie not found")
		exit(1)

	if not os.path.exists(lm_path):
		print("Language model not found")
		exit(1)

	if not os.path.exists(alphabet_path):
		print("Alphabet not found")
		exit(1)

	if not os.path.exists(model_path):
		print("Model not found")
		exit(1)

	# Parse CSV
	with open(csv_path) as f:
		line_no = 0			
		for line in f:
			line_no += 1
			if line_no < start_line:
				continue;
			
			components = line.split(",")

			if len(components) != 3:
				print("Invalid line")
				continue
			
			if os.path.exists(components[0]):
				expected_transcript = components[2].strip()
				actual_transcript = transcribe(components[0]).strip()

				if not compareTranscripts(expected_transcript, actual_transcript):
					print("***")
					print("File: " + components[0])
					print("Expected transcript: " + expected_transcript)
					print("Actual transcript: " + actual_transcript)
					print("***")
		

def firstFileWithExtension(ext, folder):
	for root, dirs, files in os.walk(folder):
		for filename in files:
			if os.path.splitext(filename)[1].lower() == "." + ext.lower():
				return os.path.join(folder,filename)

	return ""

def transcribe(wav_path):
	global model_path, lm_path, trie_path, alphabet_path

	return str(subprocess.check_output(["deepspeech", "--model", model_path, "--lm", lm_path, "--trie", trie_path, \
 										"--alphabet", alphabet_path, "--audio", wav_path], stderr=subprocess.DEVNULL),"utf-8")

def compareTranscripts(expected, actual):
	global min_word_diff

	# Flag up if number of words is significantly different from expected
	expected_words = len(expected.split())	
	actual_words = len(actual.split())	

	if expected_words == 0 or actual_words == 0:
		return False

	if actual_words == expected_words:
		return True

	if actual_words > expected_words:
		if actual_words - expected_words < min_word_diff:
			return True

		return (actual_words - expected_words) / expected_words < threshold

	if expected_words - actual_words < min_word_diff:
		return True

	return (expected_words - actual_words) / expected_words < threshold


runScript()

