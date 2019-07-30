# deepspeech-tools

Scripts to simplify prepping datasets for Mozilla's DeepSpeech. All scripts require Python 3.

## csv_combiner

Merge multiple CSV files together. CSVs should already be in DeepSpeech format (filename,file size,transcript) before merging. The script will make sure CSV headers aren't repeated and that every file has an absolute path.

### Usage

~~~~
clip_stats.py [--no-estimate] <directory or CSV to scan>
~~~~

Count the number of files, total file size and total duration of a group of audio files.

`<directory or CSV to scan>` - either a directory containing WAV files or a CSV file in DeepSpeech format with the filename as the first column.

`-no-estimate` - by default the script will estimate the duration based on the file size, assuming 16-bit 16000Hz mono audio files. Use this flag to get the actual duration from ffmpeg, which is useful if the estimates are not accurate enough or if your audio is at a different sample rate. Note that this option is significantly slower than estimation.

### Output

A list of all files found, their total size and the total duration in hours. This total updates dynamically as the scan progresses.

**Sample output**

~~~~
Found 32242 files, 9482.20 MB, 86.31 hours 
~~~~

~~~~
csv_combiner.py --dest <combined CSV file> <individual CSV file 1> <individual CSV file 2>...
~~~~

`--dest` - The CSV file that will contain the combined contents of all individual files.

`<individual CSV file>` - One or more CSV files to combine.

**Example**

~~~~ 
python3 csv_combiner.py --dest train-combined.csv ../commonvoice/train.csv ../librispeech/train.csv
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
