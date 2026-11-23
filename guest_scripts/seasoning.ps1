Write-Host "[*] Starting Benign User Activity Simulation..."
$browser = Start-Process msedge.exe -ArgumentList "https://en.wikipedia.org/wiki/Cybersecurity" -PassThru
Start-Sleep -Seconds 5
$docPath = "$env:USERPROFILE\Documents\Q4_Financial_Report.txt"
"Confidential Quarterly Overview - Approved" | Out-File -FilePath $docPath
Start-Sleep -Seconds 2
Test-Connection -ComputerName 8.8.8.8 -Count 2 | Out-Null
Stop-Process -Id $browser.Id -Force -ErrorAction SilentlyContinue
Write-Host "[+] Seasoning complete."
