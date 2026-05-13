#Requires -Version 5.1
<#
.SYNOPSIS
    Build the in-repo QuantDinger frontend and deploy it to Docker.

.DESCRIPTION
    1. Runs `npm run build` inside the frontend directory.
    2. If building from an external override directory, syncs dist/ into this project's frontend/dist/.
    3. Rebuilds and restarts the Docker frontend service.
    4. Reports final container health.

.PARAMETER FrontendDir
    Frontend source directory.
    Default: <project>/frontend.
    Optional override via env var QUANTDINGER_FRONTEND_DIR.

.PARAMETER SkipBuild
    Skip the npm build step (use existing dist from VueSrc).

.PARAMETER SkipDocker
    Skip the Docker rebuild/restart step (only sync dist).

.EXAMPLE
    .\scripts\deploy-frontend.ps1

.EXAMPLE
    .\scripts\deploy-frontend.ps1 -FrontendDir "C:\code\QuantDinger-Vue" -SkipBuild
#>

param(
    [Alias('VueSrc')]
    [string] $FrontendDir = $env:QUANTDINGER_FRONTEND_DIR,
    [switch] $SkipBuild,
    [switch] $SkipDocker
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ── Resolve paths ─────────────────────────────────────────────────────────────
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$RepoFrontendDir = Join-Path $ProjectRoot 'frontend'
$DistTarget  = Join-Path $RepoFrontendDir 'dist'

if (-not $FrontendDir) {
    $FrontendDir = $RepoFrontendDir
}

$FrontendDir = $FrontendDir.TrimEnd('\\')
$BuildDist = Join-Path $FrontendDir 'dist'
$NeedsSync = $false

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  QuantDinger — build + deploy frontend"         -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Frontend  : $FrontendDir"
Write-Host "  Dist dest : $DistTarget"
Write-Host "  Sync dist : $( if ($NeedsSync) { 'YES (external -> repo)' } else { 'NO (in-repo build)' } )"
Write-Host "  Docker    : $( if ($SkipDocker) { 'SKIP' } else { 'rebuild frontend service' } )"
Write-Host ""

# ── 1. Validate frontend source dir ───────────────────────────────────────────
if (-not (Test-Path $FrontendDir -PathType Container)) {
    Write-Error "Frontend directory not found: $FrontendDir`nSet -FrontendDir or env var QUANTDINGER_FRONTEND_DIR."
    exit 1
}

$ResolvedFrontendDir = (Resolve-Path -Path $FrontendDir).Path
$ResolvedRepoFrontendDir = (Resolve-Path -Path $RepoFrontendDir).Path
$NeedsSync = $ResolvedFrontendDir -ne $ResolvedRepoFrontendDir

# ── 2. npm run build ──────────────────────────────────────────────────────────
if (-not $SkipBuild) {
    $NodeModulesDir = Join-Path $FrontendDir 'node_modules'
    $VueCliServiceCmd = Join-Path $NodeModulesDir '.bin\vue-cli-service.cmd'

    if (-not (Test-Path $NodeModulesDir -PathType Container) -or -not (Test-Path $VueCliServiceCmd -PathType Leaf)) {
        Write-Host "[1/4] Installing frontend dependencies (npm install --legacy-peer-deps)..." -ForegroundColor Yellow
        Push-Location $FrontendDir
        try {
            npm install --legacy-peer-deps
            if ($LASTEXITCODE -ne 0) { throw "npm install exited with code $LASTEXITCODE" }
        } finally {
            Pop-Location
        }
        Write-Host "      Dependency install complete." -ForegroundColor Green
    } else {
        Write-Host "[1/4] Dependencies already present (skip npm install)." -ForegroundColor DarkGray
    }

    Write-Host "[2/4] Building frontend (npm run build)..." -ForegroundColor Yellow
    Push-Location $FrontendDir
    try {
        npm run build
        if ($LASTEXITCODE -ne 0) { throw "npm run build exited with code $LASTEXITCODE" }
    } finally {
        Pop-Location
    }
    Write-Host "      Build complete." -ForegroundColor Green
} else {
    Write-Host "[1/4] Skipping dependency install/build (--SkipBuild specified)." -ForegroundColor DarkGray
}

# ── 3. Validate dist exists ───────────────────────────────────────────────────
if (-not (Test-Path $BuildDist -PathType Container)) {
    Write-Error "dist/ not found at: $BuildDist — run without -SkipBuild or build manually first."
    exit 1
}

# ── 4. Sync dist only when building from external override ───────────────────
if ($NeedsSync) {
    Write-Host "[3/4] Syncing dist to $DistTarget ..." -ForegroundColor Yellow

    if (-not (Test-Path $DistTarget -PathType Container)) {
        New-Item -ItemType Directory -Path $DistTarget -Force | Out-Null
    }

    # Robocopy mirrors the directory (/MIR = sync + remove stale files)
    # Exit codes 0-7 from robocopy indicate success (bit flags for copied/skipped/etc.)
    $robocopy = robocopy "$BuildDist" "$DistTarget" /MIR /NFL /NDL /NJH /NJS /nc /ns /np
    if ($LASTEXITCODE -ge 8) {
        Write-Error "robocopy failed with exit code $LASTEXITCODE"
        exit 1
    }

    Write-Host "      Sync complete." -ForegroundColor Green
} else {
    Write-Host "[3/4] Sync skipped (build already targets frontend/dist)." -ForegroundColor DarkGray
}

# ── 5. Docker rebuild ─────────────────────────────────────────────────────────
if (-not $SkipDocker) {
    Write-Host "[4/4] Rebuilding Docker frontend service..." -ForegroundColor Yellow
    Push-Location $ProjectRoot
    try {
        docker compose -f docker-compose.yml up -d --build frontend
        if ($LASTEXITCODE -ne 0) { throw "docker compose up exited with code $LASTEXITCODE" }
    } finally {
        Pop-Location
    }

    # Wait up to 30 s for health check to settle
    Write-Host "      Waiting for container health..." -ForegroundColor DarkGray
    $deadline = [datetime]::Now.AddSeconds(30)
    $health = ''
    while ([datetime]::Now -lt $deadline) {
        $health = (docker inspect --format='{{.State.Health.Status}}' quantdinger-frontend 2>$null)
        if ($health -eq 'healthy') { break }
        Start-Sleep -Seconds 3
    }

    if ($health -eq 'healthy') {
        Write-Host "      Container is healthy." -ForegroundColor Green
    } else {
        Write-Host "      Container status: $health (check manually if not 'healthy')" -ForegroundColor Yellow
    }
} else {
    Write-Host "[4/4] Skipping Docker redeploy (--SkipDocker specified)." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Done. Frontend deployed successfully."          -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
