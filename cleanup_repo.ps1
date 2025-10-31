# Futurix AI - Repository Cleanup (PowerShell)
# Creates a backup and removes safe, generated, or redundant files

$ErrorActionPreference = "Stop"

Write-Host "=== Futurix AI Repository Cleanup (PowerShell) ===" -ForegroundColor Cyan

# Timestamp and backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $env:TEMP "repo_cleanup_backup_$timestamp"
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

# Manifest
$manifest = Join-Path $backupDir "cleanup_manifest.txt"
"Cleanup Manifest - $timestamp`n===============================" | Out-File -Encoding utf8 $manifest

# Helper: Backup file or directory
function Backup-ItemPath {
    param(
        [Parameter(Mandatory=$true)][string]$Path
    )
    if (Test-Path $Path -PathType Leaf) {
        Copy-Item $Path -Destination $backupDir -Force -ErrorAction SilentlyContinue
        Add-Content $manifest "FILE: $Path"
    } elseif (Test-Path $Path -PathType Container) {
        $zipName = (Split-Path $Path -Leaf) + ".zip"
        $zipPath = Join-Path $backupDir $zipName
        Compress-Archive -Path $Path -DestinationPath $zipPath -Force -ErrorAction SilentlyContinue
        Add-Content $manifest "DIR: $Path -> $zipPath"
    }
}

# 1) Safe generated artifacts
Write-Host "1) Removing Python caches, temp files, logs" -ForegroundColor Yellow
Get-ChildItem -Recurse -Force -Include "__pycache__" -Directory -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
Get-ChildItem -Recurse -Force -Include "*.pyc","*.pyo",".DS_Store","*.tmp","*.bak" -File -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item $_.FullName -Force -ErrorAction SilentlyContinue }

# 2) Backend runtime outputs (kept in backup not necessary)
$backendPatterns = @(
    "backend/data/uploads/*",
    "backend/data/exports/*",
    "backend/logs/*"
)
foreach ($pattern in $backendPatterns) {
    Get-ChildItem $pattern -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
        # no backup for large/generated artifacts
        Remove-Item $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
        Add-Content $manifest "REMOVED: $($_.FullName)"
    }
}

# 3) Flagged files likely redundant (backup then remove)
$maybeRedundant = @(
    "debug_client.py",
    "fix_openai_client.sh",
    "FIX_README.md",
    "setup_shivaay_integration.sh",
    "SHIVAAY_INTEGRATION_SUMMARY.md",
    "test_openai_client.py",
    "test_shivaay_integration.py"
)
foreach ($p in $maybeRedundant) {
    if (Test-Path $p) {
        Backup-ItemPath -Path $p
        Remove-Item $p -Force -ErrorAction SilentlyContinue
        Add-Content $manifest "REMOVED: $p"
    }
}

# 4) Duplicated config at root vs backend (keep backend/*, remove root duplicates)
$rootDupes = @(
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml"
)
foreach ($p in $rootDupes) {
    if (Test-Path $p -PathType Leaf) {
        # Keep backend versions
        if (Test-Path (Join-Path "backend" $p)) {
            Backup-ItemPath -Path $p
            Remove-Item $p -Force -ErrorAction SilentlyContinue
            Add-Content $manifest "REMOVED_DUPLICATE: $p (kept backend/$p)"
        }
    }
}

# 5) Old src/ tree (archive only, do not delete automatically)
if (Test-Path "src" -PathType Container) {
    Write-Host "Archiving src/ for manual review (not deleting)" -ForegroundColor Yellow
    Backup-ItemPath -Path "src"
}

# 6) Example code (archive only, do not delete automatically)
if (Test-Path "examples" -PathType Container) {
    Backup-ItemPath -Path "examples"
    # keep examples unless you want to remove; uncomment next line to delete
    # Remove-Item "examples" -Recurse -Force
}

# 7) Create preview summary
$preview = Join-Path (Get-Location) "preview_cleanup.txt"
@"
===========================================
Cleanup executed on: $timestamp
Backup Directory: $backupDir
Manifest: $manifest

Safe removals performed:
- Python cache files, temp files, logs
- backend/data/* contents (uploads, exports), backend/logs/*
- Redundant scripts/docs flagged
- Root duplicates removed when backend versions exist

Archived (not deleted):
- src/ (old structure) if present
- examples/ if present

Review manifest for exact file list.
===========================================
"@ | Out-File -Encoding utf8 $preview

Write-Host "Cleanup complete. Backup: $backupDir" -ForegroundColor Green
