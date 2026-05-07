# install.ps1 — Agent Memory Skill installer (Windows)
# Source: https://github.com/pgwiz/ai-skills
# Run: irm https://raw.githubusercontent.com/pgwiz/ai-skills/main/install/install.ps1 | iex

param([string]$SkillFolderOverride = "")

$AgentUser = $env:USERNAME
$AgentHome = $env:USERPROFILE
$AgentSystemPath = "$AgentHome\agent-system"

if ($SkillFolderOverride -ne "") {
    $SkillPath = $SkillFolderOverride
} elseif (Test-Path "$AgentHome\.copilot") {
    $SkillPath = "$AgentHome\.copilot\skills\agent-memory"
} elseif (Test-Path "$AgentHome\.agents") {
    $SkillPath = "$AgentHome\.agents\skills\agent-memory"
} else {
    $SkillPath = "$AgentHome\.copilot\skills\agent-memory"
}

Write-Host ""
Write-Host "=== Agent Memory Skill Installer ===" -ForegroundColor Cyan
Write-Host "User      : $AgentUser"
Write-Host "Home      : $AgentHome"
Write-Host "System    : $AgentSystemPath"
Write-Host "Skill dir : $SkillPath"
Write-Host ""
$confirm = Read-Host "Proceed? (y/n)"
if ($confirm -ne "y") { exit 0 }

if (Test-Path ".\agent-memory\SKILL.md") {
    $SourceRoot = "."
    $TempRoot = $null
} else {
    $TempRoot = Join-Path $env:TEMP ("ai-skills-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null

    Write-Host "Fetching skill source from GitHub..." -ForegroundColor Cyan
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

if (-not (Test-Path "$SourceRoot\agent-memory\SKILL.md")) {
    throw "Source files not found at $SourceRoot"
}

function Patch-File([string]$FilePath) {
    $c = Get-Content -Path $FilePath -Raw -Encoding UTF8
    $c = $c.Replace('{AGENT_SYSTEM_PATH}', $AgentSystemPath)
    $c = $c.Replace('{AGENT_USER}', $AgentUser)
    $c = $c.Replace('{AGENT_HOME}', $AgentHome)
    Set-Content -Path $FilePath -Value $c -Encoding UTF8
}

Write-Host "Installing global memory files..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $AgentSystemPath | Out-Null

@("GLOBAL_PROTOCOL.md","GLOBAL_WARNINGS.md","CONVENTIONS.md","AGENT_BOOTSTRAP.md","SESSION_START.md","README.md") | ForEach-Object {
    $src = "$SourceRoot\agent-memory\references\$_"
    $dest = "$AgentSystemPath\$_"
    if (Test-Path $src) {
        Copy-Item $src $dest -Force
        Patch-File $dest
        Write-Host "  ✓ $_" -ForegroundColor DarkGray
    }
}

Write-Host "Installing skill..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "$SkillPath\references" | Out-Null

Copy-Item "$SourceRoot\agent-memory\SKILL.md" "$SkillPath\SKILL.md" -Force
Patch-File "$SkillPath\SKILL.md"

Get-ChildItem "$SourceRoot\agent-memory\references\*.md" | ForEach-Object {
    Copy-Item $_.FullName "$SkillPath\references\" -Force
    Patch-File "$SkillPath\references\$($_.Name)"
}

$config = @"
AGENT_SYSTEM_PATH=$AgentSystemPath
AGENT_USER=$AgentUser
AGENT_HOME=$AgentHome
INSTALLED_ON=$(Get-Date -Format 'yyyy-MM-dd HH:mm')
PLATFORM=Windows
"@

Set-Content "$AgentSystemPath\.agent-config" -Value $config -Encoding UTF8
Set-Content "$SkillPath\.agent-config" -Value $config -Encoding UTF8

Write-Host ""
Write-Host "Install complete!" -ForegroundColor Green
Write-Host "Global files : $AgentSystemPath\"
Write-Host "Skill        : $SkillPath\"
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "  1. Open any project root"
Write-Host "  2. Tell the agent: Bootstrap .agent/ for this project"
Write-Host "  3. From now on, just type your task"

if ($TempRoot -and (Test-Path $TempRoot)) {
    Remove-Item -Recurse -Force $TempRoot
}
