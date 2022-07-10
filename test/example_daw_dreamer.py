import dawdreamer as daw
import numpy as np
import os
from scipy.io import wavfile
import librosa

SAMPLE_RATE = 44100
BUFFER_SIZE = 128 # Parameters will undergo automation at this block size.
BASE_PATH = os.path.join("C:\\Users\\pcber", "Documents", "Paul", "Music")
SYNTH_PLUGIN = os.path.join(BASE_PATH, "Reaper", "Plugins", "Gsinth.dll")  # for instruments, DLLs work.
SYNTH_PRESET = "C:/path/to/preset.fxp"
REVERB_PLUGIN = "C:/path/to/reverb.dll"  # for effects, both DLLs and .vst3 files work
VOCALS_PATH = "C:/path/to/vocals.wav"
PIANO_PATH = "C:/path/to/piano.wav"
SAMPLE_PATH = os.path.join(BASE_PATH, "DawDreamer", "HiHat_02_702.wav")  # sound to be used for sampler instrument.
MIDI_PATH = os.path.join(BASE_PATH, "Midi", "Bach", "bwv827.mid")


def load_audio_file(file_path, duration=None):
    sig, rate = librosa.load(file_path, duration=duration, mono=False, sr=SAMPLE_RATE)
    assert(rate == SAMPLE_RATE)
    return sig


def make_sine(freq: float, duration: float, sr=SAMPLE_RATE):
    """Return sine wave based on freq in Hz and duration in seconds"""
    num_samples = int(duration * sr)  # Number of samples
    return np.sin(np.pi*2.*freq*np.arange(num_samples)/sr)


# Make an engine. We'll only need one.
engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
engine.set_bpm(120.)  # default is 120.

DURATION = 10  # How many seconds we want to render.

# Load audio into a numpy array shaped (Number Channels, Number Samples)
# vocals = load_audio_file(VOCALS_PATH, duration=10.)
# piano = load_audio_file(PIANO_PATH, duration=10.)

# Make a processor and give it the name "my_synth", which we must remember later.
synth = engine.make_plugin_processor("my_synth", SYNTH_PLUGIN)
# synth.load_preset(SYNTH_PRESET)
synth.set_parameter(5, 0.1234) # override a specific parameter.
synth.load_midi(MIDI_PATH)
# We can also add notes one at a time.
synth.add_midi_note(67, 127, 0.5, .25) # (MIDI note, velocity, start sec, duration sec)

# We can automate VST parameters over time. First, we must know the parameter names.
# Get a list of dictionaries where each dictionary describes a controllable parameter.
print(synth.get_plugin_parameters_description())
print(synth.get_parameter_name(1)) # For Serum, returns "A Pan" (the panning of oscillator A)
# The Plugin Processor can set automation according to a parameter index.
synth.set_automation(1, make_sine(.5, DURATION)) # 0.5 Hz sine wave.

# For any processor type, we can get the number of inputs and outputs
print("synth num inputs: ", synth.get_num_input_channels())
print("synth num outputs: ", synth.get_num_output_channels())

load_audio_file(SAMPLE_PATH)
sig, rate = librosa.load(SAMPLE_PATH, duration=None, mono=False, sr=SAMPLE_RATE)
print(sig, rate)

# The sampler processor works like the plugin processor.
# Provide audio for the sample, and then provide MIDI.
# The note value affects the pitch and playback speed of the sample.
# There are basic sampler parameters such as ADSR for volume and filters which you can
# inspect with `get_parameters_description()`
sampler = engine.make_sampler_processor("my_sampler", np.array([load_audio_file(SAMPLE_PATH)]))
# sampler.set_data(load_audio_file(SAMPLE_PATH_2))  # this is allowed too at any time.
print(sampler.get_parameters_description())
sampler.set_parameter(0, 60.)  # set the center frequency to middle C (60)
sampler.set_parameter(5, 100.)  # set the volume envelope's release to 100 milliseconds.
sampler.load_midi(MIDI_PATH)
# We can also add notes one at a time.
sampler.add_midi_note(67, 127, 0.5, .25)  # (MIDI note, velocity, start sec, duration sec)