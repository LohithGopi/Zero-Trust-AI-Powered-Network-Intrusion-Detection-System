# Script to permit standard user packet capture in Npcap without running as Administrator
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Elevating to Administrator to update Npcap driver settings..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "Updating Npcap Driver Security Parameters..." -ForegroundColor Cyan
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Services\npcap\Parameters" -Name "AdminOnly" -Value 0 -Force
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Services\npcap\Parameters" -Name "WinPcapCompatible" -Value 1 -Force
Restart-Service npcap
Write-Host "Done! Npcap is now configured to allow non-admin packet capture." -ForegroundColor Green
Read-Host -Prompt "Press Enter to exit"
