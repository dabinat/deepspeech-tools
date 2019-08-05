# deepspeech-tools

Scripts to simplify prepping datasets for Mozilla's DeepSpeech. All scripts require Python 3.

## clip_stats

Count the number of files, total file size and total duration of a group of audio files.

### Usage

~~~~
clip_stats.py [--no-estimate] <directory or CSV to scan>
~~~~

`<directory or CSV to scan>` - either a directory containing WAV files or a CSV file in DeepSpeech format with the filename as the first column.

`--no-estimate` - by default the script will estimate the duration based on the file size, assuming 16-bit 16000Hz mono audio files. Use this flag to get the actual duration from ffmpeg, which is useful if the estimates are not accurate enough or if your audio is at a different sample rate. Note that this option is significantly slower than estimation.

### Output

A list of all files found, their total size and the total duration in hours. This total updates dynamically as the scan progresses.

**Sample output**

~~~~
Found 32242 files, 9482.20 MB, 86.31 hours 
~~~~

## csv_combiner

Merge multiple CSV files together. CSVs should already be in DeepSpeech format (filename,file size,transcript) before merging. The script will make sure CSV headers aren't repeated and that every file has an absolute path.

~~~~
csv_combiner.py --dest <combined CSV file> <individual CSV file 1> <individual CSV file 2>...
~~~~

`--dest` - The CSV file that will contain the combined contents of all individual files.

`<individual CSV file>` - One or more CSV files to combine.

**Example**

~~~~ 
python3 csv_combiner.py --dest train-combined.csv ../commonvoice/train.csv ../librispeech/train.csv
~~~~

## csv_purge

Take a list of filenames and strip them from a CSV file.

~~~~
csv_purge.py --source <source CSV file> --dest <dest CSV file> --purge-list <text or CSV file>
~~~~

`--source` - The CSV file you want to strip lines from. The filename should be the first column.

`--dest` - The destination CSV file without the stripped lines.

`--purge-list` - A file containing filenames you wish to strip from the CSV. This can either be a text file with a filename on each line or a CSV with the filename as the first column. Paths can be either absolute or just the filename by itself.

**Example**

~~~~ 
python3 csv_purge.py --source train.csv --dest train-purged.csv --purge-list bad-clips.csv
~~~~

## transcript_check

Checks for significant differences in the number of words a transcript was supposed to return versus the actual number. For example, a clip that was supposed to return five words but returns ten could be an indication of repetition or additional background voices. A clip that was supposed to return twelve words but returns three could indicate excessive noise, a partial recording or an extremely quiet recording.

Note that the purpose of this tool is to flag up clips for further inspection. It is likely to contain false positives from difficult accents and challenging noise environments. It is not recommended that you filter out clips based on the direct output of this script without human review first.

Also note that for best results, you shouldn't check a dataset with a model that was trained on that dataset. So if you're checking Common Voice, you should train on a model that does not include Common Voice data.

This script requires the DeepSpeech command-line tool to be installed (`which deepspeech` should not return an empty string). It's strongly recommended to run this on the CUDA version of DeepSpeech with as powerful a graphics card as possible.

### Usage

~~~~
transcript_check.py --input <CSV file> --model-dir <dir> [--threshold <float>] [--min-word-diff <int>] [--start-line <int>]

transcript_check.py --input <CSV file> --model <model> --alphabet <alphabet> --lm <lm> --trie <trie> [--threshold <float>] [--min-word-diff <int>] [--start-line <int>]
~~~~

`--input` - A CSV file in DeepSpeech format (filename, file size, transcript).

`--model-dir` - A directory containing a DeepSpeech model (.pb or .pbmm), alphabet (.txt), language model (.binary) and trie. 
If you specify this option, the script will ascertain the paths automatically so you don't need to use the --model, --lm, etc arguments. However, you can still use those arguments individually to override paths in the model directory. 

`--threshold` - The percentage difference in word count required to flag up a clip. Default is 0.3.

`--min-word-diff` - The minimum number of words that have to be different in order to flag up a clip. This prevents the threshold percentage flagging up too many clips with short transcripts. Default is 2.

`--start-line` - The line in the source CSV to begin processing. Due to the slow speed of inference, you can use this to avoid processing files you've already checked or start processing at an arbitrary point in a large dataset. The first line of the CSV starts at 1.

### Output

**Sample output**

~~~~
***
File: /home/ubuntu/commonvoice/clips/common_voice_en_18849927.wav
Expected transcript: eight warships of the royal navy have also been named after him
Actual transcript: eight or siseroan also we open
***
***
File: /home/ubuntu/commonvoice/clips/common_voice_en_18849337.wav
Expected transcript: the increase in jobs resulted in a huge immigrant population of russians in belarus
Actual transcript: in passeriano
***
~~~~

## wav_check

Locate corrupt WAV files in a directory. Requires ffmpeg to be installed.

### Usage

~~~~
wav_check.py <directory to scan>
~~~~

`<directory to scan>` - a directory containing WAV files. Files without a .wav extension will be skipped.

### Output

A list of each file that was checked, along with "OK" if it passed the check or "FAIL" if it failed.

**Sample output**

~~~~
/home/ubuntu/001.wav - OK
/home/ubuntu/002.wav - OK
/home/ubuntu/003.wav - FAIL
~~~~

**Tip:** To receive only a list of failures, pipe stdout to null like so:
~~~~
python3 wav_check.py <directory to scan> >/dev/null
~~~~
