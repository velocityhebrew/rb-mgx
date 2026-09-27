"""
Roblox Autonomous Game Player & Live Recorder
Controls the player avatar in Roblox Obbies using DirectInput scancodes,
handles window focus, camera panning, jumping sequences, and records 60FPS footage.
"""

import os
import sys
import time
import subprocess
import win32gui
import win32con
import pydirectinput

# DirectInput settings
pydirectinput.FAILSAFE = True
pydirectinput.PAUSE = 0.05

ROBLOX_DIR = os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions")
RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)


def find_roblox_executable():
    """Finds the installed RobloxPlayerBeta.exe"""
    if os.path.exists(ROBLOX_DIR):
        for root, dirs, files in os.walk(ROBLOX_DIR):
            if "RobloxPlayerBeta.exe" in files:
                exe_path = os.path.join(root, "RobloxPlayerBeta.exe")
                return exe_path
    return None


def get_roblox_window():
    """Finds the active Roblox window handle"""
    hwnd_found = None
    
    def enum_cb(hwnd, extra):
        nonlocal hwnd_found
        title = win32gui.GetWindowText(hwnd)
        if "Roblox" in title and win32gui.IsWindowVisible(hwnd):
            hwnd_found = hwnd
            
    win32gui.EnumWindows(enum_cb, None)
    return hwnd_found


def focus_roblox():
    """Brings the Roblox window to the foreground"""
    hwnd = get_roblox_window()
    if hwnd:
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)
            print(f"[RobloxBot] Focused window handle: {hwnd}")
            return True
        except Exception as e:
            print(f"[RobloxBot] Warning focusing window: {e}")
            return True
    print("[RobloxBot] Roblox window not detected.")
    return False


def play_parkour_loop(duration_seconds=600):
    """
    Executes intelligent obby parkour inputs:
    - Forward movement (W)
    - Precision jumping (Space)
    - Corner strafes (A/D)
    - Camera angle adjustments via right-mouse drag
    """
    print(f"[RobloxBot] Starting autonomous parkour bot for {duration_seconds}s...")
    if not focus_roblox():
        print("[RobloxBot] Please open Roblox and enter an Obby game.")
        return
        
    start_time = time.time()
    step_count = 0
    
    # Enable Shift-lock if needed
    pydirectinput.press("shift")
    time.sleep(0.2)
    
    while time.time() - start_time < duration_seconds:
        step_count += 1
        elapsed = time.time() - start_time
        
        # 1. Forward run
        pydirectinput.keyDown("w")
        time.sleep(0.4)
        
        # 2. Timed Jump (single block jump)
        pydirectinput.keyDown("space")
        time.sleep(0.12)
        pydirectinput.keyUp("space")
        time.sleep(0.3)
        
        # 3. Double Jump / Long Platform leap
        if step_count % 3 == 0:
            pydirectinput.keyDown("space")
            time.sleep(0.15)
            pydirectinput.keyUp("space")
            time.sleep(0.25)
            
        # 4. Corner Turn / Strafe navigation
        if step_count % 7 == 0:
            # Turn right
            pydirectinput.keyDown("d")
            time.sleep(0.18)
            pydirectinput.keyUp("d")
            # Smooth camera rotation
            pydirectinput.mouseDown(button="right")
            pydirectinput.moveRel(45, 0, duration=0.1)
            pydirectinput.mouseUp(button="right")
        elif step_count % 11 == 0:
            # Turn left
            pydirectinput.keyDown("a")
            time.sleep(0.18)
            pydirectinput.keyUp("a")
            pydirectinput.mouseDown(button="right")
            pydirectinput.moveRel(-45, 0, duration=0.1)
            pydirectinput.mouseUp(button="right")
            
        # Brief breath between sections
        if step_count % 15 == 0:
            pydirectinput.keyUp("w")
            time.sleep(0.3)
            pydirectinput.keyDown("w")
            
        if step_count % 20 == 0:
            print(f"[RobloxBot] Active for {elapsed:.1f}s / {duration_seconds}s (Step {step_count})")
            
    pydirectinput.keyUp("w")
    pydirectinput.keyUp("a")
    pydirectinput.keyUp("d")
    pydirectinput.keyUp("space")
    print(f"[RobloxBot] Session complete! Finished {step_count} parkour maneuvers.")


def record_roblox_window(output_filename="live_roblox_recording.mp4", duration_seconds=300):
    """Records the Roblox window using FFmpeg at 60 FPS 1080p"""
    output_path = os.path.join(RECORDINGS_DIR, output_filename)
    cmd = [
        "ffmpeg", "-y",
        "-f", "gdigrab",
        "-framerate", "60",
        "-i", "title=Roblox",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-t", str(duration_seconds),
        output_path
    ]
    print(f"[RobloxRecorder] Starting 60FPS recording to {output_path}...")
    proc = subprocess.Popen(cmd)
    return proc, output_path


if __name__ == "__main__":
    exe = find_roblox_executable()
    print(f"Found Roblox Executable: {exe}")
    hwnd = get_roblox_window()
    print(f"Active Roblox Window: {hwnd}")
