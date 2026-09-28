--[[
    Speed Boost & Jump Pad Manager
    Temporarily accelerates player walkspeed and launches leaps.
]]

local Workspace = game:GetService("Workspace")
local SpeedPadsFolder = Workspace:WaitForChild("SpeedPads", 10)

local boostCooldown = {}

local function onSpeedPadTouched(hit)
    local character = hit.Parent
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    if not humanoid then return end

    if boostCooldown[character] then return end
    boostCooldown[character] = true

    -- Apply speed coil boost
    local oldSpeed = humanoid.WalkSpeed
    humanoid.WalkSpeed = 36 -- Super sprint

    task.delay(4.5, function()
        if humanoid and humanoid.Parent then
            humanoid.WalkSpeed = oldSpeed
        end
        boostCooldown[character] = nil
    end)
end

if SpeedPadsFolder then
    for _, pad in ipairs(SpeedPadsFolder:GetChildren()) do
        if pad:IsA("BasePart") then
            pad.Touched:Connect(onSpeedPadTouched)
        end
    end
end
