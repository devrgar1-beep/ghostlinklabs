# Remote Deployment for GhostLink (Python + Docker)

This guide provides two paths to deploy GhostLink on a remote Linux host:

- Ansible playbook (recommended, repeatable and idempotent)
- One-shot SSH bootstrap script

It also includes a quick guide for using VS Code Remote SSH and a UFW firewall example.

---

## Ansible Method (recommended)

Prerequisites:

- Control machine: macOS/Linux with Ansible installed
- Remote host: Ubuntu/Debian with SSH access and sudo privileges

1. Install Ansible (control machine)

```bash
python3 -m pip install --user ansible
# or
brew install ansible
```

1. Set inventory host

- Edit `deploy/ansible/inventory.ini` and set `ansible_host` and `ansible_user`.

1. Run connectivity check

```bash
ansible -i deploy/ansible/inventory.ini ghostlink -m ping
```

1. Run the playbook

- Set your repository URL via `--extra-vars` (overrides the default in the playbook):

```bash
ansible-playbook \
  -i deploy/ansible/inventory.ini \
  deploy/ansible/playbook.yml \
  --extra-vars "repo_url=https://github.com/YOUR_ORG/ghostlinklabs-main.git"
```

What it does:

- Installs Docker Engine and the Compose plugin from Docker’s official repo
- Ensures your user is in the `docker` group
- Creates `/opt/ghostlink` and clones/updates the repo
- Runs `docker compose -f docker-compose.dev.yml up -d`

Notes:

- If it’s the first time the user is added to the `docker` group, you may need to log out/in for non-sudo Docker usage.

---

## SSH Bootstrap Script (simple alternative)

Use when you don’t want to install Ansible. It performs the same steps via SSH.

1. Ensure you can SSH into the host and have sudo privileges.

1. Run the script from the repo root:

```bash
HOST=youruser@your.ip.address \
REPO_URL=https://github.com/YOUR_ORG/ghostlinklabs-main.git \
./deploy/ssh_bootstrap.sh
```

What it does:

- Installs Docker Engine and the Compose plugin from Docker’s official repo (idempotent)
- Adds the user to the `docker` group
- Creates `/opt/ghostlink` and clones/updates the repo
- Runs `docker compose -f docker-compose.dev.yml up -d`

---

## VS Code Remote SSH (Dev Experience)

1. Install the VS Code extension: Remote - SSH (ms-vscode-remote.remote-ssh)

1. Add your host to `~/.ssh/config`:

```sshconfig
Host ghostlink-remote
  HostName YOUR_IP
  User YOUR_USER
  IdentityFile ~/.ssh/id_ed25519
```

1. Connect in VS Code:

- Open Command Palette → "Remote-SSH: Connect to Host…" → select `ghostlink-remote`.
- Open folder `/opt/ghostlink` on the remote to work directly on the server.

Optional: Use the included `.devcontainer/` setup to standardize local dev environments.

---

## UFW Firewall Example

On the remote host (Ubuntu), allow common ports and enable UFW:

```bash
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 8000/tcp    # App/API (example)
sudo ufw allow 9108/tcp    # Metrics/Prometheus exporter (example)
sudo ufw allow 3000/tcp    # Grafana/Frontend (example)

sudo ufw enable
sudo ufw status numbered
```

Adjust ports to match your compose/services.
