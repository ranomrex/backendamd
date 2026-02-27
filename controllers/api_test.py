import librosa
import numpy as np
y, sr = librosa.load("test.mp3")
tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

chroma = librosa.feature.chroma_stft(y=y, sr=sr)
key_index = np.argmax(np.mean(chroma, axis=1))
keys = ['C', 'C#', 'D', 'D#', 'E', 'F',
            'F#', 'G', 'G#', 'A', 'A#', 'B']
key = keys[key_index]


print("BPM:", tempo)
print("Key:", key)