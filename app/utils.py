import music21
import numpy as np
import io
from scipy.io.wavfile import write as write_wav
from synthesizer import Synthesizer, Waveform


def note_to_frequencies(note_lists):
    freqs = []
    for note_str in note_lists:
        try:
            note = music21.note.Note(note_str)
            freqs.append(note.pitch.frequency)
        except:
            continue
    return freqs


def generate_wav_bytes_from_notes_freq(notes_freq):
    if not notes_freq:
        return b''

    synth = Synthesizer(
        osc1_waveform=Waveform.sine,
        osc1_volume=1.0,
        use_osc2=False
    )

    sample_rate = 44100

    audio = np.concatenate([
        synth.generate_constant_wave(freq, 0.5)
        for freq in notes_freq
    ])

    # normalize (important for safety)
    audio = audio / np.max(np.abs(audio))

    buffer = io.BytesIO()
    write_wav(buffer, sample_rate, audio.astype(np.float32))

    return buffer.getvalue()   # 🔥 THIS WAS MISSING
