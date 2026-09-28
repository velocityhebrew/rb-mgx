--[[
    Checkpoint & Stage Respawn Manager
    Awards Aura on stage progression, plays checkpoint effects, and handles character respawn position.
]]

local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")

local CheckpointsFolder = Workspace:WaitForChild("Checkpoints", 10)

local function getCheckpointByNumber(stageNum)
    if not CheckpointsFolder then return nil end
    return CheckpointsFolder:FindFirstChild("Checkpoint" .. tostring(stageNum))
end

local function onCharacterAdded(character, player)
    local leaderstats = player:WaitForChild("leaderstats", 10)
    if not leaderstats then return end

    local stage = leaderstats:WaitForChild("Stage", 10)
    if not stage then return end

    local humanoidRootPart = character:WaitForChild("HumanoidRootPart", 10)
    if not humanoidRootPart then return end

    task.wait(0.1)
    local targetCheckpoint = getCheckpointByNumber(stage.Value)
    if targetCheckpoint then
        humanoidRootPart.CFrame = targetCheckpoint.CFrame + Vector3.new(0, 3.5, 0)
    end
end

local function onPlayerAdded(player)
    player.CharacterAdded:Connect(function(character)
        onCharacterAdded(character, player)
    end)
end

Players.PlayerAdded:Connect(onPlayerAdded)

-- Setup Checkpoint Touch Events
local function setupCheckpoints()
    if not CheckpointsFolder then
        warn("[CheckpointManager] Checkpoints folder not found in Workspace!")
        return
    end

    for _, pad in ipairs(CheckpointsFolder:GetChildren()) do
        local stageNum = tonumber(string.match(pad.Name, "%d+"))
        if stageNum then
            pad.Touched:Connect(function(hit)
                local character = hit.Parent
                local player = Players:GetPlayerFromCharacter(character)
                if not player then return end

                local leaderstats = player:FindFirstChild("leaderstats")
                if not leaderstats then return end

                local stage = leaderstats:FindFirstChild("Stage")
                local aura = leaderstats:FindFirstChild("Aura")
                if not stage or not aura then return end

                -- Only advance if this is the next stage
                if stageNum > stage.Value then
                    stage.Value = stageNum
                    local auraGain = 500
                    aura.Value = aura.Value + auraGain
                    print(string.format("[Checkpoint] %s reached Stage %d! (+%d Aura)", player.Name, stageNum, auraGain))

                    -- Visual Feedback: Pad Glow
                    pad.Material = Enum.Material.Neon
                    pad.Color = Color3.fromRGB(0, 255, 128)

                    -- Emit Sound / Particle
                    local sound = pad:FindFirstChild("CheckpointSound")
                    if sound then
                        sound:Play()
                    end
                end
            end)
        end
    end
end

task.spawn(setupCheckpoints)
