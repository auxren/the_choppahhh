import librosa
import numpy as np
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path

def process_folder(folder: Path):
    audio_files = list(folder.glob("*.flac")) + list(folder.glob("*.wav"))
    setlist_file = folder / "setlist.txt"
    if not audio_files or not setlist_file.exists():
        raise FileNotFoundError("Missing audio or setlist.txt")

    audio_path = audio_files[0]
    with open(setlist_file) as f:
        titles = [line.strip() for line in f if line.strip()]

    y, sr = librosa.load(str(audio_path), sr=None)
    peaks = librosa.onset.onset_detect(y=y, sr=sr, units='time', backtrack=True)
    starts = list(peaks[:len(titles)]) + [librosa.get_duration(y=y, sr=sr)]

    track_data = []
    for i, title in enumerate(titles):
        track_data.append({
            "title": title,
            "start": starts[i],
            "end": starts[i + 1],
            "audio_path": str(audio_path),
            "sr": sr
        })
    return track_data

def generate_waveform_preview(track):
    y, sr = librosa.load(track["audio_path"], sr=track["sr"], offset=max(0, track["start"] - 5), duration=10)
    times = np.linspace(0, len(y)/sr, num=len(y))
    plt.figure(figsize=(10, 2))
    plt.plot(times, y)
    plt.title(f"{track['title']} — {track['start']:.2f}s")
    plt.xlabel("Seconds")
    plt.tight_layout()
    plt.show()

def preview_audio(track):
    cmd = [
        "ffplay", "-nodisp", "-autoexit",
        "-ss", str(track["start"]),
        "-t", "10",
        track["audio_path"]
    ]
    subprocess.Popen(cmd)
