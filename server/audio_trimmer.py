from mido import MidiFile
from mido import tick2second

data_paths = ["./Dataset/FinalData/test/c/", "./Dataset/FinalData/val/c/"]

mid = MidiFile(data_paths[0] + "1_funk_80_beat_4-4_6.midi")

for i, track in enumerate(mid.tracks):
    total_time = 0
    for msg in track:
        tempo = 0
        if msg.type == 'set_tempo':
            tempo = msg.tempo
        total_time  += tick2second(msg.time, mid.ticks_per_beat, tempo)
        print(msg, total_time) # or copy to output file