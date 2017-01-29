import pytest
import glob
import os

import midi_tools

@pytest.fixture()
def sample_midis():
	midi_fmt = os.path.join(os.path.dirname(__file__), 'data', "*.mid")
	return glob.glob(midi_fmt)

def test_compute_pitch_histogram(sample_midis):
	pitch_counts = midi_tools.compute_pitch_histogram(sample_midis[0])
	assert sum(pitch_counts.values()) > 0 