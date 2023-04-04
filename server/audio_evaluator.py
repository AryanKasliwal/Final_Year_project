from mido import MidiFile
from mido import tick2second

def evaluate_generated_track(midi_track_original, midi_track_generated):
    original_scores = []
    for track in midi_track_original:
        original_scores.append(track)
        
    index = 0
    similarity_score, total_score = 0, 0
    for track in midi_track_generated:
        if track == original_scores[index]:
            similarity_score += 1
        total_score += 1
        index += 1
    print(f"Similarity score: {similarity_score * 100 / total_score}%")
    return (similarity_score * 100 / total_score)
