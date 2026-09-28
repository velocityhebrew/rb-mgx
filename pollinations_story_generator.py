"""
Pollinations AI Official Paid API Story & Script Generator
Uses the official paid endpoint (https://gen.pollinations.ai/v1/chat/completions)
with Secret Key (sk_...) authentication via Bearer token.
"""

import os
import json
import random
import urllib.request
import urllib.error

# Pollinations Secret Key (starts with sk_ from enter.pollinations.ai)
POLLINATIONS_API_KEY = os.environ.get("POLLINATIONS_API_KEY", "")

# Official Paid API Endpoint
POLLINATIONS_PAID_ENDPOINT = "https://gen.pollinations.ai/v1/chat/completions"

THEMES = [
    "The wild microwave lunch incident in 3rd period math",
    "Bro tried to use ChatGPT on the smartboard during Spanish test",
    "First date at McDonald's ordering 40 nuggets in total silence",
    "Teacher caught streaming Fortnite on Twitch instead of grading",
    "Accidentally AirPlaying Minecraft parkour to the whole school auditorium",
    "Bro bought an iced latte with 18 pumps of syrup and called it Sigma fuel",
    "The fake AirPods that played Bluetooth connection at 200% volume in the library",
    "Bro wore a full tuxedo to gym class to boost his aura",
    "Bro claimed he has 10 million power in Rise of Kingdoms to skip the cafeteria line",
    "Accidentally joined the class Zoom from a Roblox gaming chair wearing full drip"
]

SYSTEM_PROMPT = """You are an elite, viral Gen-Z brainrot scriptwriter for a high-retention gaming channel.
Generate a hilarious, rapid-fire dialogue between two characters playing a Roblox parkour obby:
- Character 'Kai': Hyperactive, confident, loud, obsessed with aura points and clutch jumps.
- Character 'Sigma': Calm, deadpan, sarcastic roaster who points out Kai's fails.

FORMAT REQUIREMENTS:
Return ONLY valid JSON (no markdown formatting, no code blocks) matching this schema:
{
  "title": "Short catchy title",
  "theme": "Theme description",
  "scenes": [
    {
      "scene_id": 1,
      "stage": "STAGE 07 / 100",
      "aura_change": "+500 AURA",
      "lines": [
        {"speaker": "Kai", "text": "...", "sfx": "vine_boom"},
        {"speaker": "Sigma", "text": "...", "sfx": "checkpoint"}
      ]
    }
  ]
}
Available sfx: 'vine_boom', 'bruh', 'checkpoint', 'oof', 'whoosh', 'level_up'.
Keep dialogue snappy, funny, and full of current internet culture (aura, rizz, clutch, Ohio, lag).
Generate exactly 8-10 scenes.
"""

def generate_daily_script(theme=None, api_key=None):
    key = api_key or POLLINATIONS_API_KEY
    if not theme:
        theme = random.choice(THEMES)
        
    print(f"[PollinationsAI] Generating new unique brainrot script via Paid API...")
    print(f"[PollinationsAI] Endpoint: {POLLINATIONS_PAID_ENDPOINT}")
    print(f"[PollinationsAI] Theme: '{theme}'")
    
    user_prompt = f"Write a complete, brand new 10-scene Roblox Obby script about: {theme}. Make it hilarious, totally original, and ensure Kai and Sigma roast each other constantly."
    
    payload = {
        "model": "openai",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.8
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "RobloxBrainrotAI/2.0"
    }
    if key:
        headers["Authorization"] = f"Bearer {key}"
        print(f"[PollinationsAI] Using configured Secret Key ({key[:6]}...)")
    else:
        print("[PollinationsAI] Warning: No POLLINATIONS_API_KEY found in environment. Set your sk_ key from enter.pollinations.ai.")
        
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(POLLINATIONS_PAID_ENDPOINT, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw_text = resp.read().decode("utf-8")
            response_json = json.loads(raw_text)
            
            # OpenAI chat completions format: choices[0].message.content
            content = response_json["choices"][0]["message"]["content"]
            
            # Strip markdown fences if present
            clean_text = content.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.startswith("```"):
                clean_text = clean_text[3:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            script_data = json.loads(clean_text)
            print(f"[PollinationsAI] Success! Generated '{script_data.get('title')}' with {len(script_data.get('scenes', []))} scenes.")
            return script_data
            
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"[PollinationsAI] HTTP Error {e.code}: {err_msg}")
        return None
    except Exception as e:
        print(f"[PollinationsAI] Error: {e}")
        return None

if __name__ == "__main__":
    script = generate_daily_script()
    if script:
        output_file = os.path.join(os.path.dirname(__file__), "daily_script_sample.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(script, f, indent=2)
        print(f"Saved generated script to {output_file}")
