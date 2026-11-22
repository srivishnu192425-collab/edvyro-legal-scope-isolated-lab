# PowerShell Lab Setup Script
# Task 02: Legal Scope and Isolated Lab

Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "       STARTING ISOLATED SECURITY PRACTICE LAB TARGET         " -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

$serverPath = Join-Path $PSScriptRoot "..\target-app\server.js"
if (-not (Test-Path $serverPath)) {
    Write-Error "Server file not found at: $serverPath"
    exit 1
}

# Check if target is already running on port 3000
$existing = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "[!] Port 3000 is already in use by PID: $($existing.OwningProcess)" -ForegroundColor Yellow
} else {
    Write-Host "[*] Launching Node.js Target Application on 127.0.0.1:3000..." -ForegroundColor Green
    $process = Start-Process node -ArgumentList $serverPath -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2
    Write-Host "[+] Target Application started with Process ID: $($process.Id)" -ForegroundColor Green
}

# Run verification script
Write-Host "`n[*] Running Isolation Verification..." -ForegroundColor Cyan
python (Join-Path $PSScriptRoot "verify_isolation.py")
