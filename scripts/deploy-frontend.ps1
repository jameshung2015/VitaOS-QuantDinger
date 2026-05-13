#Requires -Version 5.1
<#
.SYNOPSIS
    Build the QuantDinger Vue frontend and deploy it to Docker.

.DESCRIPTION
    1. Runs `npm run build` inside the Vue source directory.
    2. Syncs the generated dist/ into this project's frontend/dist/.
    3. Rebuilds and restarts the Docker frontend service.
    4. Reports final container health.

.PARAMETER VueSrc
    Absolute path to the Vue source repo (default: D:\app\QuantDinger-Vue).
    Override via env var QUANTDINGER_VUE_SRC or this parameter.

.PARAMETER SkipBuild
    Skip the npm build step (use existing dist from VueSrc).

.PARAMETER SkipDocker
    Skip the Docker rebuild/restart step (only sync dist).

.EXAMPLE
    .\scripts\deploy-frontend.ps1

.EXAMPLE
    .\scripts\deploy-frontend.ps1 -VueSrc "C:\code\QuantDinger-Vue" -SkipBuild
#>

param(
    [string] $VueSrc    = $env:QUANTDINGER_VUE_SRC,
    [switch] $SkipBuild,
    [switch] $SkipDocker
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ── Resolve paths ─────────────────────────────────────────────────────────────
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$DistTarget  = Join-Path $ProjectRoot 'frontend\dist'

if (-not $VueSrc) {
    $VueSrc = 'D:\app\QuantDinger-Vue'
}

$VueSrc = $VueSrc.TrimEnd('\')
$VueDist = Join-Path $VueSrc 'dist'

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  QuantDinger — build + deploy frontend"         -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Vue src   : $VueSrc"
Write-Host "  Dist dest : $DistTarget"
Write-Host "  Docker    : $( if ($SkipDocker) { 'SKIP' } else { 'rebuild frontend service' } )"
Write-Host ""

# ── 1. Validate Vue source dir ────────────────────────────────────────────────
if (-not (Test-Path $VueSrc -PathType Container)) {
    Write-Error "Vue source directory not found: $VueSrc`nSet -VueSrc or env var QUANTDINGER_VUE_SRC."
    exit 1
}

# ── 2. npm run build ──────────────────────────────────────────────────────────
if (-not $SkipBuild) {
    Write-Host "[1/3] Building frontend (npm run build)..." -ForegroundColor Yellow
    Push-Location $VueSrc
    try {
        npm run build
        if ($LASTEXITCODE -ne 0) { throw "npm run build exited with code $LASTEXITCODE" }
    } finally {
        Pop-Location
    }
    Write-Host "      Build complete." -ForegroundColor Green
} else {
    Write-Host "[1/3] Skipping build (--SkipBuild specified)." -ForegroundColor DarkGray
}

# ── 3. Validate dist exists ───────────────────────────────────────────────────
if (-not (Test-Path $VueDist -PathType Container)) {
    Write-Error "dist/ not found at: $VueDist — run without -SkipBuild or build manually first."
    exit 1
}

# ── 4. Sync dist → frontend/dist ─────────────────────────────────────────────
Write-Host "[2/3] Syncing dist to $DistTarget ..." -ForegroundColor Yellow

# Ensure target directory exists
if (-not (Test-Path $DistTarget -PathType Container)) {
    New-Item -ItemType Directory -Path $DistTarget -Force | Out-Null
}

# Robocopy mirrors the directory (/MIR = sync + remove stale files)
# Exit codes 0-7 from robocopy indicate success (bit flags for copied/skipped/etc.)
$robocopy = robocopy "$VueDist" "$DistTarget" /MIR /NFL /NDL /NJH /NJS /nc /ns /np
if ($LASTEXITCODE -ge 8) {
    Write-Error "robocopy failed with exit code $LASTEXITCODE"
    exit 1
}

Write-Host "      Sync complete." -ForegroundColor Green

# ── 5. Docker rebuild ─────────────────────────────────────────────────────────
if (-not $SkipDocker) {
    Write-Host "[3/3] Rebuilding Docker frontend service..." -ForegroundColor Yellow
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
    Write-Host "[3/3] Skipping Docker redeploy (--SkipDocker specified)." -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Done. Frontend deployed successfully."          -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
