--[[
    Kill-Part (Lava / Laser) Collision Manager
    Instantly eliminates players touching hazardous obstacles and deducts penalty aura.
]]

local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")

local KillPartsFolder = Workspace:WaitForChild("KillParts", 10)
local deathDebounce = {}

local function onPartTouched(hit)
    local character = hit.Parent
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid or humanoid.Health <= 0 then return end

    local player = Players:GetPlayerFromCharacter(character)
    if not player then return end

    if deathDebounce[player.UserId] then return end
    deathDebounce[player.UserId] = true

    -- Aura penalty
    local leaderstats = player:FindFirstChild("leaderstats")
    if leaderstats then
        local aura = leaderstats:FindFirstChild("Aura")
        if aura then
            aura.Value = math.max(0, aura.Value - 100)
            print(string.format("[Hazard] %s eliminated by lava! (-100 Aura, Total: %d)", player.Name, aura.Value))
        end
    end

    -- Trigger death
    humanoid.Health = 0

    task.delay(1.0, function()
        deathDebounce[player.UserId] = nil
    end)
end

local function setupKillParts()
    if not KillPartsFolder then return end

    for _, part in ipairs(KillPartsFolder:GetDescendants()) do
        if part:IsA("BasePart") then
            part.Touched:Connect(onPartTouched)
        end
    end

    KillPartsFolder.DescendantAdded:Connect(function(part)
        if part:IsA("BasePart") then
            part.Touched:Connect(onPartTouched)
        end
    end)
end

task.spawn(setupKillParts)
