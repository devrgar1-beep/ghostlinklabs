# ==========================================
# GHOSTLINK POWERSHELL INTEGRATION EXAMPLE
# ==========================================
# Demonstration of PowerShell 7.5.4 + GhostLink AI integration
# Shows modern PowerShell features with AI-powered automation

#Requires -Version 7.5.4

param(
    [switch]$SkipInit,
    [switch]$RunAllExamples,
    [string]$ApiUrl = "http://localhost:8080"
)

# ==========================================
# SETUP AND INITIALIZATION
# ==========================================

Write-Host "🚀 GhostLink PowerShell Integration Demo" -ForegroundColor Magenta
Write-Host "=" * 50 -ForegroundColor Magenta

# Update API URL if specified
if ($ApiUrl -ne "http://localhost:8080") {
    $script:GhostLinkConfig.ApiUrl = $ApiUrl
    Write-Host "📡 Using custom API URL: $ApiUrl" -ForegroundColor Cyan
}

# Initialize GhostLink integration
if (-not $SkipInit) {
    Write-Host "`n🔗 Initializing GhostLink..." -ForegroundColor Cyan
    $initialized = Initialize-GhostLink

    if (-not $initialized) {
        Write-Warning "GhostLink initialization failed. Some examples may not work."
        Write-Host "Press Enter to continue with available features..." -ForegroundColor Yellow
        Read-Host
    }
} else {
    # Import the module even when skipping init
    Write-Host "`n🔗 Importing GhostLink module..." -ForegroundColor Cyan
    Import-Module ./ghostlink_powershell_integration.psm1
}

# ==========================================
# EXAMPLE 1: BASIC CODE ANALYSIS
# ==========================================

function Show-CodeAnalysisExample {
    Write-Host "`n📊 Example 1: PowerShell Code Analysis" -ForegroundColor Yellow
    Write-Host "-" * 40 -ForegroundColor Yellow

    $sampleCode = @'
# Sample PowerShell script for analysis
$processes = Get-Process | Where-Object { $_.CPU -gt 10 }
foreach ($proc in $processes) {
    Write-Host "High CPU process: $($proc.Name) - CPU: $($proc.CPU)"
}
'@

    Write-Host "Analyzing sample code:" -ForegroundColor Gray
    Write-Host $sampleCode -ForegroundColor White
    Write-Host ""

    $analysis = Analyze-PowerShellCode -Code $sampleCode -AnalysisType "performance"

    if ($analysis) {
        Write-Host "✅ Analysis completed successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Analysis failed (GhostLink API may not be running)" -ForegroundColor Red
    }
}

# ==========================================
# EXAMPLE 2: SCRIPT OPTIMIZATION
# ==========================================

function Show-ScriptOptimizationExample {
    Write-Host "`n🔧 Example 2: Script Optimization" -ForegroundColor Yellow
    Write-Host "-" * 35 -ForegroundColor Yellow

    $inefficientCode = @'
# Inefficient PowerShell script
$results = @()
$services = Get-Service
foreach ($service in $services) {
    if ($service.Status -eq 'Running') {
        $results += $service
    }
}
$results | ForEach-Object { Write-Host $_.Name }
'@

    Write-Host "Original inefficient code:" -ForegroundColor Gray
    Write-Host $inefficientCode -ForegroundColor White
    Write-Host ""

    # Create temporary file for optimization
    $tempFile = [System.IO.Path]::GetTempFileName() + ".ps1"
    $inefficientCode | Out-File $tempFile -Encoding UTF8

    Write-Host "Optimizing script..." -ForegroundColor Cyan
    Optimize-PowerShellScript -Path $tempFile -Backup

    if (Test-Path $tempFile) {
        Write-Host "`nOptimized code:" -ForegroundColor Green
        Get-Content $tempFile -Raw | Write-Host -ForegroundColor White

        # Clean up
        Remove-Item $tempFile -ErrorAction SilentlyContinue
        Remove-Item "$tempFile.backup" -ErrorAction SilentlyContinue
    } else {
        Write-Host "⚠️ Optimization example skipped (file operations failed)" -ForegroundColor Red
    }
}

# ==========================================
# EXAMPLE 3: AUTOMATION TASK EXECUTION
# ==========================================

function Show-AutomationExample {
    Write-Host "`n🤖 Example 3: Automation Task Execution" -ForegroundColor Yellow
    Write-Host "-" * 40 -ForegroundColor Yellow

    Write-Host "Executing sample automation task..." -ForegroundColor Cyan

    $taskResult = Invoke-GhostLinkAutomation -Task "system-info" -Parameters @{
        "include_processes" = $true
        "include_services" = $false
        "format" = "json"
    }

    if ($taskResult) {
        Write-Host "✅ Automation task completed" -ForegroundColor Green
        Write-Host "Task output preview:" -ForegroundColor Gray
        if ($taskResult.output) {
            ($taskResult.output | ConvertFrom-Json | ConvertTo-Json -Depth 2) | Write-Host -ForegroundColor White
        }
    } else {
        Write-Host "⚠️ Automation task failed (GhostLink API may not be running)" -ForegroundColor Red
    }
}

# ==========================================
# EXAMPLE 4: SESSION MONITORING
# ==========================================

function Show-MonitoringExample {
    Write-Host "`n📊 Example 4: Session Monitoring" -ForegroundColor Yellow
    Write-Host "-" * 32 -ForegroundColor Yellow

    Write-Host "Retrieving GhostLink session information..." -ForegroundColor Cyan

    $sessionInfo = Get-GhostLinkSessionInfo

    if ($sessionInfo) {
        Write-Host "✅ Session information retrieved" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Session info retrieval failed (GhostLink API may not be running)" -ForegroundColor Red
    }

    Write-Host "`nStarting monitoring for 5 seconds..." -ForegroundColor Cyan

    $monitor = Start-GhostLinkMonitoring

    # Execute some sample commands to generate monitoring data
    Start-Sleep -Seconds 1
    Get-Process | Select-Object -First 5 | Out-Null
    Start-Sleep -Seconds 1
    Get-Service | Select-Object -First 3 | Out-Null
    Start-Sleep -Seconds 1
    Get-ChildItem | Select-Object -First 2 | Out-Null
    Start-Sleep -Seconds 1

    Stop-GhostLinkMonitoring -Event $monitor

    Write-Host "✅ Monitoring demonstration completed" -ForegroundColor Green
}

# ==========================================
# EXAMPLE 5: PARALLEL ANALYSIS
# ==========================================

function Show-ParallelAnalysisExample {
    Write-Host "`n🔄 Example 5: Parallel Script Analysis" -ForegroundColor Yellow
    Write-Host "-" * 38 -ForegroundColor Yellow

    Write-Host "Creating sample scripts for parallel analysis..." -ForegroundColor Cyan

    # Create temporary sample scripts
    $tempDir = [System.IO.Path]::GetTempPath()
    $scriptPaths = @()

    for ($i = 1; $i -le 3; $i++) {
        $scriptPath = Join-Path $tempDir "sample_script_$i.ps1"
        $scriptPaths += $scriptPath

        $sampleScript = @"
# Sample script $i for analysis
function Get-SampleData$i {
    param([int]`$Count = 10)
    1..`$Count | ForEach-Object {
        [PSCustomObject]@{
            ID = `$_
            Name = "Item_`$i`_`$($_)"
            Value = Get-Random -Minimum 1 -Maximum 100
            Timestamp = Get-Date
        }
    }
}

`$data = Get-SampleData$i -Count 5
`$data | Format-Table
"@

        $sampleScript | Out-File $scriptPath -Encoding UTF8
    }

    Write-Host "Analyzing $($scriptPaths.Count) scripts in parallel..." -ForegroundColor Cyan

    $parallelResults = Invoke-ParallelGhostLinkAnalysis -Paths $scriptPaths -MaxThreads 2

    Write-Host "`nParallel analysis results:" -ForegroundColor Green
    foreach ($result in $parallelResults) {
        Write-Host "  📄 $($result.Path): $(if ($result.Analysis) { "Analyzed" } elseif ($result.Error) { "Error: $($result.Error)" } else { "Skipped" })" -ForegroundColor White
    }

    # Clean up
    foreach ($path in $scriptPaths) {
        Remove-Item $path -ErrorAction SilentlyContinue
    }

    Write-Host "✅ Parallel analysis demonstration completed" -ForegroundColor Green
}

# ==========================================
# EXAMPLE 6: ADVANCED POWERSHELL 7.5.4 FEATURES
# ==========================================

function Show-AdvancedFeaturesExample {
    Write-Host "`n⚡ Example 6: Advanced PowerShell 7.5.4 Features" -ForegroundColor Yellow
    Write-Host "-" * 48 -ForegroundColor Yellow

    Write-Host "Demonstrating modern PowerShell features..." -ForegroundColor Cyan

    # Ternary operator (PowerShell 7+)
    $status = (Get-Service | Where-Object { $_.Status -eq 'Running' } | Measure-Object).Count -gt 10 ?
        "Many services running" : "Normal service count"
    Write-Host "  🔍 Service Status: $status" -ForegroundColor White

    # Pipeline parallel processing
    Write-Host "  🔄 Parallel pipeline processing:" -ForegroundColor White
    1..5 | ForEach-Object -Parallel {
        $num = $_
        Start-Sleep -Milliseconds (Get-Random -Minimum 100 -Maximum 500)
        [PSCustomObject]@{
            Number = $num
            Square = $num * $num
            Thread = $using:Pid
        }
    } | Format-Table | Out-Host

    # Null coalescing and conditional assignment
    $configValue = $env:GHOSTLINK_CONFIG ?? "default"
    Write-Host "  ⚙️ Config Value: $configValue" -ForegroundColor White

    # String interpolation improvements
    $version = $PSVersionTable.PSVersion
    Write-Host "  📦 PowerShell Version: $version" -ForegroundColor White

    Write-Host "✅ Advanced features demonstration completed" -ForegroundColor Green
}

# ==========================================
# MAIN EXECUTION
# ==========================================

try {
    if ($RunAllExamples) {
        Write-Host "`n🎯 Running all examples..." -ForegroundColor Green

        Show-CodeAnalysisExample
        Show-ScriptOptimizationExample
        Show-AutomationExample
        Show-MonitoringExample
        Show-ParallelAnalysisExample
        Show-AdvancedFeaturesExample
    } else {
        # Interactive menu
        Write-Host "`nSelect an example to run:" -ForegroundColor Cyan
        Write-Host "1. Code Analysis" -ForegroundColor White
        Write-Host "2. Script Optimization" -ForegroundColor White
        Write-Host "3. Automation Tasks" -ForegroundColor White
        Write-Host "4. Session Monitoring" -ForegroundColor White
        Write-Host "5. Parallel Analysis" -ForegroundColor White
        Write-Host "6. Advanced Features" -ForegroundColor White
        Write-Host "A. Run All Examples" -ForegroundColor White
        Write-Host "Q. Quit" -ForegroundColor White

        do {
            $choice = Read-Host "`nEnter your choice"

            switch ($choice.ToUpper()) {
                "1" { Show-CodeAnalysisExample }
                "2" { Show-ScriptOptimizationExample }
                "3" { Show-AutomationExample }
                "4" { Show-MonitoringExample }
                "5" { Show-ParallelAnalysisExample }
                "6" { Show-AdvancedFeaturesExample }
                "A" {
                    Show-CodeAnalysisExample
                    Show-ScriptOptimizationExample
                    Show-AutomationExample
                    Show-MonitoringExample
                    Show-ParallelAnalysisExample
                    Show-AdvancedFeaturesExample
                }
                "Q" { break }
                default { Write-Host "Invalid choice. Please try again." -ForegroundColor Red }
            }

            if ($choice.ToUpper() -ne "Q" -and $choice.ToUpper() -ne "A") {
                Write-Host "`nPress Enter to continue..." -ForegroundColor Gray
                Read-Host
            }

        } while ($choice.ToUpper() -ne "Q")
    }

} catch {
    Write-Warning "An error occurred during execution: $($_.Exception.Message)"
    Write-Host "Stack trace:" -ForegroundColor Red
    $_.ScriptStackTrace
} finally {
    Write-Host "`n👋 GhostLink PowerShell demo completed!" -ForegroundColor Magenta
    Write-Host "For more information, visit: https://ghostlink.ai/powershell" -ForegroundColor Cyan
}