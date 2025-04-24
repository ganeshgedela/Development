#!/bin/bash

set -e

echo "🚀 Starting Docker + Docker Compose installation..."

# Step 1: Update the package list
echo "🔄 Updating package list..."
sudo apt-get update

# Step 2: Install dependencies
echo "📦 Installing required packages..."
sudo apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# Step 3: Add Docker’s GPG key
echo "🔐 Adding Docker GPG key..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Step 4: Add Docker repository
echo "📁 Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Step 5: Update again with Docker repo
echo "🔄 Updating package list again with Docker repo..."
sudo apt-get update

# Step 6: Install Docker Engine and CLI
echo "🐳 Installing Docker Engine and tools..."
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Step 7: Install Docker Compose plugin manually (latest version)
echo "🔍 Fetching latest Docker Compose plugin version..."
COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')

echo "⬇️ Installing Docker Compose v${COMPOSE_VERSION} as plugin..."
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -SL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Step 8: Add current user to docker group (optional)
echo "👤 Adding current user to docker group (optional)..."
sudo usermod -aG docker $USER

# Step 9: Show installed versions
echo "✅ Docker version:"
docker --version

echo "✅ Docker Compose version:"
docker compose version

echo "🎉 Installation complete! Please log out and back in to use Docker without sudo."
