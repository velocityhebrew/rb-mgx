"""
Master Video Renderer for Roblox Brainrot AI
Assembles 1080p 60FPS video with real continuous parkour gameplay,
synchronized dual-character commentary, dynamic bouncing subtitles, meme SFX, and stage HUD.
"""

import os
import sys
import subprocess
import time

BASE_DIR = os.path.dirname(__file__)
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
SOURCE_VIDEO = os.path.join(RECORDINGS_DIR, "roblox_source.mp4")
MASTER_AUDIO = os.path.join(RECORDINGS_DIR, "master_audio.wav")
SUBTITLES_ASS = os.path.join(RECORDINGS_DIR, "subtitles.ass")
OUTPUT_VIDEO = os.path.join(RECORDINGS_DIR, "roblox_brainrot_5min.mp4")


def check_prerequisites():
    if not os.path.exists(SOURCE_VIDEO):
        raise FileNotFoundError(f"Missing source video: {SOURCE_VIDEO}")
    if not os.path.exists(MASTER_AUDIO):
        raise FileNotFoundError(f"Missing master audio: {MASTER_AUDIO}")
    if not os.path.exists(SUBTITLES_ASS):
        raise FileNotFoundError(f"Missing subtitles: {SUBTITLES_ASS}")
    print("[Renderer] All prerequisites verified!")


def render_master_video(target_duration=300.0):
    check_prerequisites()
    print(f"[Renderer] Encoding master 1080p 60FPS video ({target_duration}s = 5 minutes)...")
    
    # Subtitle filter with forward slashes for cross-platform compatibility
    sub_filter = "subtitles.ass"
    
    # Visual filter pipeline:
    # 1. High-fidelity Lanczos 1080p upscale
    # 2. Subtle unsharp mask for crisp block edges
    # 3. Dynamic color & contrast pop
    # 4. Burn-in ASS subtitles (bouncing fonts, aura points, stage HUD)
    vf = (
        "scale=1920:1080:flags=lanczos,"
        "unsharp=5:5:0.6:3:3:0.3,"
        "eq=saturation=1.12:contrast=1.04,"
        f"ass={sub_filter}"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-i", SOURCE_VIDEO,
        "-i", MASTER_AUDIO,
        "-filter_complex", f"[0:v]{vf}[v_out]",
        "-map", "[v_out]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-r", "60",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(target_duration),
        OUTPUT_VIDEO
    ]
    
    print("[Renderer] Launching FFmpeg render command:")
    print(" ".join(cmd))
    
    start_time = time.time()
    # Run from RECORDINGS_DIR so relative ass path is resolved cleanly
    proc = subprocess.run(cmd, cwd=RECORDINGS_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if proc.returncode != 0:
        print("[Renderer ERROR] FFmpeg failed:")
        print(proc.stderr[-1000:])
        raise RuntimeError("Video rendering failed.")
        
    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"\n[Renderer SUCCESS] Master video rendered successfully in {elapsed:.1f}s!")
    print(f"File: {OUTPUT_VIDEO}")
    print(f"Size: {file_size_mb:.2f} MB")
    print(f"Resolution: 1920x1080 (1080p)")
    print(f"Framerate: 60 FPS")
    print(f"Duration: {target_duration}s (5 Minutes)")
    return OUTPUT_VIDEO


if __name__ == "__main__":
    render_master_video(300.0)
