"""
YouTube Uploader for Roblox Brainrot AI
Uploads the 5-minute 1080p 60FPS video, sets the viral thumbnail, and adds it to the Roblox playlist.
"""

import os
import sys
import json
import time

# Ensure UTF-8 printing in Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

LOCAL_TOKEN_PATHS = [
    r"C:\Users\kreg9\Downloads\kreggscode\open code\bots\youtube refresh tokens bot\token_chess magix.json",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "token.json")
]

DEFAULT_PLAYLIST_TITLE = "Roblox Brainrot Stories & Parkour [AI Duo]"


def get_authenticated_service():
    client_id = (os.getenv('YOUTUBE_CLIENT_ID') or os.getenv('YT_CLIENT_ID', '')).strip()
    client_secret = (os.getenv('YOUTUBE_CLIENT_SECRET') or os.getenv('YT_CLIENT_SECRET', '')).strip()
    refresh_token = (os.getenv('YOUTUBE_REFRESH_TOKEN') or os.getenv('YT_REFRESH_TOKEN', '')).strip()

    if not all([client_id, client_secret, refresh_token]):
        for p in LOCAL_TOKEN_PATHS:
            if os.path.exists(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    client_id = data.get("client_id", "").strip()
                    client_secret = data.get("client_secret", "").strip()
                    refresh_token = data.get("refresh_token", "").strip()
                    if all([client_id, client_secret, refresh_token]):
                        print(f"[youtube] Loaded credentials from local token file: {p}")
                        break
                except Exception:
                    pass

    if not all([client_id, client_secret, refresh_token]):
        print("[youtube] ⚠️ Missing credentials! Set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN.")
        return None

    def mask(s): return f"{s[:4]}...{s[-4:]}" if s and len(s) > 8 else "SET"
    print(f"[youtube] Authenticating with Client ID: {mask(client_id)}")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube"]
    )

    try:
        creds.refresh(Request())
        print("[youtube] Successfully refreshed OAuth access token.")
    except Exception as e:
        print(f"[youtube] ❌ Auth error: {e}")
        return None

    return build('youtube', 'v3', credentials=creds)


def add_video_to_playlist(youtube, video_id, playlist_title=DEFAULT_PLAYLIST_TITLE):
    try:
        print(f"[youtube] Checking playlists for: '{playlist_title}'...")
        res = youtube.playlists().list(part="snippet", mine=True, maxResults=50).execute()
        playlist_id = None
        for item in res.get("items", []):
            if item["snippet"]["title"].strip().lower() == playlist_title.strip().lower():
                playlist_id = item["id"]
                break

        if not playlist_id:
            print(f"[youtube] Creating new playlist: '{playlist_title}'...")
            new_pl = youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": playlist_title,
                        "description": "Satisfying 60FPS Roblox Obby & Parkour gameplay with hilarious dual-character AI brainrot commentary (Kai & Sigma), sound effects, and crazy storytimes."
                    },
                    "status": {"privacyStatus": "public"}
                }
            ).execute()
            playlist_id = new_pl["id"]
            time.sleep(3)

        print(f"[youtube] Adding video {video_id} to playlist {playlist_id}...")
        for attempt in range(3):
            try:
                youtube.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {"kind": "youtube#video", "videoId": video_id}
                        }
                    }
                ).execute()
                print("[youtube] ✅ Video successfully added to playlist!")
                break
            except Exception as pe:
                if attempt < 2:
                    time.sleep(4)
                else:
                    raise pe
    except Exception as e:
        print(f"[youtube] ⚠️ Playlist notice: {e}")


def upload_to_youtube(
    video_path,
    thumbnail_path=None,
    title=None,
    description=None,
    tags=None,
    playlist_title=DEFAULT_PLAYLIST_TITLE,
    privacy_status="public"
):
    print("\n" + "=" * 60)
    print("▶️ YOUTUBE UPLOAD INITIATED (ROBLOX BRAINROT AI)")
    print("=" * 60)

    youtube = get_authenticated_service()
    if not youtube:
        print("[youtube] ⚠️ Skipping YouTube upload (no valid credentials).")
        return {"status": "skipped", "platform": "youtube"}

    if title is None:
        title = "I Tested an IMPOSSIBLE 100-Stage Roblox Obby (Or Shave My Eyebrows)"

    if tags is None:
        tags = [
            "Roblox", "Roblox Obby", "Roblox Parkour", "Roblox Brainrot",
            "Tower of Hell", "Kai and Sigma", "Gaming Comedy", "Aura Points",
            "Parkour Challenge", "Roblox 60FPS", "Storytime Animation", "Gaming AI"
        ]

    if description is None:
        description = (
            "If Kai doesn't beat this 100-stage Roblox Obby in 5 minutes flat, Sigma gets to shave his eyebrows live on stream!\n\n"
            "Will he clutch the bottomless void drops, or will his aura plummet to negative infinity?\n\n"
            "TIMESTAMPS:\n"
            "0:00 - The Eyebrow Bet & Stage 1\n"
            "0:30 - The 3rd Period Microwave Incident\n"
            "1:00 - The Spinning Hammers of Doom\n"
            "1:30 - The 40 Chicken Nuggets First Date\n"
            "2:00 - Vanishing Platforms & Near-Death Clutch\n"
            "2:30 - The ChatGPT Spanish Exam Smart Board Fiasco\n"
            "3:00 - The Laser Grid Tightrope\n"
            "3:30 - The 8th Grade Gym Dodgeball Legend\n"
            "4:00 - Floating Ice Blocks & 360 Spin\n"
            "4:30 - Stage 100 Golden Trophy & Outro\n\n"
            "💬 Drop a comment with 'CHICKEN NUGGET' down below to get your comment pinned!\n"
            "🔔 Subscribe for daily high-energy Roblox challenges!\n\n"
            "#Roblox #RobloxObby #RobloxParkour #Brainrot #Gaming #Aura #Parkour"
        )

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "20"  # Gaming
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    file_size_mb = os.path.getsize(video_path) // (1024 * 1024)
    print(f"[youtube] Uploading: '{title}' ({file_size_mb} MB)...")

    req = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  -> Upload progress: {int(status.progress() * 100)}%")

    video_id = resp.get("id")
    video_url = f"https://youtu.be/{video_id}"
    print(f"\n[youtube] 🎉 Video published successfully! Live URL: {video_url}")

    if thumbnail_path and os.path.exists(thumbnail_path):
        print(f"[youtube] Uploading custom viral thumbnail: {thumbnail_path}...")
        try:
            mime = "image/png" if thumbnail_path.endswith(".png") else "image/jpeg"
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path), mimetype=mime)
            ).execute()
            print("[youtube] ✅ Custom thumbnail set successfully!")
        except Exception as e:
            print(f"[youtube] ⚠️ Thumbnail notice: {e}")

    add_video_to_playlist(youtube, video_id, playlist_title)
    return {"status": "success", "platform": "youtube", "video_id": video_id, "url": video_url}


if __name__ == "__main__":
    vid = os.path.join(os.path.dirname(os.path.dirname(__file__)), "recordings", "roblox_brainrot_5min.mp4")
    thumb = os.path.join(os.path.dirname(os.path.dirname(__file__)), "recordings", "thumbnail.png")
    if os.path.exists(vid):
        upload_to_youtube(vid, thumb)
    else:
        print(f"File not found: {vid}")
