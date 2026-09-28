"""
Roblox Place (.rbxlx) Generator for "Escape Brainrot Obby (+1M Aura)"
Generates complete 3D obby obstacle course, checkpoints, hazards, and embeds Luau game scripts.
"""

import os
import xml.sax.saxutils as saxutils

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
OUTPUT_FILE = os.path.join(BASE_DIR, "EscapeBrainrotObby.rbxlx")


def escape_xml(s):
    return saxutils.escape(s)


def read_source(subpath):
    p = os.path.join(SRC_DIR, subpath)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def make_cframe_xml(x, y, z):
    return f"""<CoordinateFrame name="CFrame">
					<X>{x}</X><Y>{y}</Y><Z>{z}</Z>
					<R00>1</R00><R01>0</R01><R02>0</R02>
					<R10>0</R10><R11>1</R11><R12>0</R12>
					<R20>0</R20><R21>0</R21><R22>1</R22>
				</CoordinateFrame>"""


def make_part_xml(ref, name, x, y, z, sx, sy, sz, color_int=4284111450, material=256, anchored=True, can_collide=True, transparency=0.0):
    return f"""		<Item class="Part" referent="{ref}">
			<Properties>
				<string name="Name">{escape_xml(name)}</string>
				<bool name="Anchored">{str(anchored).lower()}</bool>
				<bool name="CanCollide">{str(can_collide).lower()}</bool>
				<float name="Transparency">{transparency}</float>
				<token name="Material">{material}</token>
				<Color3uint8 name="Color3uint8">{color_int}</Color3uint8>
				{make_cframe_xml(x, y, z)}
				<Vector3 name="size">
					<X>{sx}</X><Y>{sy}</Y><Z>{sz}</Z>
				</Vector3>
			</Properties>
		</Item>"""


def build_place():
    print(f"Generating Roblox Studio Place file: {OUTPUT_FILE}...")
    
    # Read Luau scripts
    leaderstats_src = read_source("server/Leaderstats.server.luau")
    checkpoint_src = read_source("server/CheckpointManager.server.luau")
    killpart_src = read_source("server/KillPartHandler.server.luau")
    fading_src = read_source("server/DisappearingPlatforms.server.luau")
    speed_src = read_source("server/SpeedBoostHandler.server.luau")
    hud_src = read_source("client/AuraHUD.client.luau")
    
    ref_counter = 100
    
    def get_ref():
        nonlocal ref_counter
        ref_counter += 1
        return f"RBX_{ref_counter}"

    # Build Checkpoint Pads (10 stages)
    checkpoint_parts = []
    stage_z_coords = []
    
    for stage in range(1, 11):
        z_pos = -(stage - 1) * 60
        y_pos = 10 + (stage - 1) * 4
        stage_z_coords.append((y_pos, z_pos))
        
        # Color: Stage 1 Cyan, Stage 10 Golden, others Neon Violet/Blue
        if stage == 1:
            col = 4280295423  # Cyan
            mat = 288         # Neon
        elif stage == 10:
            col = 4294953984  # Gold
            mat = 288         # Neon
        else:
            col = 4288230399  # Purple/Blue
            mat = 288         # Neon
            
        pad_size = (18, 2, 18) if stage in (1, 10) else (12, 1.5, 12)
        part = make_part_xml(
            get_ref(), f"Checkpoint{stage}",
            0, y_pos, z_pos,
            pad_size[0], pad_size[1], pad_size[2],
            color_int=col, material=mat
        )
        checkpoint_parts.append(part)

    # Build Stage Obstacles
    obstacle_parts = []
    kill_parts = []
    fading_parts = []
    speed_parts = []
    
    # Stage 1 -> 2: Floating Step Blocks
    for i in range(1, 5):
        frac = i / 5.0
        x = -4 if i % 2 == 1 else 4
        y = 10 + frac * 4
        z = 0 - frac * 60
        obstacle_parts.append(make_part_xml(get_ref(), f"StepBlock_{i}", x, y, z, 5, 1, 5, color_int=4294940672, material=288))
        
    # Stage 2 -> 3: Red Lava Bars (KillParts)
    for i in range(1, 4):
        frac = i / 4.0
        y = 14 + frac * 4
        z = -60 - frac * 60
        # Safe stepping block
        obstacle_parts.append(make_part_xml(get_ref(), f"SafePad_{i}", 0, y, z, 6, 1, 6, color_int=4284111450, material=256))
        # Lava Bar right next to it
        kill_parts.append(make_part_xml(get_ref(), f"LavaBar_{i}", 0, y + 1.2, z + 7, 16, 0.8, 1.5, color_int=4294901760, material=288))

    # Stage 3 -> 4: Fading / Disappearing Platforms
    for i in range(1, 5):
        frac = i / 5.0
        y = 18 + frac * 4
        z = -120 - frac * 60
        x = -3 if i % 2 == 0 else 3
        fading_parts.append(make_part_xml(get_ref(), f"FadeBlock_{i}", x, y, z, 5, 1, 5, color_int=4294967040, material=288))

    # Stage 4 -> 5: Laser Grid Tightrope
    beam_z_start = -180
    beam_z_end = -240
    obstacle_parts.append(make_part_xml(get_ref(), "TightropeBeam", 0, 24, (beam_z_start + beam_z_end)/2, 1.5, 0.8, 56, color_int=4288256511, material=288))
    # Lasers intersecting
    for i in range(1, 4):
        lz = beam_z_start - i * 14
        kill_parts.append(make_part_xml(get_ref(), f"LaserBeam_{i}", 0, 25.5, lz, 14, 0.5, 0.5, color_int=4294901760, material=288))

    # Stage 5 -> 6: Speed Boost Sprint Track
    obstacle_parts.append(make_part_xml(get_ref(), "SprintTrack", 0, 28, -270, 8, 1, 56, color_int=4280295423, material=256))
    speed_parts.append(make_part_xml(get_ref(), "SpeedPad_Boost", 0, 28.6, -245, 6, 0.4, 6, color_int=4294953984, material=288))

    # Stage 6 -> 7: Vertical Climb (Truss Pillars)
    for i in range(1, 6):
        y = 30 + i * 0.8
        z = -300 - i * 10
        obstacle_parts.append(make_part_xml(get_ref(), f"ClimbStep_{i}", 0, y, z, 5, 1, 5, color_int=4285098345, material=288))

    # Stage 9 -> 10: Golden Victory Trophy Platform
    # Trophy Base
    obstacle_parts.append(make_part_xml(get_ref(), "TrophyBase", 0, 48, -550, 6, 2, 6, color_int=4294953984, material=288))
    # Trophy Pillar
    obstacle_parts.append(make_part_xml(get_ref(), "TrophyPillar", 0, 52, -550, 2.5, 6, 2.5, color_int=4294953984, material=288))
    # Trophy Crown Cup
    obstacle_parts.append(make_part_xml(get_ref(), "TrophyCup", 0, 56, -550, 7, 3, 7, color_int=4294953984, material=288))

    xml_content = f"""<roblox xmlns:xmime="http://www.w3.org/2005/05/xmlmime" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://www.roblox.com/roblox.xsd" version="4">
	<External>null</External>
	<External>nil</External>
	<Item class="Workspace" referent="RBX_Workspace">
		<Properties>
			<string name="Name">Workspace</string>
			<bool name="FilteringEnabled">true</bool>
		</Properties>
		
		<!-- SpawnLocation -->
		<Item class="SpawnLocation" referent="RBX_Spawn">
			<Properties>
				<string name="Name">SpawnLocation</string>
				<bool name="Anchored">true</bool>
				<bool name="CanCollide">true</bool>
				<token name="Material">288</token>
				<Color3uint8 name="Color3uint8">4280295423</Color3uint8>
				{make_cframe_xml(0, 10, 0)}
				<Vector3 name="size">
					<X>20</X><Y>2</Y><Z>20</Z>
				</Vector3>
				<int name="Duration">0</int>
			</Properties>
		</Item>

		<!-- Checkpoints Folder -->
		<Item class="Folder" referent="RBX_CheckpointsFolder">
			<Properties>
				<string name="Name">Checkpoints</string>
			</Properties>
{chr(10).join(checkpoint_parts)}
		</Item>

		<!-- Obstacles Folder -->
		<Item class="Folder" referent="RBX_ObstaclesFolder">
			<Properties>
				<string name="Name">Obstacles</string>
			</Properties>
{chr(10).join(obstacle_parts)}
		</Item>

		<!-- KillParts (Lava & Lasers) -->
		<Item class="Folder" referent="RBX_KillPartsFolder">
			<Properties>
				<string name="Name">KillParts</string>
			</Properties>
{chr(10).join(kill_parts)}
		</Item>

		<!-- Fading Platforms -->
		<Item class="Folder" referent="RBX_FadingFolder">
			<Properties>
				<string name="Name">FadingPlatforms</string>
			</Properties>
{chr(10).join(fading_parts)}
		</Item>

		<!-- Speed Boost Pads -->
		<Item class="Folder" referent="RBX_SpeedPadsFolder">
			<Properties>
				<string name="Name">SpeedPads</string>
			</Properties>
{chr(10).join(speed_parts)}
		</Item>
	</Item>

	<!-- Lighting -->
	<Item class="Lighting" referent="RBX_Lighting">
		<Properties>
			<string name="Name">Lighting</string>
			<float name="Brightness">2.5</float>
			<float name="ClockTime">14.5</float>
			<Color3 name="OutdoorAmbient">
				<R>0.5</R><G>0.5</G><B>0.6</B>
			</Color3>
		</Properties>
	</Item>

	<!-- ServerScriptService (Game Logic) -->
	<Item class="ServerScriptService" referent="RBX_ServerScriptService">
		<Properties>
			<string name="Name">ServerScriptService</string>
		</Properties>
		
		<Item class="Script" referent="RBX_Script_Leaderstats">
			<Properties>
				<string name="Name">LeaderstatsManager</string>
				<ProtectedString name="Source"><![CDATA[{leaderstats_src}]]></ProtectedString>
			</Properties>
		</Item>

		<Item class="Script" referent="RBX_Script_Checkpoints">
			<Properties>
				<string name="Name">CheckpointManager</string>
				<ProtectedString name="Source"><![CDATA[{checkpoint_src}]]></ProtectedString>
			</Properties>
		</Item>

		<Item class="Script" referent="RBX_Script_KillParts">
			<Properties>
				<string name="Name">KillPartHandler</string>
				<ProtectedString name="Source"><![CDATA[{killpart_src}]]></ProtectedString>
			</Properties>
		</Item>

		<Item class="Script" referent="RBX_Script_Fading">
			<Properties>
				<string name="Name">DisappearingPlatforms</string>
				<ProtectedString name="Source"><![CDATA[{fading_src}]]></ProtectedString>
			</Properties>
		</Item>

		<Item class="Script" referent="RBX_Script_Speed">
			<Properties>
				<string name="Name">SpeedBoostHandler</string>
				<ProtectedString name="Source"><![CDATA[{speed_src}]]></ProtectedString>
			</Properties>
		</Item>
	</Item>

	<!-- StarterPlayer & Client Scripts -->
	<Item class="StarterPlayer" referent="RBX_StarterPlayer">
		<Properties>
			<string name="Name">StarterPlayer</string>
		</Properties>
		<Item class="StarterPlayerScripts" referent="RBX_StarterPlayerScripts">
			<Properties>
				<string name="Name">StarterPlayerScripts</string>
			</Properties>
			<Item class="LocalScript" referent="RBX_Script_AuraHUD">
				<Properties>
					<string name="Name">AuraHUD</string>
					<ProtectedString name="Source"><![CDATA[{hud_src}]]></ProtectedString>
				</Properties>
			</Item>
		</Item>
	</Item>

	<!-- ReplicatedStorage -->
	<Item class="ReplicatedStorage" referent="RBX_ReplicatedStorage">
		<Properties>
			<string name="Name">ReplicatedStorage</string>
		</Properties>
	</Item>
</roblox>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    file_size_kb = os.path.getsize(OUTPUT_FILE) / 1024
    print(f"SUCCESS! Roblox Place created: {OUTPUT_FILE} ({file_size_kb:.1f} KB)")
    return OUTPUT_FILE


if __name__ == "__main__":
    build_place()
