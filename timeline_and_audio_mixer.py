"""
Timeline and Master Audio Mixer for Roblox Brainrot AI
Speeds up voice clips by 1.10x for energetic brainrot pacing,
ensuring all 10 scenes, victory trophy, and outro fit perfectly within exactly 300.0s (5 minutes).
"""

import os
import glob
from pydub import AudioSegment
from pydub.effects import speedup
from brainrot_script import SCENES

BASE_DIR = os.path.dirname(__file__)
VOICEOVER_DIR = os.path.join(BASE_DIR, "voiceover")
SFX_DIR = os.path.join(BASE_DIR, "sfx")
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")


def load_sfx_files():
    sfx = {}
    for f in glob.glob(os.path.join(SFX_DIR, "*.wav")):
        name = os.path.splitext(os.path.basename(f))[0]
        try:
            sfx[name] = AudioSegment.from_file(f)
        except Exception as e:
            print(f"Error loading SFX {name}: {e}")
    return sfx


def build_timeline_and_master_audio(target_duration_sec=300.0):
    print("Building master audio timeline with 1.10x energetic brainrot pacing...")
    sfx_bank = load_sfx_files()
    bg_beat = AudioSegment.from_file(os.path.join(SFX_DIR, "bg_beat.wav"))
    
    # 1. Gather all dialogue lines and speed up for YouTube retention
    lines_info = []
    line_counter = 0
    total_speedup_ms = 0
    
    for scene in SCENES:
        scene_id = scene["scene_id"]
        stage = scene["stage"]
        aura = scene["aura_change"]
        
        for item in scene["lines"]:
            speaker = item[0]
            text = item[1]
            sfx_name = item[2] if len(item) > 2 else None
            
            line_counter += 1
            filename = f"scene_{scene_id:02d}_line_{line_counter:03d}_{speaker.lower()}.mp3"
            filepath = os.path.join(VOICEOVER_DIR, filename)
            
            raw_seg = AudioSegment.from_file(filepath)
            # Apply 1.10x speedup for rapid-fire comedic timing
            seg = speedup(raw_seg, playback_speed=1.10, chunk_size=50, crossfade=25)
            dur_ms = len(seg)
            total_speedup_ms += dur_ms
            
            lines_info.append({
                "scene_id": scene_id,
                "line_id": line_counter,
                "speaker": speaker,
                "text": text,
                "sfx": sfx_name,
                "stage": stage,
                "aura": aura,
                "audio_seg": seg,
                "duration_ms": dur_ms
            })
            
    print(f"Accelerated speech duration: {total_speedup_ms / 1000.0:.2f}s across {len(lines_info)} lines.")
    
    # Target is ~300.0s (300,000 ms)
    target_ms = int(target_duration_sec * 1000)
    # Target speech end time around 295,000 ms to leave 5s for outro swell
    available_speech_window = 295000 - 500  # starts at 500ms
    remaining_ms = available_speech_window - total_speedup_ms
    num_gaps = len(lines_info) - 1
    gap_ms = max(80, int(remaining_ms / num_gaps))
    print(f"Natural conversational gap: {gap_ms} ms between lines.")
    
    # 2. Position each line on the master track
    current_time_ms = 500
    timeline = []
    
    master_voice = AudioSegment.silent(duration=target_ms + 2000)
    master_sfx = AudioSegment.silent(duration=target_ms + 2000)
    
    for idx, item in enumerate(lines_info):
        start_ms = current_time_ms
        end_ms = start_ms + item["duration_ms"]
        
        # Audio stereo placement
        voice_clip = item["audio_seg"] + 2.5
        if item["speaker"] == "Kai":
            voice_clip = voice_clip.pan(-0.15)
        else:
            voice_clip = voice_clip.pan(0.15)
            
        master_voice = master_voice.overlay(voice_clip, position=start_ms)
        
        # SFX Placement
        sfx_ms = None
        if item["sfx"] and item["sfx"] in sfx_bank:
            sfx_clip = sfx_bank[item["sfx"]]
            sfx_pos = max(0, end_ms - 200)
            master_sfx = master_sfx.overlay(sfx_clip - 1.0, position=sfx_pos)
            sfx_ms = sfx_pos
            
        timeline.append({
            "line_id": item["line_id"],
            "scene_id": item["scene_id"],
            "speaker": item["speaker"],
            "text": item["text"],
            "stage": item["stage"],
            "aura": item["aura"],
            "start_sec": start_ms / 1000.0,
            "end_sec": end_ms / 1000.0,
            "sfx": item["sfx"],
            "sfx_sec": (sfx_ms / 1000.0) if sfx_ms else None
        })
        
        current_time_ms = end_ms + gap_ms

    print(f"Final dialogue line finishes at: {current_time_ms / 1000.0:.2f}s (leaving {target_duration_sec - (current_time_ms/1000.0):.1f}s for outro)")
    
    # Trim to exactly target_ms (300,000 ms)
    master_voice = master_voice[:target_ms]
    master_sfx = master_sfx[:target_ms]
    
    # 3. Seamless Background Beat
    bg_loops_needed = int(target_ms / len(bg_beat)) + 3
    full_bg = bg_beat * bg_loops_needed
    full_bg = full_bg[:target_ms] - 19.5
    
    # 4. Master Mix
    print("Mixing voiceovers, SFX, and background beat into final master...")
    final_mix = full_bg.overlay(master_voice).overlay(master_sfx)
    # Fade out smoothly over the last 2 seconds
    final_mix = final_mix.fade_out(2000)
    
    output_audio_path = os.path.join(RECORDINGS_DIR, "master_audio.wav")
    final_mix.export(output_audio_path, format="wav")
    print(f"Master audio exported: {output_audio_path} ({len(final_mix)/1000.0:.2f}s)")
    
    return timeline, output_audio_path, len(final_mix) / 1000.0


def generate_subtitles_ass(timeline, output_ass_path=os.path.join(RECORDINGS_DIR, "subtitles.ass")):
    """Generates ASS subtitles with high-retention styling"""
    print(f"Generating ASS subtitles: {output_ass_path}...")
    
    def sec_to_ass(s):
        hrs = int(s // 3600)
        mins = int((s % 3600) // 60)
        secs = int(s % 60)
        cs = int(round((s - int(s)) * 100))
        if cs >= 100:
            cs = 99
        return f"{hrs:01d}:{mins:02d}:{secs:02d}.{cs:02d}"

    header = """[Script Info]
Title: Roblox Brainrot Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
Timer: 100.0000
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KaiStyle,Impact,62,&H0000FFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,2,60,60,95,1
Style: SigmaStyle,Impact,62,&H00FFFF00,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,2,60,60,95,1
Style: StageStyle,Arial,36,&H0000FFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,4,2,7,50,50,45,1
Style: AuraStyle,Impact,40,&H0033FF33,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,5,2,9,50,50,45,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    events = []
    
    for item in timeline:
        start_t = sec_to_ass(item["start_sec"])
        end_t = sec_to_ass(item["end_sec"])
        
        style = "KaiStyle" if item["speaker"] == "Kai" else "SigmaStyle"
        
        # Split text into 4-5 word rapid bursts
        words = item["text"].split()
        dur = item["end_sec"] - item["start_sec"]
        chunk_size = 5
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        
        chunk_dur = dur / len(chunks)
        for c_idx, chunk in enumerate(chunks):
            c_start = item["start_sec"] + c_idx * chunk_dur
            c_end = min(item["end_sec"], c_start + chunk_dur)
            c_text = " ".join(chunk)
            
            t_s = sec_to_ass(c_start)
            t_e = sec_to_ass(c_end)
            
            line_str = f"Dialogue: 0,{t_s},{t_e},{style},,0,0,0,,{item['speaker'].upper()}: {c_text}"
            events.append(line_str)
            
        stage_line = f"Dialogue: 1,{start_t},{end_t},StageStyle,,0,0,0,,🕹️ {item['stage']}"
        events.append(stage_line)
        
        aura_line = f"Dialogue: 1,{start_t},{end_t},AuraStyle,,0,0,0,,⚡ {item['aura']}"
        events.append(aura_line)

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
        
    print(f"Subtitles written with {len(events)} cues to {output_ass_path}")
    return output_ass_path


if __name__ == "__main__":
    timeline, audio_path, dur = build_timeline_and_master_audio(300.0)
    generate_subtitles_ass(timeline)
