--[[
    Leaderstats & DataStore Manager
    Tracks player Stage progress and Aura points with auto-saving
]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local ObbyDataStore = DataStoreService:GetDataStore("BrainrotObby_Save_v1")

local function onPlayerAdded(player)
    local leaderstats = Instance.new("Folder")
    leaderstats.Name = "leaderstats"
    leaderstats.Parent = player

    local stage = Instance.new("IntValue")
    stage.Name = "Stage"
    stage.Value = 1
    stage.Parent = leaderstats

    local aura = Instance.new("IntValue")
    aura.Name = "Aura"
    aura.Value = 1000
    aura.Parent = leaderstats

    -- Load saved data
    local key = "Player_" .. player.UserId
    local success, data = pcall(function()
        return ObbyDataStore:GetAsync(key)
    end)

    if success and data then
        stage.Value = data.Stage or 1
        aura.Value = data.Aura or 1000
        print("[DataStore] Loaded progress for " .. player.Name .. ": Stage " .. stage.Value .. " | Aura " .. aura.Value)
    else
        print("[DataStore] Starting fresh progress for " .. player.Name)
    end
end

local function savePlayerData(player)
    local leaderstats = player:FindFirstChild("leaderstats")
    if not leaderstats then return end

    local stage = leaderstats:FindFirstChild("Stage")
    local aura = leaderstats:FindFirstChild("Aura")
    if not stage or not aura then return end

    local data = {
        Stage = stage.Value,
        Aura = aura.Value
    }

    local key = "Player_" .. player.UserId
    local success, err = pcall(function()
        ObbyDataStore:SetAsync(key, data)
    end)

    if success then
        print("[DataStore] Saved progress for " .. player.Name)
    else
        warn("[DataStore] Failed saving data for " .. player.Name .. ": " .. tostring(err))
    end
end

Players.PlayerAdded:Connect(onPlayerAdded)
Players.PlayerRemoving:Connect(savePlayerData)

game:BindToClose(function()
    for _, player in ipairs(Players:GetPlayers()) do
        savePlayerData(player)
    end
end)
