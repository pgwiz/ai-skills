# install.ps1 - Universal AI Skills installer (Windows)
# Source: https://github.com/pgwiz/ai-skills
# Run: irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex

param(
    [string]$SkillFolderOverride = "",
    [ValidateSet("auto", "antigravity", "copilot", "agents", "all")]
    [string]$Target = "auto",
    [ValidateSet("all", "agent-memory", "dev-md-compactor")]
    [string]$Skill = "all",
    [switch]$Yes
)

$AgentUser = $env:USERNAME
$AgentHome = $env:USERPROFILE
$AgentSystemPath = "$AgentHome\agent-system"

# Determine target directories
$TargetBaseDirs = @{}

if ($SkillFolderOverride -ne "") {
    $TargetBaseDirs["custom"] = $SkillFolderOverride
} else {
    $TargetsToProcess = @()
    if ($Target -eq "all") {
        $TargetsToProcess = @("antigravity", "copilot", "agents")
    } elseif ($Target -ne "auto") {
        $TargetsToProcess = @($Target)
    } else {
        # Auto-detect existing runtimes
        if (Test-Path "$AgentHome\.gemini\config\skills") {
            $TargetsToProcess += "antigravity"
        }
        if (Test-Path "$AgentHome\.copilot") {
            $TargetsToProcess += "copilot"
        }
        if (Test-Path "$AgentHome\.agents") {
            $TargetsToProcess += "agents"
        }
        if ($TargetsToProcess.Count -eq 0) {
            if (Test-Path "$AgentHome\.gemini") {
                $TargetsToProcess += "antigravity"
            } else {
                $TargetsToProcess += "copilot"
            }
        }
    }

    foreach ($t in $TargetsToProcess) {
        switch ($t) {
            "antigravity" { $TargetBaseDirs["antigravity"] = "$AgentHome\.gemini\config\skills" }
            "copilot"     { $TargetBaseDirs["copilot"]     = "$AgentHome\.copilot\skills" }
            "agents"      { $TargetBaseDirs["agents"]      = "$AgentHome\.agents\skills" }
        }
    }
}

# Determine skills to install
$SkillsToInstall = @()
if ($Skill -eq "all") {
    $SkillsToInstall = @("agent-memory", "dev-md-compactor")
} else {
    $SkillsToInstall = @($Skill)
}

Write-Host ""
Write-Host "=== AI Skills Universal Installer (Windows) ===" -ForegroundColor Cyan
Write-Host "User        : $AgentUser"
Write-Host "Home        : $AgentHome"
Write-Host "System Path : $AgentSystemPath"
Write-Host "Skills      : $($SkillsToInstall -join ', ')"
Write-Host "Targets     : $($TargetBaseDirs.Keys -join ', ')"
foreach ($kv in $TargetBaseDirs.GetEnumerator()) {
    Write-Host "  -> $($kv.Key): $($kv.Value)" -ForegroundColor DarkGray
}
Write-Host ""

if (-not $Yes) {
    $confirm = Read-Host "Proceed? (y/n)"
    if ($confirm -ne "y") {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Locate source files
if ((Test-Path ".\agent-memory\SKILL.md") -or (Test-Path ".\dev-md-compactor\SKILL.md")) {
    $SourceRoot = "."
    $TempRoot = $null
} elseif ((Test-Path "..\agent-memory\SKILL.md") -or (Test-Path "..\dev-md-compactor\SKILL.md")) {
    $SourceRoot = ".."
    $TempRoot = $null
} else {
    $TempRoot = Join-Path $env:TEMP ("ai-skills-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null

    Write-Host "Fetching skills source from GitHub..." -ForegroundColor Cyan
    if (Get-Command git -ErrorAction SilentlyContinue) {
        git clone --depth=1 https://github.com/pgwiz/ai-skills.git "$TempRoot\repo" 2>$null
        $SourceRoot = "$TempRoot\repo"
    } else {
        $zipPath = Join-Path $TempRoot "repo.zip"
        $extractPath = Join-Path $TempRoot "extract"
        New-Item -ItemType Directory -Force -Path $extractPath | Out-Null
        Invoke-WebRequest -Uri "https://github.com/pgwiz/ai-skills/archive/refs/heads/main.zip" -OutFile $zipPath
        Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
        $SourceRoot = Join-Path $extractPath "ai-skills-main"
    }
}

function Patch-File([string]$FilePath) {
    $c = Get-Content -Path $FilePath -Raw -Encoding UTF8
    $c = $c.Replace('{AGENT_SYSTEM_PATH}', $AgentSystemPath)
    $c = $c.Replace('{AGENT_USER}', $AgentUser)
    $c = $c.Replace('{AGENT_HOME}', $AgentHome)
    Set-Content -Path $FilePath -Value $c -Encoding UTF8
}

$InstalledLocations = @()

# 1. Install agent-memory
if ($SkillsToInstall -contains "agent-memory") {
    if (-not (Test-Path "$SourceRoot\agent-memory\SKILL.md")) {
        throw "Source for agent-memory not found at $SourceRoot\agent-memory"
    }

    Write-Host "Installing global memory files for agent-memory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Force -Path $AgentSystemPath | Out-Null

    @("GLOBAL_PROTOCOL.md","GLOBAL_WARNINGS.md","CONVENTIONS.md","AGENT_BOOTSTRAP.md","SESSION_START.md","README.md") | ForEach-Object {
        $src = "$SourceRoot\agent-memory\references\$_"
        $dest = "$AgentSystemPath\$_"
        if (Test-Path $src) {
            Copy-Item $src $dest -Force
            Patch-File $dest
            Write-Host "  + $_" -ForegroundColor DarkGray
        }
    }

    $nowStr = Get-Date -Format 'yyyy-MM-dd HH:mm'
    $config = "AGENT_SYSTEM_PATH=$AgentSystemPath`nAGENT_USER=$AgentUser`nAGENT_HOME=$AgentHome`nINSTALLED_ON=$nowStr`nPLATFORM=Windows`n"
    Set-Content "$AgentSystemPath\.agent-config" -Value $config -Encoding UTF8

    foreach ($entry in $TargetBaseDirs.GetEnumerator()) {
        $baseDir = $entry.Value
        $skillDir = if ($entry.Key -eq "custom" -and ($baseDir -match "agent-memory$")) { $baseDir } else { Join-Path $baseDir "agent-memory" }
        Write-Host "Installing agent-memory to $($entry.Key) [$skillDir]..." -ForegroundColor Cyan

        New-Item -ItemType Directory -Force -Path "$skillDir\references" | Out-Null
        Copy-Item "$SourceRoot\agent-memory\SKILL.md" "$skillDir\SKILL.md" -Force
        Patch-File "$skillDir\SKILL.md"

        Get-ChildItem "$SourceRoot\agent-memory\references\*.md" | ForEach-Object {
            Copy-Item $_.FullName "$skillDir\references\" -Force
            Patch-File "$skillDir\references\$($_.Name)"
        }

        Set-Content "$skillDir\.agent-config" -Value $config -Encoding UTF8
        $InstalledLocations += $skillDir
    }
}

# 2. Install dev-md-compactor
if ($SkillsToInstall -contains "dev-md-compactor") {
    if (-not (Test-Path "$SourceRoot\dev-md-compactor\SKILL.md")) {
        throw "Source for dev-md-compactor not found at $SourceRoot\dev-md-compactor"
    }

    foreach ($entry in $TargetBaseDirs.GetEnumerator()) {
        $baseDir = $entry.Value
        $skillDir = if ($entry.Key -eq "custom" -and ($baseDir -match "dev-md-compactor$")) { $baseDir } else { Join-Path $baseDir "dev-md-compactor" }
        Write-Host "Installing dev-md-compactor to $($entry.Key) [$skillDir]..." -ForegroundColor Cyan

        New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
        Copy-Item "$SourceRoot\dev-md-compactor\SKILL.md" "$skillDir\SKILL.md" -Force

        # references
        $refDest = Join-Path $skillDir "references"
        New-Item -ItemType Directory -Force -Path $refDest | Out-Null
        Get-ChildItem -Path "$SourceRoot\dev-md-compactor\references" -Filter "*.md" | ForEach-Object {
            Copy-Item $_.FullName "$refDest\" -Force
        }

        # scripts (exclude __pycache__)
        $scriptDest = Join-Path $skillDir "scripts"
        New-Item -ItemType Directory -Force -Path $scriptDest | Out-Null
        Get-ChildItem -Path "$SourceRoot\dev-md-compactor\scripts" -File | ForEach-Object {
            Copy-Item $_.FullName "$scriptDest\" -Force
        }

        # templates
        $tplDest = Join-Path $skillDir "templates"
        New-Item -ItemType Directory -Force -Path $tplDest | Out-Null
        Get-ChildItem -Path "$SourceRoot\dev-md-compactor\templates" -File | ForEach-Object {
            Copy-Item $_.FullName "$tplDest\" -Force
        }

        $InstalledLocations += $skillDir
    }
}

Write-Host ""
Write-Host "Install complete!" -ForegroundColor Green
if ($SkillsToInstall -contains "agent-memory") {
    Write-Host "Global memory files : $AgentSystemPath\"
}
Write-Host "Installed skill locations:"
foreach ($loc in $InstalledLocations) {
    Write-Host "  + $loc" -ForegroundColor Green
}
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "  - Google Antigravity : Skills are active globally in ~/.gemini/config/skills/"
Write-Host "  - dev-md-compactor   : Run /compact-docs or python dev-md-compactor/scripts/run_compactor.py"
Write-Host "  - agent-memory       : Tell the agent 'Bootstrap .agent/ for this project'"
Write-Host ""

if ($TempRoot -and (Test-Path $TempRoot)) {
    Remove-Item -Recurse -Force $TempRoot
}
