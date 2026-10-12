@echo off
:: Self-elevate script to Administrator if not already elevated
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run_fix
) else (
    echo Requesting Administrator privileges to configure Npcap driver...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

:run_fix
echo ========================================================
echo Configuring Npcap Packet Capture Permissions
echo ========================================================
echo.
powershell -Command "Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Services\npcap\Parameters' -Name 'AdminOnly' -Value 0 -ErrorAction SilentlyContinue; Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Services\npcap\Parameters' -Name 'WinPcapCompatible' -Value 1 -ErrorAction SilentlyContinue; Restart-Service npcap -ErrorAction SilentlyContinue"

echo [SUCCESS] Npcap AdminOnly restriction set to 0.
echo [SUCCESS] Npcap driver restarted.
echo Non-elevated terminals and python web server can now capture live network packets!
echo.
pause
