# PowerShell Lab Teardown Script
# Task 02: Legal Scope and Isolated Lab

Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "           TEARING DOWN ISOLATED PRACTICE LAB TARGET          " -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan

$connections = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($connections) {
    foreach ($conn in $connections) {
        $pidToKill = $conn.OwningProcess
        Write-Host "[*] Terminating process listening on port 3000 (PID: $pidToKill)..." -ForegroundColor Yellow
        try {
            Stop-Process -Id $pidToKill -Force -ErrorAction Stop
            Write-Host "[+] Process $pidToKill stopped successfully." -ForegroundColor Green
        } catch {
            Write-Host "[-] Could not stop process $pidToKill: $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "[i] No active process found listening on port 3000." -ForegroundColor Green
}

Write-Host "[+] Isolated lab environment successfully torn down." -ForegroundColor Green
