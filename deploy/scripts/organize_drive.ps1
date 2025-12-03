# PowerShell script to organize C drive files
# Leaves applications and system files alone

param(
    [string]$Path = "C:\"
)

# Directories to skip (system and applications)
$skipDirs = @(
    "C:\Windows",
    "C:\Program Files",
    "C:\Program Files (x86)",
    "C:\inetpub",
    "C:\eSupport"
)

# Function to organize a directory
function Organize-Directory {
    param([string]$dirPath)

    if ($skipDirs -contains $dirPath) {
        Write-Host "Skipping system directory: $dirPath"
        return
    }

    Write-Host "Organizing: $dirPath"

    # Create subfolders if they don't exist
    $notesDir = Join-Path $dirPath "notes"
    $docsDir = Join-Path $dirPath "docs"
    $scriptsDir = Join-Path $dirPath "scripts"
    $archivesDir = Join-Path $dirPath "archives"
    $backupsDir = Join-Path $dirPath "backups"

    New-Item -ItemType Directory -Path $notesDir -Force | Out-Null
    New-Item -ItemType Directory -Path $docsDir -Force | Out-Null
    New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
    New-Item -ItemType Directory -Path $archivesDir -Force | Out-Null
    New-Item -ItemType Directory -Path $backupsDir -Force | Out-Null

    # Move files based on extensions
    Get-ChildItem -Path $dirPath -File | ForEach-Object {
        $file = $_.FullName
        $name = $_.Name

        # Skip certain files
        if ($name -eq "README.md" -or $name -eq "main.py" -or $name -eq "config.yaml") {
            return
        }

        switch ($_.Extension) {
            ".txt" { Move-Item $file $notesDir -Force }
            ".md" { Move-Item $file $docsDir -Force }
            ".pdf" { Move-Item $file $docsDir -Force }
            ".docx" { Move-Item $file $docsDir -Force }
            ".csv" { Move-Item $file $docsDir -Force }
            ".zip" { Move-Item $file $archivesDir -Force }
            ".tgz" { Move-Item $file $archivesDir -Force }
            ".bak" { Move-Item $file $backupsDir -Force }
            ".py" { 
                # Only move .py if not main scripts
                if ($name -notmatch "^(main|setup|demo|test)_") {
                    Move-Item $file $scriptsDir -Force
                }
            }
        }
    }

    # Recursively organize subdirectories (but skip system ones)
    Get-ChildItem -Path $dirPath -Directory | ForEach-Object {
        $subDir = $_.FullName
        if ($skipDirs -notcontains $subDir) {
            Organize-Directory $subDir
        }
    }
}

# Start organizing from the specified path
Organize-Directory $Path

Write-Host "Organization complete!"