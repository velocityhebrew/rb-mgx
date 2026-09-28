--[[
    Disappearing / Fading Platform Manager
    Platforms fade away 0.75 seconds after being stepped on, then regenerate.
]]

local Workspace = game:GetService("Workspace")
local TweenService = game:GetService("TweenService")

local FadingFolder = Workspace:WaitForChild("FadingPlatforms", 10)

local function setupFadingPart(part)
    if not part:IsA("BasePart") then return end

    local isFading = false
    local originalColor = part.Color
    local originalTransparency = part.Transparency

    part.Touched:Connect(function(hit)
        local character = hit.Parent
        local humanoid = character:FindFirstChildOfClass("Humanoid")
        if not humanoid or isFading then return end

        isFading = true

        -- Warning phase (0.6 seconds): Rapid flashing yellow/red
        part.Color = Color3.fromRGB(255, 60, 60)
        task.wait(0.6)

        -- Fade out: Tween transparency to 1
        local tweenInfo = TweenInfo.new(0.2, Enum.EasingStyle.Linear)
        local fadeTween = TweenService:Create(part, tweenInfo, {Transparency = 1})
        fadeTween:Play()
        fadeTween.Completed:Wait()

        part.CanCollide = false

        -- Respawn cooldown (3.0 seconds)
        task.wait(3.0)

        -- Reappear
        part.Transparency = originalTransparency
        part.Color = originalColor
        part.CanCollide = true
        isFading = false
    end)
end

if FadingFolder then
    for _, part in ipairs(FadingFolder:GetChildren()) do
        setupFadingPart(part)
    end
end
