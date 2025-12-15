<#
Simplified PowerShell equivalent of deploy/scripts/run_venv.sh
Supports: up (background), down, status, logs
Notes: This is intentionally lightweight; on Windows use a process manager (nssm / Task Scheduler) for production.
#>
param(
    [Parameter(Mandatory=$false)] [string]$cmd = "status"
)

$APP_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VENV_DIR = Join-Path $APP_DIR ".venv"
$RUN_DIR = Join-Path $APP_DIR ".run"
$LOG_DIR = Join-Path $APP_DIR ".logs"
$PY = ${env:PYTHON} ? ${env:PYTHON} : "python"

New-Item -ItemType Directory -Force -Path $RUN_DIR, $LOG_DIR | Out-Null

function Ensure-Venv {
    if (-Not (Test-Path $VENV_DIR)) {
        Write-Host "[*] Creating venv at $VENV_DIR"
        & $PY -m venv $VENV_DIR
        & (Join-Path $VENV_DIR 'Scripts\Activate.ps1')
        & python -m pip install --upgrade pip
        & python -m pip install -r (Join-Path $APP_DIR 'requirements.txt')
    } else {
        & (Join-Path $VENV_DIR 'Scripts\Activate.ps1')
    }
}

function Start-Background($script, $name) {
    Ensure-Venv
    $out = Join-Path $LOG_DIR "$name.log"
    $p = Start-Process -FilePath (Join-Path $VENV_DIR 'Scripts\python.exe') -ArgumentList @((Join-Path $APP_DIR $script)) -RedirectStandardOutput $out -RedirectStandardError $out -PassThru
    $p.Id | Out-File -FilePath (Join-Path $RUN_DIR "$name.pid") -Encoding ascii
    Write-Host "[*] $name started (pid $($p.Id))"
}

function Stop-Background($name) {
    $pidfile = Join-Path $RUN_DIR "$name.pid"
    if (Test-Path $pidfile) {
        $pid = Get-Content $pidfile | Select-Object -First 1
        try { Stop-Process -Id $pid -ErrorAction SilentlyContinue } catch {}
        Remove-Item $pidfile -ErrorAction SilentlyContinue
        Write-Host "[*] $name stopped"
    }
}

switch ($cmd) {
    'up' {
        Start-Background 'gl_controller_metrics.py' 'controller'
        Start-Background 'gl_peer.py' 'peer'
        break
    }
    'bg-up' {
        Start-Background 'gl_controller_metrics.py' 'controller'
        Start-Background 'gl_peer.py' 'peer'
        break
    }
    'down' {
        Stop-Background 'controller'
        Stop-Background 'peer'
        Stop-Background 'mesh'
        Stop-Background 'responder'
        break
    }
    'status' {
        Get-ChildItem -Path $RUN_DIR -Filter *.pid -ErrorAction SilentlyContinue | ForEach-Object {
            $name = $_.BaseName
            $pid = Get-Content $_.FullName
            if (Get-Process -Id $pid -ErrorAction SilentlyContinue) {
                Write-Host "$name: running (pid $pid)"
            } else {
                Write-Host "$name: not running (pid $pid)"
            }
        }
        break
    }
    'logs' {
        Get-ChildItem -Path $LOG_DIR -Filter *.log -ErrorAction SilentlyContinue | ForEach-Object {
            Write-Host "---- $($_.Name) ----"
            Get-Content $_.FullName -Tail 50
        }
        break
    }
    default {
        Write-Host "Usage: run_venv.ps1 up|bg-up|down|status|logs"
    }
}
