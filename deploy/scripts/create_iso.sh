#!/bin/bash
set -e

# Install dependencies
sudo apt-get update
sudo apt-get install -y live-build debootstrap squashfs-tools xorriso isolinux syslinux-efi grub-pc-bin grub-efi-amd64-bin mtools dosfstools

# Create build directory
mkdir -p iso-build
cd iso-build

# Initialize live-build
lb config \
  --distribution bookworm \
  --architecture amd64 \
  --binary-images iso-hybrid \
  --bootloader grub-efi \
  --debian-installer live \
  --debian-installer-distribution bookworm \
  --archive-areas "main contrib non-free" \
  --mirror-bootstrap http://deb.debian.org/debian/ \
  --mirror-chroot http://deb.debian.org/debian/ \
  --mirror-binary http://deb.debian.org/debian/ \
  --mirror-debian-installer http://deb.debian.org/debian/

# Add custom packages
echo "openssh-server curl wget htop vim nano git python3 python3-pip" > config/package-lists/custom.list.chroot

# Add post-install script
mkdir -p config/includes.chroot/opt/ghostlink
cat > config/includes.chroot/opt/ghostlink/harden.sh << 'EOF'
#!/bin/bash
# Hardening script
echo "GhostLink OS hardening..."

# Disable root login
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

# Install basic tools
apt-get update
apt-get install -y ufw fail2ban

# Configure firewall
ufw allow ssh
ufw --force enable

# Create ghost user
useradd -m -s /bin/bash ghost
usermod -aG sudo ghost
echo 'ghost:ghostlink' | chpasswd

# Set up Swiss Army Launcher
cat > /usr/local/bin/ghostlink-launcher << 'EOF_LAUNCHER'
#!/bin/bash
while true; do
    echo "GhostLink Swiss Army Launcher"
    echo "1. Start tmux session"
    echo "2. Enter tools directory"
    echo "3. System info"
    echo "4. Shutdown"
    echo "5. Reboot"
    echo "0. Exit"
    read -p "Choice: " choice
    case $choice in
        1) tmux new -A -s ghostlink ;;
        2) cd /opt/ghostlink/tools && bash ;;
        3) echo "Hostname: $(hostname)"; echo "Kernel: $(uname -a)"; echo "Disk:"; lsblk; echo "Memory:"; free -h; read -rp 'Enter to continue...' ;;
        4) sudo shutdown -h now ;;
        5) sudo reboot ;;
        0) exit 0 ;;
        *) echo "Invalid"; sleep 1 ;;
    esac
done
EOF_LAUNCHER
chmod +x /usr/local/bin/ghostlink-launcher

# Set up systemd service
cat > /etc/systemd/system/ghostlink-launcher.service << 'EOF_SERVICE'
[Unit]
Description=GhostLink Launcher
After=network.target

[Service]
Type=simple
User=ghost
ExecStart=/usr/local/bin/ghostlink-launcher
Restart=always

[Install]
WantedBy=multi-user.target
EOF_SERVICE

systemctl enable ghostlink-launcher

echo "Hardening complete. Reboot to start launcher."
EOF
chmod +x config/includes.chroot/opt/ghostlink/harden.sh

# Build the ISO
lb build

# Move ISO to output
mkdir -p ../out
mv *.iso ../out/ghostlink-os.iso

echo "ISO built: ../out/ghostlink-os.iso"