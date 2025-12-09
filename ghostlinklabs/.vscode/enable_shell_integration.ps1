# VS Code Shell Integration enablement script for PowerShell

# This script registers the VS Code shell integration snippet for Windows PowerShell.
# It will NOT modify the user's $Profile automatically. Run with admin privileges if you want to persist.

try {
    $codeExe = 'code'
    # Try locating the shell integration script for pwsh (PowerShell Core) and then fallback to powershell
    $shellPath = & $codeExe --locate-shell-integration-path pwsh 2>$null
    if (-not $shellPath) {
        $shellPath = & $codeExe --locate-shell-integration-path powershell 2>$null
    }

    if ($shellPath) {
        Write-Host "Found shell integration script at: $shellPath"
        Write-Host 'To enable shell integration, add the following line to your PowerShell profile ($Profile):'
        Write-Host "`nif ($env:TERM_PROGRAM -eq 'vscode') { . \"$shellPath\" }`n"
        Write-Host 'You can automatically add it by running:'
        Write-Host "Add-Content -Path $Profile -Value 'if ($env:TERM_PROGRAM -eq \"vscode\") { . \"$shellPath\" }'"
    } else {
        Write-Host 'Unable to locate the VS Code shell integration script. Ensure VS Code is installed and in PATH (code command available).'
    }
} catch {
    Write-Warning "Error: $_"
}
