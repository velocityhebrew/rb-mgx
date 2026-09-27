"""
Roblox Brainrot AI - Script Definition (Calibrated for 5-Minute Master Cut)
Dual-character dialogue between Kai (hype friend) and Sigma (deadpan roaster)
Timed to deliver the complete 10-scene storyline in exactly 300 seconds.
"""

SCENES = [
    {
        "scene_id": 1,
        "title": "The Eyebrow Bet & 100-Stage Obby",
        "stage": "STAGE 07 / 100",
        "aura_change": "+500 AURA",
        "lines": [
            ("Kai", "Yo Sigma! If I don't beat this one-hundred-stage Roblox obby in five minutes flat, you get to shave my eyebrows live on stream!"),
            ("Sigma", "Kai, your hairline is already running away. Start jumping before I get the clippers.", "vine_boom"),
            ("Kai", "Watch this jump! Boom! Plus five hundred aura! Look at these glowing neon platforms, this is light work!"),
            ("Sigma", "You clipped the pixel edge of a block. Pure dumb luck. Checkpoint reached.", "checkpoint")
        ]
    },
    {
        "scene_id": 2,
        "title": "The Third Period Microwave Incident",
        "stage": "STAGE 19 / 100",
        "aura_change": "+1,200 AURA",
        "lines": [
            ("Kai", "While I'm hitting these speed coils, you won't believe what happened in third period algebra today."),
            ("Sigma", "Let me guess. You failed a five-question pop quiz and blamed it on lag?", "vine_boom"),
            ("Kai", "No! Brody literally brought a whole countertop microwave into class in his backpack!"),
            ("Sigma", "A microwave in math class? Why am I legally associated with you?", "bruh"),
            ("Kai", "Bro plugged it in next to the teacher and heated up pizza rolls at ten in the morning! The hallway smelled insane!", "vine_boom")
        ]
    },
    {
        "scene_id": 3,
        "title": "The Spinning Hammers of Doom",
        "stage": "STAGE 28 / 100",
        "aura_change": "+2,500 AURA",
        "lines": [
            ("Sigma", "Did Mr. Henderson confiscate the pizza rolls or throw it out the window?"),
            ("Kai", "Neither! He took two rolls, dipped them in ranch, and said 'Quiet down, we're doing quadratic formulas!' Infinite aura move!", "vine_boom"),
            ("Kai", "Watch me time these spinning hammers! One... two... SLIDE! OHHH! Chat clip that pixel gap right now!", "whoosh"),
            ("Sigma", "Calculated risk: zero. Dumb luck: one hundred percent. Stage twenty-eight checkpoint reached.", "checkpoint")
        ]
    },
    {
        "scene_id": 4,
        "title": "The 40 Chicken Nuggets First Date",
        "stage": "STAGE 39 / 100",
        "aura_change": "-50,000 AURA",
        "lines": [
            ("Kai", "My cousin went on a first date to McDonald's last Friday. Bro thought he had supreme Ohio rizz."),
            ("Sigma", "Taking a first date to McDonald's is already negative fifty thousand aura points.", "bruh"),
            ("Kai", "He ordered forty nuggets, ate thirty-six in complete silence, and asked her to split the bill fifty-fifty!", "vine_boom"),
            ("Sigma", "A true romantic. She posted his receipt on TikTok and blocked him, didn't she?"),
            ("Kai", "Two million views! Bro got publicly cancelled by the Ronald McDonald fan club!", "vine_boom")
        ]
    },
    {
        "scene_id": 5,
        "title": "The Vanishing Platforms & Near Death",
        "stage": "STAGE 50 / 100",
        "aura_change": "+10,000 AURA (CLUTCH)",
        "lines": [
            ("Sigma", "Look at your screen, Kai. The neon platforms are literally vanishing into the abyss."),
            ("Kai", "WAIT WAIT! JUMP! NOOO! OH MY GOD I CLUTCHED THE LADDER! MY HEART STOPPED!", "oof"),
            ("Sigma", "Your heart stopped, but miraculously your mouth kept going. Stage fifty reached. Halfway mark.", "checkpoint"),
            ("Kai", "Look at this golden checkpoint! The aura is skyrocketing!", "level_up")
        ]
    },
    {
        "scene_id": 6,
        "title": "The ChatGPT Spanish Exam Fiasco",
        "stage": "STAGE 62 / 100",
        "aura_change": "-100,000 AURA",
        "lines": [
            ("Kai", "Remember Marcus who said he was fluent in Spanish because he watched Money Heist with subtitles?"),
            ("Sigma", "Marcus couldn't order a taco at Taco Bell without pointing at pictures.", "bruh"),
            ("Kai", "On the mid-term essay exam, bro pulls out his phone to use ChatGPT for his Spanish essay."),
            ("Sigma", "Don't tell me he forgot to mute text-to-speech?", "vine_boom"),
            ("Kai", "WORSE! He accidentally air-played his phone to the eighty-inch Smart Board! The whole class watched ChatGPT write 'Hola profesor' in four-K!", "vine_boom"),
            ("Sigma", "Generational academic catastrophe. Minus one hundred thousand aura.", "bruh")
        ]
    },
    {
        "scene_id": 7,
        "title": "The Laser Grid Tightrope",
        "stage": "STAGE 74 / 100",
        "aura_change": "+5,000 AURA",
        "lines": [
            ("Kai", "Mr. Martinez didn't say a word, just took a photo of the Smart Board and hit send to the dean!"),
            ("Sigma", "Marcus is now majoring in commercial lawn maintenance. Focus on the laser tightrope, Kai.", "whoosh"),
            ("Kai", "I am locking in. Absolute silence. Step... Step... JUMP! LETS GOOO! World-class precision!"),
            ("Sigma", "Adequate collision avoidance. Plus five thousand aura.", "checkpoint")
        ]
    },
    {
        "scene_id": 8,
        "title": "The 8th Grade Dodgeball Legend",
        "stage": "STAGE 83 / 100",
        "aura_change": "+25,000 AURA",
        "lines": [
            ("Kai", "That was prime Olympic agility! Smoother than Tyler in eighth grade gym dodgeball!"),
            ("Sigma", "Tyler was four-foot-eleven and threw balls like wet napkins. What folklore are you inventing?", "bruh"),
            ("Kai", "Five varsity football players threw dodgeballs at him at the exact same millisecond!"),
            ("Kai", "Tyler did a full Matrix backward bridge, caught one between his knees, kicked another, and tagged the captain! Gym went wild!", "vine_boom"),
            ("Sigma", "Ninety-five percent cinematic hallucination, five percent sleep deprivation.", "whoosh")
        ]
    },
    {
        "scene_id": 9,
        "title": "The Floating Ice Blocks & 360 Spin",
        "stage": "STAGE 93 / 100",
        "aura_change": "+100,000 AURA",
        "lines": [
            ("Sigma", "Stage ninety-three. Floating ice blocks with instant decay. This is where ninety-nine percent rage quit.", "vine_boom"),
            ("Kai", "Not me! I was forged in the Tower of Hell! Hands steady, sweat dripping, no choke!"),
            ("Sigma", "If you slip, you're buying the whole discord squad boba for a month."),
            ("Kai", "Bet! Jump one... Jump two... Ice slide... THREE SIXTY SPIN OFF THE EDGE! TOUCHDOWN! AURA OVER NINE THOUSAND!", "level_up"),
            ("Sigma", "Disgustingly clean. Don't look down, finish line is right there.", "checkpoint")
        ]
    },
    {
        "scene_id": 10,
        "title": "The 100th Stage Golden Trophy & Outro",
        "stage": "STAGE 100 / 100 (VICTORY)",
        "aura_change": "MAX AURA: 1,000,000+",
        "lines": [
            ("Kai", "STAGE ONE HUNDRED! GIANT GOLDEN TROPHY! WE DID IT! FIVE MINUTES FLAT! Bow down to the Parkour King!", "level_up"),
            ("Sigma", "You conquered a kids' obstacle course. Your mother is shouting downstairs to empty the dishwasher.", "bruh"),
            ("Kai", "If you watched all five minutes, comment 'CHICKEN NUGGET' right now to get your comment pinned!"),
            ("Sigma", "And subscribe to the channel before Kai's computer explodes. Hit the bell.", "vine_boom"),
            ("Kai", "Smash like, subscribe for daily Roblox brainrot challenges, and we'll see you in the next one! PEACE!", "whoosh")
        ]
    }
]

if __name__ == "__main__":
    total_words = 0
    total_lines = 0
    for scene in SCENES:
        for line in scene["lines"]:
            total_lines += 1
            total_words += len(line[1].split())
    print(f"Total Scenes: {len(SCENES)}")
    print(f"Total Dialogue Lines: {total_lines}")
    print(f"Total Spoken Words: {total_words}")
    print(f"Estimated Speech Duration: {total_words / 2.7:.1f} seconds")
