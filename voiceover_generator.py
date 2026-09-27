"""
Voiceover Generator for Roblox Brainrot AI
Generates dual-character voiceovers using Edge-TTS with timestamps and audio mixing
"""

import os
import asyncio
import edge_tts
from pydub import AudioSegment
from brainrot_script import SCENES

VOICEOVER_DIR = os.path.join(os.path.dirname(__file__), "voiceover")
SFX_DIR = os.path.join(os.path.dirname(__file__), "sfx")
os.makedirs(VOICEOVER_DIR, exist_ok=True)

# Voice profiles
VOICES = {
    "Kai": {
        "voice": "en-US-GuyNeural",
        "rate": "+6%",
        "pitch": "+3Hz"
    },
    "Sigma": {
        "voice": "en-US-ChristopherNeural",
        "rate": "-2%",
        "pitch": "-2Hz"
    }
}


async def generate_line_audio(text: str, speaker: str, output_path: str):
    cfg = VOICES.get(speaker, VOICES["Kai"])
    communicate = edge_tts.Communicate(
        text=text,
        voice=cfg["voice"],
        rate=cfg["rate"],
        pitch=cfg["pitch"]
    )
    await communicate.save(output_path)


async def generate_all_dialogue():
    print("Generating speech audio for all 10 scenes...")
    dialogue_metadata = []
    
    line_counter = 0
    for scene in SCENES:
        scene_id = scene["scene_id"]
        stage = scene["stage"]
        aura = scene["aura_change"]
        
        for item in scene["lines"]:
            speaker = item[0]
            text = item[1]
            sfx = item[2] if len(item) > 2 else None
            
            line_counter += 1
            filename = f"scene_{scene_id:02d}_line_{line_counter:03d}_{speaker.lower()}.mp3"
            filepath = os.path.join(VOICEOVER_DIR, filename)
            
            # Generate if not exists
            if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
                await generate_line_audio(text, speaker, filepath)
            
            # Read duration with pydub
            audio = AudioSegment.from_file(filepath)
            duration_sec = len(audio) / 1000.0
            
            dialogue_metadata.append({
                "scene_id": scene_id,
                "line_id": line_counter,
                "speaker": speaker,
                "text": text,
                "sfx": sfx,
                "stage": stage,
                "aura": aura,
                "filepath": filepath,
                "duration": duration_sec
            })
            print(f"[{speaker}] Scene {scene_id} Line {line_counter}: {duration_sec:.2f}s - {text[:45]}...")

    print(f"Total dialogue lines generated: {len(dialogue_metadata)}")
    return dialogue_metadata


if __name__ == "__main__":
    asyncio.run(generate_all_dialogue())
