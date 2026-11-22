# PowerShell Lab Isolation Verification Script
# Task 02: Legal Scope and Isolated Lab

Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "         VERIFYING LAB NETWORK ISOLATION AND BINDING          " -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

$targetHost = "127.0.0.1"
$targetPort = 3000

# 1. Check TCP Port Listener on Loopback
Write-Host "`n[*] Test 1: Checking NetTCPConnection on Loopback..." -ForegroundColor Yellow
$connection = Get-NetTCPConnection -LocalAddress $targetHost -LocalPort $targetPort -State Listen -ErrorAction SilentlyContinue

if ($connection) {
    Write-Host "    [+] PASS: Port 3000 is listening strictly on $targetHost (PID: $($connection.OwningProcess))" -ForegroundColor Green
} else {
    Write-Host "    [-] WARNING: Specific NetTCPConnection cmdlet check did not find listener on $targetHost" -ForegroundColor Red
}

# 2. Check that target is NOT listening on all interfaces (0.0.0.0)
Write-Host "`n[*] Test 2: Checking that service is NOT listening on 0.0.0.0 (All Interfaces)..." -ForegroundColor Yellow
$wildcardConnection = Get-NetTCPConnection -LocalAddress "0.0.0.0" -LocalPort $targetPort -State Listen -ErrorAction SilentlyContinue

if ($null -eq $wildcardConnection) {
    Write-Host "    [+] PASS: Port 3000 is NOT bound to 0.0.0.0 (Not exposed globally)." -ForegroundColor Green
} else {
    Write-Host "    [-] FAIL: Port 3000 is bound to 0.0.0.0! Network isolation compromised." -ForegroundColor Red
}

# 3. HTTP Health Probe
Write-Host "`n[*] Test 3: HTTP Loopback Health Probe..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://${targetHost}:${targetPort}/health" -Method Get -TimeoutSec 3
    Write-Host "    [+] PASS: HTTP Response Received: $($response.status)" -ForegroundColor Green
    Write-Host "    [+] Environment: $($response.network_isolation)" -ForegroundColor Green
    Write-Host "    [+] Scope: $($response.authorized_scope)" -ForegroundColor Green
} catch {
    Write-Host "    [-] FAIL: HTTP Probe failed: $_" -ForegroundColor Red
}

Write-Host "`n==============================================================" -ForegroundColor Cyan
Write-Host "                  VERIFICATION COMPLETE                       " -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
