"""
Background Electronic Gaming Beat Synthesizer
Generates a rhythmic, catchy 128-BPM backing track for high-energy gaming commentary
"""

import os
import wave
import numpy as np

SAMPLE_RATE = 44100
BPM = 128
BEAT_DUR = 60.0 / BPM
BAR_DUR = BEAT_DUR * 4
NUM_BARS = 4
TOTAL_LOOP_DUR = BAR_DUR * NUM_BARS


def synth_kick(sr=SAMPLE_RATE):
    """Deep punchy 808 kick drum"""
    dur = 0.35
    t = np.linspace(0, dur, int(sr * dur), False)
    freq = 45 + 130 * np.exp(-t * 18.0)
    phase = 2 * np.pi * np.cumsum(freq) / sr
    body = np.sin(phase)
    # Distortion for grit
    body = np.tanh(body * 1.8)
    env = np.exp(-t * 9.0)
    # Click on attack
    click = np.random.uniform(-0.5, 0.5, int(sr * 0.005))
    kick = body * env
    kick[:len(click)] += click
    return kick


def synth_snare(sr=SAMPLE_RATE):
    """Crisp trap snare / clap"""
    dur = 0.22
    t = np.linspace(0, dur, int(sr * dur), False)
    noise = np.random.uniform(-1, 1, len(t))
    env_noise = np.exp(-t * 18.0)
    # Body tone
    tone = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 25.0)
    return (noise * env_noise * 0.7 + tone * 0.5)


def synth_hihat(dur=0.06, sr=SAMPLE_RATE):
    """Crisp 16th note closed hihat"""
    t = np.linspace(0, dur, int(sr * dur), False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.exp(-t * 60.0)
    # High-pass filter simulation
    return (noise[1:] - noise[:-1]) * env[:-1] * 0.35


def synth_bass_note(freq, dur, sr=SAMPLE_RATE):
    """Warm synth bass tone with subtle sub harmonic"""
    t = np.linspace(0, dur, int(sr * dur), False)
    tone = (
        0.7 * np.sin(2 * np.pi * freq * t) +
        0.3 * np.sin(2 * np.pi * (freq * 0.5) * t) +
        0.2 * np.sin(2 * np.pi * (freq * 2.0) * t)
    )
    env = np.sin(np.pi * t / dur) ** 0.3 * np.exp(-t * 1.5)
    return tone * env


def generate_music_loop(output_path="sfx/bg_beat.wav"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    num_samples = int(SAMPLE_RATE * TOTAL_LOOP_DUR)
    mix = np.zeros(num_samples)
    
    kick = synth_kick()
    snare = synth_snare()
    hihat = synth_hihat()
    
    def add_sound(arr, pos_sec, sound, gain=1.0):
        pos_idx = int(pos_sec * SAMPLE_RATE)
        end_idx = min(pos_idx + len(sound), len(arr))
        snd_len = end_idx - pos_idx
        if snd_len > 0:
            arr[pos_idx:end_idx] += sound[:snd_len] * gain

    # 1. Drum Pattern across 4 bars (16 beats)
    for bar in range(NUM_BARS):
        bar_start = bar * BAR_DUR
        # Kicks: Beat 1, 2.5, 3.75
        add_sound(mix, bar_start + 0 * BEAT_DUR, kick, gain=0.85)
        add_sound(mix, bar_start + 1.5 * BEAT_DUR, kick, gain=0.7)
        add_sound(mix, bar_start + 2.75 * BEAT_DUR, kick, gain=0.8)
        
        # Snares on beats 2 and 4
        add_sound(mix, bar_start + 1 * BEAT_DUR, snare, gain=0.65)
        add_sound(mix, bar_start + 3 * BEAT_DUR, snare, gain=0.65)
        
        # 16th Hi-hats
        for step in range(16):
            vel = 0.5 if step % 2 == 0 else 0.35
            add_sound(mix, bar_start + step * (BEAT_DUR / 4), hihat, gain=vel)

    # 2. Bassline & Melody (A minor, F, C, G)
    chord_roots = [110.0, 87.31, 130.81, 98.00]  # A2, F2, C3, G2
    for bar in range(NUM_BARS):
        root = chord_roots[bar]
        bar_start = bar * BAR_DUR
        # 4 bass pulses per bar
        for b in range(4):
            note = synth_bass_note(root, BEAT_DUR * 0.85)
            add_sound(mix, bar_start + b * BEAT_DUR, note, gain=0.45)
            # Melodic accent on upbeat
            accent_freq = root * 2.0
            acc = synth_bass_note(accent_freq, BEAT_DUR * 0.4)
            add_sound(mix, bar_start + (b + 0.5) * BEAT_DUR, acc, gain=0.25)

    # Normalize to -3dB
    max_val = np.max(np.abs(mix))
    if max_val > 0:
        mix = mix / max_val * 0.70
    
    int_audio = (mix * 32767).astype(np.int16)
    with wave.open(output_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(int_audio.tobytes())
    
    print(f"Generated seamless music loop: {output_path} ({TOTAL_LOOP_DUR:.2f}s @ 128 BPM)")
    return output_path


if __name__ == "__main__":
    generate_music_loop()
