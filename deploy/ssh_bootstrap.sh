#!/usr/bin/env bash
set -euo pipefail

# Usage: HOST=user@ip REPO_URL=https://... ./deploy/ssh_bootstrap.sh

if [[ -z "${HOST:-}" || -z "${REPO_URL:-}" ]]; then
  echo "Usage: HOST=user@ip REPO_URL=https://... ./deploy/ssh_bootstrap.sh" >&2
  exit 1
fi

# Accept host key on first connect for convenience
SSH_OPTS=(
  -o StrictHostKeyChecking=accept-new
)

ssh "${SSH_OPTS[@]}" "$HOST" "REPO_URL='$REPO_URL' bash -s" <<'REMOTE_EOF'
set -euo pipefail

REPO_DIR="/opt/ghostlink"
REMOTE_USER="${SUDO_USER:-$USER}"

# Detect distro ID (ubuntu/debian)
if [[ -r /etc/os-release ]]; then
  . /etc/os-release
  DISTRO_ID="${ID}"
else
  echo "Unsupported OS: /etc/os-release not found" >&2
  exit 1
fi

# Install prerequisites
if ! command -v curl >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y ca-certificates curl gnupg lsb-release git
fi

# Install Docker from official repository (idempotent)
if ! command -v docker >/dev/null 2>&1; then
  sudo install -m 0755 -d /etc/apt/keyrings
  if [[ ! -f /etc/apt/keyrings/docker.gpg ]]; then
    curl -fsSL "https://download.docker.com/linux/${DISTRO_ID}/gpg" | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
  fi
  ARCH="$(dpkg --print-architecture)"
  CODENAME="$(. /etc/os-release; echo "$VERSION_CODENAME")"
  echo "deb [arch=${ARCH} signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${DISTRO_ID} ${CODENAME} stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
  sudo apt-get update -y
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
fi

# Ensure user is in docker group (idempotent)
if ! id -nG "$REMOTE_USER" | grep -qw docker; then
  sudo usermod -aG docker "$REMOTE_USER" || true
fi

# Prepare app directory
sudo mkdir -p "$REPO_DIR"
sudo chown "$REMOTE_USER":"$REMOTE_USER" "$REPO_DIR"

# Clone or update repository
if [[ ! -d "$REPO_DIR/.git" ]]; then
  git clone "$REPO_URL" "$REPO_DIR"
else
  cd "$REPO_DIR"
  # Try fast-forward pull; fall back to fetch
  git pull --ff-only || git fetch --all --prune
fi

cd "$REPO_DIR"
# Bring up containers (run with sudo so it works before re-login to gain docker group)
sudo docker compose -f docker-compose.dev.yml up -d

echo "Deployment complete. If this is the first time adding $REMOTE_USER to the docker group, re-login for non-sudo docker access."
REMOTE_EOF

echo "Done."
