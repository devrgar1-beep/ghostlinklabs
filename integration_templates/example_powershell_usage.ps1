# Example: GhostLink PowerShell Integration
# Demonstrates how to use GhostLink AI capabilities in PowerShell

# Import the GhostLink module (adjust path as needed)
Import-Module "$PSScriptRoot\ghostlink_powershell_integration.psm1"

# Initialize GhostLink connection
Initialize-GhostLink -ApiUrl "http://localhost:8080"

# Test connection
if (Test-GhostLinkConnection) {
    Write-Host "🎉 Ready to use GhostLink!" -ForegroundColor Green
} else {
    Write-Warning "GhostLink API not available. Make sure the server is running."
    exit 1
}

# Example 1: Analyze PowerShell code
Write-Host "`n🔍 Example 1: Code Analysis" -ForegroundColor Cyan
$sampleCode = @'
function Get-UserInfo {
    param($username)
    $user = Get-ADUser $username -Properties *
    return $user
}
'@

$analysis = $sampleCode | Analyze-PowerShellCode -IncludeSuggestions
Write-Host "Analysis complete!" -ForegroundColor Green

# Example 2: Get AI suggestions
Write-Host "`n🤖 Example 2: AI Suggestions" -ForegroundColor Cyan
$suggestions = Get-GhostLinkSuggestion -Context "I need to optimize a PowerShell script that processes CSV files" -Task "scripting"
Write-Host "Got $($suggestions.Count) suggestions!" -ForegroundColor Green

# Example 3: Optimize a script
Write-Host "`n🔧 Example 3: Script Optimization" -ForegroundColor Cyan

# Create a sample script to optimize
$sampleScript = @"
# Inefficient script
$files = Get-ChildItem *.txt
foreach ($file in $files) {
    $content = Get-Content $file.FullName
    $lineCount = $content.Count
    Write-Host "$($file.Name): $lineCount lines"
}
"@

# Save to temp file
$tempScript = [System.IO.Path]::GetTempFileName() + ".ps1"
$sampleScript | Set-Content $tempScript

# Optimize it
$optimization = Optimize-PowerShellScript -Path $tempScript
Write-Host "Optimization complete!" -ForegroundColor Green

# Clean up
Remove-Item $tempScript

# Example 4: Session monitoring
Write-Host "`n📊 Example 4: Session Monitoring" -ForegroundColor Cyan
Start-GhostLinkMonitoring -SessionName "Demo-Session" -IncludePerformance

# Run some commands to monitor
Get-Process | Select-Object -First 5 | Format-Table
Get-Service | Where-Object {$_.Status -eq 'Running'} | Select-Object -First 3
Get-ChildItem $env:TEMP | Measure-Object

# Stop monitoring and get insights
Stop-GhostLinkMonitoring

Write-Host "`n✨ GhostLink PowerShell integration demo complete!" -ForegroundColor Magenta