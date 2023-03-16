import os
import os.path
import random
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import torch
from tqdm import tqdm
import magenta

from livelossplot import PlotLosses
from livelossplot.outputs import MatplotlibPlot


# Settings

number_tracks = 5
number_pitches = 72
min_pitch = 24
number_samples_per_song = 8
number_measures = 4
beat_resolution = 4
programs = [0, 0, 25, 33, 48]
is_drums = [True, True, True, True, True]
tempo = 100

batch_size = 16
latent_dimensions = 128
number_steps = 20000

sampling_interval = 100
number_samples = 4

measure_resolution = 4 * beat_resolution
tempo_arr = np.full((4 * 4 * measure_resolution, 1), tempo)
assert 24 % beat_resolution == 0, (
    "beat_resolution must be a factor of 24 (the beat resolution used in "
    "the source dataset)."
)

assert len(programs) == len(is_drums), (
    "Lengths of programs, is_drums and track_names must be the same."
)

# song_dir = 

import tensorflow as tf

print(tf.__version__)