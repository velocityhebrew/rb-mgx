--[[
    Aura & Stage Custom ScreenGui HUD
    Displays real-time Stage counter, dynamic Aura meter, and popup rewards.
]]

local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local playerGui = player:WaitForChild("PlayerGui")

-- 1. Create ScreenGui
local screenGui = Instance.new("ScreenGui")
screenGui.Name = "BrainrotAuraHUD"
screenGui.ResetOnSpawn = false
screenGui.Parent = playerGui

-- 2. Stage Frame (Top Left)
local stageFrame = Instance.new("Frame")
stageFrame.Name = "StageFrame"
stageFrame.Size = UDim2.new(0, 200, 0, 48)
stageFrame.Position = UDim2.new(0, 25, 0, 25)
stageFrame.BackgroundColor3 = Color3.fromRGB(20, 20, 30)
stageFrame.BorderSizePixel = 0
stageFrame.Parent = screenGui

local stageCorner = Instance.new("UICorner")
stageCorner.CornerRadius = UDim.new(0, 10)
stageCorner.Parent = stageFrame

local stageStroke = Instance.new("UIStroke")
stageStroke.Color = Color3.fromRGB(255, 220, 0)
stageStroke.Thickness = 2.5
stageStroke.Parent = stageFrame

local stageLabel = Instance.new("TextLabel")
stageLabel.Name = "StageLabel"
stageLabel.Size = UDim2.new(1, 0, 1, 0)
stageLabel.BackgroundTransparency = 1
stageLabel.Font = Enum.Font.FredokaOne
stageLabel.Text = "🕹️ STAGE 1 / 10"
stageLabel.TextColor3 = Color3.fromRGB(255, 235, 50)
stageLabel.TextSize = 20
stageLabel.Parent = stageFrame

-- 3. Aura Frame (Top Right)
local auraFrame = Instance.new("Frame")
auraFrame.Name = "AuraFrame"
auraFrame.Size = UDim2.new(0, 220, 0, 48)
auraFrame.Position = UDim2.new(1, -245, 0, 25)
auraFrame.BackgroundColor3 = Color3.fromRGB(15, 25, 20)
auraFrame.BorderSizePixel = 0
auraFrame.Parent = screenGui

local auraCorner = Instance.new("UICorner")
auraCorner.CornerRadius = UDim.new(0, 10)
auraCorner.Parent = auraFrame

local auraStroke = Instance.new("UIStroke")
auraStroke.Color = Color3.fromRGB(0, 255, 128)
auraStroke.Thickness = 2.5
auraStroke.Parent = auraFrame

local auraLabel = Instance.new("TextLabel")
auraLabel.Name = "AuraLabel"
auraLabel.Size = UDim2.new(1, 0, 1, 0)
auraLabel.BackgroundTransparency = 1
auraLabel.Font = Enum.Font.FredokaOne
auraLabel.Text = "⚡ 1,000 AURA"
auraLabel.TextColor3 = Color3.fromRGB(50, 255, 150)
auraLabel.TextSize = 20
auraLabel.Parent = auraFrame

-- 4. Listen for Leaderstats Changes
local leaderstats = player:WaitForChild("leaderstats", 15)
if leaderstats then
    local stageVal = leaderstats:WaitForChild("Stage", 10)
    local auraVal = leaderstats:WaitForChild("Aura", 10)

    if stageVal then
        stageVal.Changed:Connect(function(newVal)
            stageLabel.Text = string.format("🕹️ STAGE %d / 10", newVal)
        end)
    end

    if auraVal then
        auraVal.Changed:Connect(function(newVal)
            auraLabel.Text = string.format("⚡ %s AURA", string.format("%d", newVal))
        end)
    end
end
