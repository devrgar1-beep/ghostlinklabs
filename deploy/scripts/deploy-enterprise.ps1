# ==========================================
# GhostLink Enterprise Deployment Script
# Automated setup for Dell R630 cluster with enterprise storage
# ==========================================

param(
    [string]$Profile = "",
    [switch]$Help
)

# Configuration
$ComposeFile = "docker-compose.enterprise.yml"
$K8sManifest = "k8s/ghostlink-cluster.yaml"
$RecursiveOntology = "recursive_loops/ontology.json"
$ProjectName = "ghostlink-enterprise"
$Namespace = "ghostlink-system"
$NetworkSubnet = "192.168.1.0/24"
$Gateway = "192.168.1.1"

# Colors for output (PowerShell)
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"

# Logging functions
function Write-LogInfo {
    param([string]$Message)
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] [INFO] $Message" -ForegroundColor $Blue
}

function Write-LogSuccess {
    param([string]$Message)
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] [SUCCESS] $Message" -ForegroundColor $Green
}

function Write-LogWarning {
    param([string]$Message)
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] [WARNING] $Message" -ForegroundColor $Yellow
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] [ERROR] $Message" -ForegroundColor $Red
}

# Pre-deployment checks
function Test-Prerequisites {
    Write-LogInfo "Checking prerequisites..."

    # Check if Docker is installed and running
    try {
        $dockerVersion = docker version 2>$null
        if ($LASTEXITCODE -ne 0) {
            throw "Docker not available"
        }
    } catch {
        Write-LogError "Docker is not installed or not running. Please install/start Docker first."
        exit 1
    }

    # Check if Docker Compose is available
    try {
        if (Get-Command "docker-compose" -ErrorAction SilentlyContinue) {
            $composeVersion = docker-compose version 2>$null
        } elseif (docker compose version 2>$null) {
            # Docker Compose V2
        } else {
            throw "Docker Compose not available"
        }
    } catch {
        Write-LogError "Docker Compose is not available. Please install Docker Compose."
        exit 1
    }

    # Check available disk space (need at least 50GB)
    $availableSpace = (Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DeviceID -eq 'C:' }).FreeSpace
    if ($availableSpace -lt 53687091200) {
        # 50GB in bytes
        Write-LogWarning "Low disk space detected. Ensure at least 50GB free space."
    }

    Write-LogSuccess "Prerequisites check passed"
}

# Create Docker network
function New-DockerNetwork {
    Write-LogInfo "Creating Docker network..."

    $networkExists = docker network ls --format "{{.Name}}" | Select-String -Pattern "ghostlink-enterprise-br0"
    if ($networkExists) {
        Write-LogInfo "Network already exists, skipping creation"
    } else {
        docker network create `
            --driver bridge `
            --subnet="$NetworkSubnet" `
            --gateway="$Gateway" `
            --opt com.docker.network.bridge.name=ghostlink-enterprise-br0 `
            --opt com.docker.network.bridge.enable_icc=true `
            --opt com.docker.network.bridge.enable_ip_masquerade=true `
            ghostlink-enterprise-br0

        Write-LogSuccess "Docker network created"
    }
}

# Validate configuration
function Test-Configuration {
    Write-LogInfo "Validating configuration..."

    # Check if compose file exists
    if (!(Test-Path $ComposeFile)) {
        Write-LogError "Compose file $ComposeFile not found"
        exit 1
    }

    # Validate compose file
    try {
        if (Get-Command "docker-compose" -ErrorAction SilentlyContinue) {
            docker-compose -f $ComposeFile config > $null
        } else {
            docker compose -f $ComposeFile config > $null
        }
    } catch {
        Write-LogError "Configuration validation failed: $($_.Exception.Message)"
        exit 1
    }

    Write-LogSuccess "Configuration validation passed"
}

# Deploy services
function Start-Services {
    param([string]$ProfileName)

    Write-LogInfo "Deploying GhostLink Enterprise services..."

    $composeArgs = @("-f", $ComposeFile, "-p", $ProjectName)

    if ($ProfileName) {
        Write-LogInfo "Using profile: $ProfileName"
        $composeArgs += @("--profile", $ProfileName)
    }

    $composeArgs += @("up", "-d")

    # Use appropriate compose command
    try {
        if (Get-Command "docker-compose" -ErrorAction SilentlyContinue) {
            & docker-compose $composeArgs
        } else {
            & docker compose $composeArgs
        }
    } catch {
        Write-LogError "Failed to deploy services: $($_.Exception.Message)"
        exit 1
    }

    Write-LogSuccess "Services deployed successfully"
}

# Wait for services to be healthy
function Wait-ServicesHealthy {
    Write-LogInfo "Waiting for services to become healthy..."

    $maxAttempts = 60
    $attempt = 1

    while ($attempt -le $maxAttempts) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost/health" -TimeoutSec 10 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                Write-LogSuccess "Services are healthy"
                return $true
            }
        } catch {
            # Service not ready yet
        }

        Write-LogInfo "Waiting for services... (attempt $attempt/$maxAttempts)"
        Start-Sleep -Seconds 10
        $attempt++
    }

    Write-LogError "Services failed to become healthy within timeout"
    return $false
}

# Setup monitoring
function Initialize-Monitoring {
    Write-LogInfo "Setting up monitoring stack..."

    # Wait for Grafana to be ready
    Start-Sleep -Seconds 30

    # Import dashboards (if any exist)
    if (Test-Path "monitoring/grafana/dashboards") {
        Write-LogInfo "Grafana dashboards directory found"
    }

    Write-LogSuccess "Monitoring setup completed"
}

# Validate recursive loop ontology
function Test-RecursiveOntology {
    Write-LogInfo "Validating recursive loop ontology..."

    if (!(Test-Path $RecursiveOntology)) {
        Write-LogError "Recursive ontology file $RecursiveOntology not found"
        exit 1
    }

    try {
        $ontology = Get-Content $RecursiveOntology -Raw | ConvertFrom-Json
        Write-LogSuccess "Recursive ontology validation passed"
        return $ontology
    } catch {
        Write-LogError "Recursive ontology validation failed: $($_.Exception.Message)"
        exit 1
    }
}

# Deploy Kubernetes cluster (optional)
function Install-KubernetesCluster {
    param([string]$ManifestPath)

    Write-LogInfo "Deploying Kubernetes cluster..."

    if (!(Test-Path $ManifestPath)) {
        Write-LogWarning "Kubernetes manifest not found, skipping K8s deployment"
        return $false
    }

    try {
        # Check if kubectl is available
        $kubectlVersion = kubectl version --client 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-LogWarning "kubectl not found, skipping Kubernetes deployment"
            return $false
        }

        # Apply the manifest
        kubectl apply -f $ManifestPath
        if ($LASTEXITCODE -eq 0) {
            Write-LogSuccess "Kubernetes cluster deployed successfully"
            return $true
        } else {
            Write-LogError "Kubernetes deployment failed"
            return $false
        }
    } catch {
        Write-LogWarning "Kubernetes deployment encountered issues: $($_.Exception.Message)"
        return $false
    }
}

# Display deployment information
function Show-DeploymentInfo {
    Write-LogSuccess "GhostLink Enterprise deployment completed!"
    Write-Host ""
    Write-Host "Service Endpoints:" -ForegroundColor $Green
    Write-Host "=================="
    Write-Host "Main API:         http://localhost/api/"
    Write-Host "API Docs:         http://localhost/api/docs"
    Write-Host "Grafana:          http://localhost:3000"
    Write-Host "Prometheus:       http://localhost:9090"
    Write-Host "Ollama API:       http://localhost:11434"
    Write-Host ""
    Write-Host "Network Information:" -ForegroundColor $Green
    Write-Host "===================="
    Write-Host "Controller:       192.168.1.100"
    Write-Host "Training Node:    192.168.1.101"
    Write-Host "Inference Node:   192.168.1.102"
    Write-Host "MD3600i Storage:  192.168.1.103"
    Write-Host "Synology NAS:     192.168.1.104-192.168.1.106"
    Write-Host ""
    Write-Host "Management Commands:" -ForegroundColor $Green
    Write-Host "===================="
    Write-Host "View logs:        docker-compose -f $ComposeFile -p $ProjectName logs -f"
    Write-Host "Stop services:    docker-compose -f $ComposeFile -p $ProjectName down"
    Write-Host "Scale training:   docker-compose -f $ComposeFile -p $ProjectName up -d --scale ghostlink-trainer=2"
    Write-Host "Update services:  docker-compose -f $ComposeFile -p $ProjectName pull && docker-compose -f $ComposeFile -p $ProjectName up -d"
}

# Main deployment function
function Main {
    if ($Help) {
        Write-Host "Usage: .\deploy-enterprise.ps1 [-Profile <profile>] [-Help]"
        Write-Host ""
        Write-Host "Parameters:"
        Write-Host "  -Profile    Deployment profile (training, inference, monitoring)"
        Write-Host "  -Help       Show this help message"
        Write-Host ""
        Write-Host "Profiles:"
        Write-Host "  training    - Deploy training services only"
        Write-Host "  inference   - Deploy inference services only"
        Write-Host "  monitoring  - Deploy monitoring stack only"
        Write-Host "  (default)   - Deploy all services"
        exit 0
    }

    Write-Host "=========================================" -ForegroundColor $Green
    Write-Host "GhostLink Enterprise Deployment"
    Write-Host "=========================================" -ForegroundColor $Green

    Test-Prerequisites
    New-DockerNetwork
    Test-Configuration
    $ontology = Test-RecursiveOntology
    Start-Services -ProfileName $Profile
    $k8sDeployed = Install-KubernetesCluster -ManifestPath $K8sManifest
    $healthy = Wait-ServicesHealthy
    if ($healthy) {
        Initialize-Monitoring
        Show-DeploymentInfo
        Write-Host ""
        Write-LogSuccess "Deployment completed successfully! 🎉"
        if ($k8sDeployed) {
            Write-LogSuccess "Kubernetes cluster is active"
        }
    } else {
        Write-LogError "Deployment failed - services not healthy"
        exit 1
    }
}

# Run main function
Main