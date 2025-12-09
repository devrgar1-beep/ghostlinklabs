# ==========================================
# GHOSTLINK POWERSHELL INTEGRATION MODULE
# ==========================================
# Modern PowerShell 7.5.4 integration for GhostLink AI
# Features .NET 9.0 interop, parallel processing, and advanced automation

#Requires -Version 7.0
#Requires -Modules @{ ModuleName="Microsoft.PowerShell.Management"; ModuleVersion="7.0.0" }

using namespace System.Net.Http
using namespace System.Text.Json
using namespace System.Threading.Tasks

# ==========================================
# CONFIGURATION
# ==========================================

$script:GhostLinkConfig = @{
    ApiUrl                = "http://localhost:8080"
    ApiKey                = "ghostlink_secure_key_2025"
    ProjectRoot           = "/Users/ghost-link-labs/ghostlinklabs"
    PythonPath            = "python3"
    MaxConcurrency        = 10
    EnableExperimental    = $true
    YoloMode              = $true
    AutoApproveAll        = $true
    BypassConfirmations   = $true
    UnrestrictedExecution = $true
}

# Singleton HttpClient for reuse
$script:GhostLinkHttpClient = $null

function Get-GhostLinkHttpClient {
    if (-not $script:GhostLinkHttpClient) {
        $script:GhostLinkHttpClient = [HttpClient]::new()
        $script:GhostLinkHttpClient.Timeout = [TimeSpan]::FromSeconds(30)
        $script:GhostLinkHttpClient.DefaultRequestHeaders.Add("Authorization", "Bearer $($script:GhostLinkConfig.ApiKey)")
    }
    return $script:GhostLinkHttpClient
}

# ==========================================
# CONFIGURATION MANAGEMENT
# ==========================================

function Get-GhostLinkConfig {
    <#
    .SYNOPSIS
        Get current GhostLink configuration
    .DESCRIPTION
        Returns the current configuration hashtable
    .EXAMPLE
        Get-GhostLinkConfig
    #>
    return $script:GhostLinkConfig.Clone()
}

function Set-GhostLinkConfig {
    <#
    .SYNOPSIS
        Update GhostLink configuration
    .DESCRIPTION
        Updates the configuration with new values
    .PARAMETER Config
        New configuration hashtable
    .EXAMPLE
        Set-GhostLinkConfig @{ ApiUrl = "http://new-url:8080" }
    #>
    param([hashtable]$Config)
    foreach ($key in $Config.Keys) {
        $script:GhostLinkConfig[$key] = $Config[$key]
    }
    # Update HttpClient if API URL or key changed
    if ($Config.ContainsKey('ApiUrl') -or $Config.ContainsKey('ApiKey')) {
        if ($script:GhostLinkHttpClient) {
            $script:GhostLinkHttpClient.Dispose()
            $script:GhostLinkHttpClient = $null
        }
    }
}

# ==========================================
# UTILITY FUNCTIONS
# ==========================================

function Initialize-GhostLink {
    <#
    .SYNOPSIS
        Initialize GhostLink PowerShell integration
    .DESCRIPTION
        Sets up the GhostLink environment and validates connectivity
    .EXAMPLE
        Initialize-GhostLink
    #>
    [CmdletBinding()]
    param()

    Write-Host "🔗 Initializing GhostLink PowerShell Integration..." -ForegroundColor Cyan

    # Validate PowerShell version
    if ($PSVersionTable.PSVersion -lt [version]"7.5.4") {
        Write-Warning "PowerShell 7.5.4+ required. Current version: $($PSVersionTable.PSVersion)"
        return $false
    }

    # Test API connectivity
    $connected = Test-GhostLinkConnection
    if (-not $connected) {
        Write-Warning "GhostLink API not accessible at $($script:GhostLinkConfig.ApiUrl)"
        return $false
    }

    Write-Host "✅ GhostLink PowerShell integration initialized successfully" -ForegroundColor Green
    return $true
}

function Test-GhostLinkConnection {
    <#
    .SYNOPSIS
        Test connection to GhostLink API
    .DESCRIPTION
        Validates connectivity to the GhostLink API endpoint
    .EXAMPLE
        Test-GhostLinkConnection
    #>
    [CmdletBinding()]
    param()

    try {
        $httpClient = Get-GhostLinkHttpClient
        $response = $httpClient.GetAsync($script:GhostLinkConfig.ApiUrl + "/health").GetAwaiter().GetResult()

        if ($response.IsSuccessStatusCode) {
            Write-Host "✅ GhostLink API connection successful" -ForegroundColor Green
            return $true
        }
        else {
            Write-Warning "GhostLink API returned status: $($response.StatusCode)"
            return $false
        }
    }
    catch {
        Write-Warning "Failed to connect to GhostLink API: $($_.Exception.Message)"
        return $false
    }
}

function Invoke-GhostLinkCodeAnalysis {
    <#
    .SYNOPSIS
        Analyze PowerShell code using GhostLink AI
    .DESCRIPTION
        Sends PowerShell code to GhostLink for analysis and optimization suggestions
    .PARAMETER Code
        The PowerShell code to analyze
    .PARAMETER AnalysisType
        Type of analysis to perform (syntax, performance, security, best-practices)
    .EXAMPLE
        Invoke-GhostLinkCodeAnalysis -Code "Get-Process | Where-Object { $_.CPU -gt 50 }"
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true)]
        [string]$Code,

        [Parameter(Mandatory = $false)]
        [ValidateSet("syntax", "performance", "security", "best-practices", "all")]
        [string]$AnalysisType = "all"
    )

    process {
        Write-Host "🔍 Analyzing PowerShell code with GhostLink AI..." -ForegroundColor Cyan

        $analysisRequest = @{
            code          = $Code
            language      = "powershell"
            analysis_type = $AnalysisType
            version       = $PSVersionTable.PSVersion.ToString()
        }

        try {
            $jsonContent = $analysisRequest | ConvertTo-Json -Depth 5
            $httpClient = Get-GhostLinkHttpClient

            $content = [System.Net.Http.StringContent]::new($jsonContent, [System.Text.Encoding]::UTF8, "application/json")
            $response = $httpClient.PostAsync($script:GhostLinkConfig.ApiUrl + "/analyze/powershell", $content).GetAwaiter().GetResult()

            if ($response.IsSuccessStatusCode) {
                $result = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult() | ConvertFrom-Json

                Write-Host "📊 Analysis Results:" -ForegroundColor Yellow
                Write-Host "  Syntax Score: $($result.syntax_score)/100" -ForegroundColor $(if ($result.syntax_score -ge 80) { "Green" } else { "Red" })
                Write-Host "  Performance Score: $($result.performance_score)/100" -ForegroundColor $(if ($result.performance_score -ge 80) { "Green" } else { "Red" })
                Write-Host "  Security Score: $($result.security_score)/100" -ForegroundColor $(if ($result.security_score -ge 80) { "Green" } else { "Red" })

                if ($result.suggestions) {
                    Write-Host "`n💡 Suggestions:" -ForegroundColor Cyan
                    foreach ($suggestion in $result.suggestions) {
                        Write-Host "  • $suggestion" -ForegroundColor White
                    }
                }

                if ($result.optimized_code) {
                    Write-Host "`n🔧 Optimized Code:" -ForegroundColor Green
                    Write-Host $result.optimized_code -ForegroundColor White
                }

                return $result
            }
            else {
                Write-Warning "Analysis failed: $($response.StatusCode)"
                return $null
            }
        }
        catch {
            Write-Warning "Analysis error: $($_.Exception.Message)"
            return $null
        }
    }
}

function Optimize-PowerShellScript {
    <#
    .SYNOPSIS
        Optimize PowerShell script using GhostLink AI
    .DESCRIPTION
        Automatically optimizes PowerShell scripts for performance and best practices
    .PARAMETER Path
        Path to the PowerShell script file
    .PARAMETER OutputPath
        Optional output path for optimized script
    .PARAMETER Backup
        Create backup of original file
    .EXAMPLE
        Optimize-PowerShellScript -Path ".\myscript.ps1"
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $false)]
        [string]$OutputPath,

        [Parameter(Mandatory = $false)]
        [switch]$Backup
    )

    if (-not (Test-Path $Path)) {
        Write-Warning "Script file not found: $Path"
        return
    }

    $code = Get-Content $Path -Raw
    $analysis = Invoke-GhostLinkCodeAnalysis -Code $code -AnalysisType "performance"

    if ($analysis -and $analysis.optimized_code) {
        if ($Backup) {
            $backupPath = $Path + ".backup"
            Copy-Item $Path $backupPath
            Write-Host "📋 Backup created: $backupPath" -ForegroundColor Yellow
        }

        $outputFile = $OutputPath ? $OutputPath : $Path
        $analysis.optimized_code | Out-File $outputFile -Encoding UTF8

        Write-Host "✅ Script optimized and saved to: $outputFile" -ForegroundColor Green
    }
    else {
        Write-Warning "Optimization failed or no improvements found"
    }
}

function Invoke-GhostLinkAutomation {
    <#
    .SYNOPSIS
        Execute automation tasks through GhostLink
    .DESCRIPTION
        Runs automated tasks using GhostLink's AI orchestration
    .PARAMETER Task
        The automation task to execute
    .PARAMETER Parameters
        Parameters for the automation task
    .EXAMPLE
        Invoke-GhostLinkAutomation -Task "code-review" -Parameters @{ "files" = @("script.ps1") }
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Task,

        [Parameter(Mandatory = $false)]
        [hashtable]$Parameters = @{}
    )

    Write-Host "🤖 Executing GhostLink automation: $Task" -ForegroundColor Cyan

    $automationRequest = @{
        task              = $Task
        parameters        = $Parameters
        execution_context = @{
            powershell_version = $PSVersionTable.PSVersion.ToString()
            platform           = $PSVersionTable.Platform
            user               = $env:USER
            working_directory  = Get-Location
        }
    }

    try {
        $jsonContent = $automationRequest | ConvertTo-Json -Depth 5
        $httpClient = Get-GhostLinkHttpClient

        $content = [System.Net.Http.StringContent]::new($jsonContent, [System.Text.Encoding]::UTF8, "application/json")
        $response = $httpClient.PostAsync($script:GhostLinkConfig.ApiUrl + "/automation/execute", $content).GetAwaiter().GetResult()

        if ($response.IsSuccessStatusCode) {
            $result = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult() | ConvertFrom-Json

            Write-Host "✅ Automation task completed successfully" -ForegroundColor Green

            if ($result.output) {
                Write-Host "`n📤 Output:" -ForegroundColor Yellow
                Write-Host $result.output -ForegroundColor White
            }

            return $result
        }
        else {
            Write-Warning "Automation failed: $($response.StatusCode)"
            return $null
        }
    }
    catch {
        Write-Warning "Automation error: $($_.Exception.Message)"
        return $null
    }
}

function Get-GhostLinkSessionInfo {
    <#
    .SYNOPSIS
        Get current GhostLink session information
    .DESCRIPTION
        Retrieves session status and metrics from GhostLink
    .EXAMPLE
        Get-GhostLinkSessionInfo
    #>
    [CmdletBinding()]
    param()

    try {
        $httpClient = Get-GhostLinkHttpClient
        $response = $httpClient.GetAsync($script:GhostLinkConfig.ApiUrl + "/session/info").GetAwaiter().GetResult()

        if ($response.IsSuccessStatusCode) {
            $sessionInfo = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult() | ConvertFrom-Json

            Write-Host "🔗 GhostLink Session Information:" -ForegroundColor Cyan
            Write-Host "  Status: $($sessionInfo.status)" -ForegroundColor $(if ($sessionInfo.status -eq "active") { "Green" } else { "Red" })
            Write-Host "  Uptime: $($sessionInfo.uptime)" -ForegroundColor White
            Write-Host "  Active Tasks: $($sessionInfo.active_tasks)" -ForegroundColor White
            Write-Host "  Memory Usage: $($sessionInfo.memory_usage)%" -ForegroundColor White
            Write-Host "  CPU Usage: $($sessionInfo.cpu_usage)%" -ForegroundColor White

            return $sessionInfo
        }
        else {
            Write-Warning "Failed to get session info: $($response.StatusCode)"
            return $null
        }
    }
    catch {
        Write-Warning "Session info error: $($_.Exception.Message)"
        return $null
    }
}

function Start-GhostLinkMonitoring {
    <#
    .SYNOPSIS
        Start real-time monitoring with GhostLink
    .DESCRIPTION
        Begins monitoring PowerShell session with GhostLink AI using PSReadLine history handler
    .EXAMPLE
        Start-GhostLinkMonitoring
    #>
    [CmdletBinding()]
    param()

    Write-Host "📊 Starting GhostLink monitoring..." -ForegroundColor Cyan

    # Use PSReadLine history handler to intercept commands
    $historyHandler = {
        param($line)

        # Send command data to GhostLink for analysis
        $monitoringData = @{
            command    = $line
            timestamp  = [DateTime]::UtcNow.ToString("o")
            session_id = $PID
        }

        try {
            $jsonContent = $monitoringData | ConvertTo-Json -Depth 5
            $httpClient = Get-GhostLinkHttpClient

            $content = [System.Net.Http.StringContent]::new($jsonContent, [System.Text.Encoding]::UTF8, "application/json")
            $response = $httpClient.PostAsync($script:GhostLinkConfig.ApiUrl + "/monitoring/command", $content).GetAwaiter().GetResult()

            if ($response.IsSuccessStatusCode) {
                Write-Host "📊 Command monitored: $line" -ForegroundColor Gray
            }
        }
        catch {
            # Silent monitoring failure
        }
    }

    # Store the handler for later removal
    $script:GhostLinkHistoryHandler = $historyHandler
    Set-PSReadLineOption -AddToHistoryHandler $historyHandler

    Write-Host "✅ GhostLink monitoring started" -ForegroundColor Green
    return $historyHandler
}

function Stop-GhostLinkMonitoring {
    <#
    .SYNOPSIS
        Stop GhostLink monitoring
    .DESCRIPTION
        Stops real-time monitoring and unregisters the history handler
    .EXAMPLE
        Stop-GhostLinkMonitoring
    #>
    [CmdletBinding()]
    param()

    if ($script:GhostLinkHistoryHandler) {
        Set-PSReadLineOption -AddToHistoryHandler $null
        $script:GhostLinkHistoryHandler = $null
        Write-Host "🛑 GhostLink monitoring stopped" -ForegroundColor Yellow
    }
    else {
        Write-Warning "No active GhostLink monitoring to stop"
    }
}

# ==========================================
# PARALLEL PROCESSING UTILITIES
# ==========================================

function Invoke-ParallelGhostLinkAnalysis {
    <#
    .SYNOPSIS
        Analyze multiple PowerShell scripts in parallel
    .DESCRIPTION
        Uses PowerShell's parallel processing to analyze multiple scripts simultaneously
    .PARAMETER Paths
        Array of script file paths to analyze
    .PARAMETER MaxThreads
        Maximum number of parallel threads
    .EXAMPLE
        Invoke-ParallelGhostLinkAnalysis -Paths @("script1.ps1", "script2.ps1", "script3.ps1")
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Paths,

        [Parameter(Mandatory = $false)]
        [int]$MaxThreads = $script:GhostLinkConfig.MaxConcurrency
    )

    Write-Host "🔄 Starting parallel analysis of $($Paths.Count) scripts..." -ForegroundColor Cyan

    $apiUrl = $script:GhostLinkConfig.ApiUrl

    $Paths | ForEach-Object -Parallel {
        $scriptPath = $_
        Write-Host "📝 Analyzing: $scriptPath" -ForegroundColor Yellow

        if (Test-Path $scriptPath) {
            $code = Get-Content $scriptPath -Raw

            # Inline analysis logic for parallel execution
            try {
                $analysisRequest = @{
                    code          = $code
                    analysis_type = "all"
                    language      = "powershell"
                } | ConvertTo-Json -Depth 5

                # Use Invoke-WebRequest for parallel compatibility
                $response = Invoke-WebRequest -Uri ($using:apiUrl + "/analyze") -Method POST -Body $analysisRequest -ContentType "application/json" -UseBasicParsing

                $analysis = $response.Content | ConvertFrom-Json
            }
            catch {
                $analysis = [PSCustomObject]@{
                    error = "Analysis error: $($_.Exception.Message)"
                }
            }

            [PSCustomObject]@{
                Path      = $scriptPath
                Analysis  = $analysis
                Timestamp = [DateTime]::UtcNow
            }
        }
        else {
            Write-Warning "File not found: $scriptPath"
            [PSCustomObject]@{
                Path      = $scriptPath
                Error     = "File not found"
                Timestamp = [DateTime]::UtcNow
            }
        }
    } -ThrottleLimit $MaxThreads
}

# ==========================================
# EXPORT MODULE MEMBERS
# ==========================================

Export-ModuleMember -Function @(
    "Initialize-GhostLink",
    "Test-GhostLinkConnection",
    "Invoke-GhostLinkCodeAnalysis",
    "Optimize-PowerShellScript",
    "Invoke-GhostLinkAutomation",
    "Get-GhostLinkSessionInfo",
    "Start-GhostLinkMonitoring",
    "Stop-GhostLinkMonitoring",
    "Invoke-ParallelGhostLinkAnalysis"
)

Export-ModuleMember -Variable @(
    "GhostLinkConfig"
)

# ==========================================
# MODULE INITIALIZATION
# ==========================================

Write-Host "🔗 GhostLink PowerShell Integration Module Loaded" -ForegroundColor Green
Write-Host "  PowerShell Version: $($PSVersionTable.PSVersion)" -ForegroundColor Gray
Write-Host "  GhostLink API: $($script:GhostLinkConfig.ApiUrl)" -ForegroundColor Gray
Write-Host "  Run 'Initialize-GhostLink' to start integration" -ForegroundColor Cyan