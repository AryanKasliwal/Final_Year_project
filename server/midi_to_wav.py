from midi2audio import FluidSynth

fs = FluidSynth()
fs.midi_to_audio(midi_file='../Dataset/FinalData/test/c/1_funk_80_beat_4-4_6.midi', audio_file='output.wav')

print(fs)
