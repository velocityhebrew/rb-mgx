"""
Meme Sound Effects Generator for Roblox Brainrot AI
Generates authentic audio effects: Vine Boom, Bruh, Roblox Oof, Checkpoint chime, Whoosh, Level Up
"""

import os
import math
import struct
import wave
import numpy as np

SFX_DIR = os.path.join(os.path.dirname(__file__), "sfx")
os.makedirs(SFX_DIR, exist_ok=True)
SAMPLE_RATE = 44100


def save_wav(filename: str, audio: np.ndarray, sr: int = SAMPLE_RATE):
    filepath = os.path.join(SFX_DIR, filename)
    # Normalize to -1.0 to 1.0
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.95
    int_audio = (audio * 32767).astype(np.int16)
    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(int_audio.tobytes())
    print(f"Generated SFX: {filename} ({len(audio)/sr:.2f}s)")
    return filepath


def generate_vine_boom():
    """Heavy 808 sub-bass drop with punchy attack and distortion"""
    duration = 1.6
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Frequency pitch drops rapidly from 130Hz down to 35Hz
    freq = 35 + 95 * np.exp(-t * 8.0)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    # Sine fundamental
    boom = np.sin(phase)
    # Add subtle saturation / harmonics
    boom = np.tanh(boom * 2.5)
    # Add low noise burst at the very start for the punch impact
    impact_t = t[:int(0.08 * SAMPLE_RATE)]
    noise = np.random.uniform(-0.6, 0.6, len(impact_t)) * np.exp(-impact_t * 50.0)
    boom[:len(impact_t)] += noise
    # Exponential decay envelope
    envelope = np.exp(-t * 2.2)
    audio = boom * envelope
    return save_wav("vine_boom.wav", audio)


def generate_bruh():
    """Deep comedic bass vocaloid drop"""
    duration = 0.8
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Formant-like bass sweep from 140Hz down to 75Hz
    freq = 75 + 65 * np.exp(-t * 4.0)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    # Harmonics
    audio = 0.6 * np.sin(phase) + 0.3 * np.sin(phase * 2) + 0.15 * np.sin(phase * 3)
    envelope = np.sin(np.pi * t / duration) ** 0.5 * np.exp(-t * 2.0)
    audio = audio * envelope
    return save_wav("bruh.wav", audio)


def generate_roblox_oof():
    """Classic pitch downward scoop grunt"""
    duration = 0.35
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # 260Hz dropping to 110Hz quickly
    freq = 110 + 150 * np.exp(-t * 9.0)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    audio = np.sin(phase) * 0.7 + np.sin(phase * 2) * 0.3
    # Shape attack & release
    env = np.ones_like(t)
    attack_samples = int(0.02 * SAMPLE_RATE)
    env[:attack_samples] = np.linspace(0, 1, attack_samples)
    env[attack_samples:] = np.exp(-(t[attack_samples:] - 0.02) * 8.0)
    audio = audio * env
    return save_wav("roblox_oof.wav", audio)


def generate_checkpoint():
    """Sparkling two-tone checkpoint chime (E6 -> B6)"""
    duration = 0.7
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    audio = np.zeros_like(t)
    
    # Note 1: 1318 Hz (E6) for first 0.15s
    t1 = t[t < 0.3]
    env1 = np.exp(-t1 * 10.0)
    audio[:len(t1)] += (np.sin(2 * np.pi * 1318 * t1) + 0.3 * np.sin(2 * np.pi * 2636 * t1)) * env1
    
    # Note 2: 1975 Hz (B6) starting at 0.12s
    start_idx = int(0.12 * SAMPLE_RATE)
    t2 = t[start_idx:] - 0.12
    env2 = np.exp(-t2 * 6.0)
    audio[start_idx:] += (np.sin(2 * np.pi * 1975 * t2) + 0.4 * np.sin(2 * np.pi * 3950 * t2)) * env2
    
    return save_wav("checkpoint.wav", audio)


def generate_whoosh():
    """Quick whoosh transition effect"""
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    # Modulate envelope: rises and falls
    envelope = np.sin(np.pi * (t / duration)) ** 2
    # Apply soft smoothing
    window = int(SAMPLE_RATE * 0.005)
    kernel = np.ones(window) / window
    smoothed = np.convolve(noise * envelope, kernel, mode="same")
    return save_wav("whoosh.wav", smoothed)


def generate_level_up():
    """4-note triumphant fanfare chime"""
    duration = 1.0
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    audio = np.zeros_like(t)
    notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
    for i, freq in enumerate(notes):
        st = i * 0.12
        end = st + 0.5
        s_idx = int(st * SAMPLE_RATE)
        e_idx = min(len(t), int(end * SAMPLE_RATE))
        nt = t[s_idx:e_idx] - st
        env = np.exp(-nt * 7.0)
        audio[s_idx:e_idx] += (np.sin(2 * np.pi * freq * nt) + 0.25 * np.sin(2 * np.pi * freq * 2 * nt)) * env
    return save_wav("level_up.wav", audio)


def generate_all_sfx():
    print("Generating Roblox Brainrot SFX suite...")
    generate_vine_boom()
    generate_bruh()
    generate_roblox_oof()
    generate_checkpoint()
    generate_whoosh()
    generate_level_up()
    print("All SFX generated successfully in:", SFX_DIR)


if __name__ == "__main__":
    generate_all_sfx()
