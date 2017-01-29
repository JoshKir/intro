from joblib import Parallel, delayed
import pretty_midi
import json
import glob
import os
import argparse 


def compute_pitch_histogram(filename):
	midi = pretty_midi.PrettyMIDI(filename)
	pitch_counts = {pc: 0 for pc in range(12)}

	for inst in midi.instruments:
		if inst.is_drum:
			continue
		for note in inst.notes:
			pc = note.pitch % 12
			pitch_counts[pc] += (note.end - note.start)
	name = os.path.split(filename)[-1]		
	return {'name': name, 
			'pitches': pitch_counts}			

def process_many (filenames, n_jobs, verbose):
	pool = Parallel(n_jobs=n_jobs, verbose=verbose)
	fx = delayed(compute_pitch_histogram)
	return pool(fx(fn) for fn in filenames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
    	"filepattern", type=str,
    	help="Filepattern for finding MIDI files, e.g. 'data/*.mid'")
    parser.add_argument(
        "Output_file", type=str,
        help="Outout file for writing results")
    parser.add_argument(
        "--n_jobs", metavar='n_jobs', type=int, default=-2,
        help="Number of CPUs to use for processing.")
    parser.add_argument(
        "--n_verbose", metavar='verbose', type=int, default=0,
        help="Verbosity for writing outputs.")

    args = parser.parse_args()
    filenames = glob.glob(args.filepattern)
    results = process_many(filenames)	
    with open(args.output_file, 'w') as fp:
    	json.dump(results, fp, indent=2)