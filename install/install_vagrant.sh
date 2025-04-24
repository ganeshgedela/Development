#!/bin/bash

set -e

LOG_FILE="$HOME/vagrant_install_$(date +%F_%T).log"
exec > >(tee -i "$LOG_FILE") 2>&1

echo "🔄 Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "🧹 Removing any existing VirtualBox and Vagrant installations..."
sudo apt remove --purge -y virtualbox* vagrant
sudo rm -rf /opt/vagrant /usr/bin/vagrant /usr/local/bin/vagrant
sudo rm -rf ~/.vagrant.d

echo "📦 Installing dependencies..."
sudo apt install -y curl gnupg lsb-release software-properties-common apt-transport-https ca-certificates

# --- VirtualBox Installation ---
echo "📥 Adding VirtualBox GPG key and repository..."
wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo gpg --dearmor -o /usr/share/keyrings/oracle-virtualbox-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/oracle-virtualbox-archive-keyring.gpg] https://download.virtualbox.org/virtualbox/debian $(lsb_release -cs) contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list

# --- HashiCorp (Vagrant) Installation ---
echo "📥 Adding HashiCorp GPG key and repository..."
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

echo "🔄 Updating package lists..."
sudo apt update

echo "🔧 Installing VirtualBox 7.0..."
sudo apt install -y virtualbox-7.0

echo "🔧 Installing Vagrant..."
sudo apt install -y vagrant

# Verify installations
echo "✅ VirtualBox version: $(vboxmanage --version)"
echo "✅ Vagrant version: $(vagrant --version)"

echo "🎉 Installation complete!"
echo "📄 Log saved at: $LOG_FILE"

