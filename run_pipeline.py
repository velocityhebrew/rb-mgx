"""
Main Pipeline Runner for Roblox Brainrot AI Video Automation
Orchestrates audio generation, SFX, subtitle generation, video rendering, thumbnail creation, and YouTube publishing.
"""

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
SFX_DIR = os.path.join(BASE_DIR, "sfx")


def main():
    print("=" * 70)
    print("🎮 ROBLOX BRAINROT AI - FULL AUTOMATION PIPELINE")
    print("=" * 70)
    
    # Step 1: SFX suite
    print("\n[Step 1/6] Verifying sound effects suite...")
    from sfx_generator import generate_all_sfx
    generate_all_sfx()
    
    # Step 2: Background music loop
    print("\n[Step 2/6] Verifying background music beat...")
    from bg_music_generator import generate_music_loop
    generate_music_loop()
    
    # Step 3: Voiceover generation
    print("\n[Step 3/6] Generating dual-character voiceovers (Edge-TTS)...")
    import asyncio
    from voiceover_generator import generate_all_dialogue
    asyncio.run(generate_all_dialogue())
    
    # Step 4: Audio timeline mixing & Subtitles
    print("\n[Step 4/6] Mixing master audio and generating ASS subtitles...")
    from timeline_and_audio_mixer import build_timeline_and_master_audio, generate_subtitles_ass
    timeline, master_audio, dur = build_timeline_and_master_audio(300.0)
    generate_subtitles_ass(timeline)
    
    # Step 5: Master 1080p 60FPS Video Rendering
    print("\n[Step 5/6] Rendering master 1080p 60FPS video with dynamic HUD & captions...")
    from render_roblox_video import render_master_video
    video_path = render_master_video(300.0)
    
    # Step 6: Viral Thumbnail Generation
    print("\n[Step 6/6] Generating viral YouTube thumbnail...")
    from thumbnail_generator import generate_thumbnail
    thumb_path = generate_thumbnail()
    
    print("\n" + "=" * 70)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"🎬 Video: {video_path}")
    print(f"🖼️ Thumbnail: {thumb_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
