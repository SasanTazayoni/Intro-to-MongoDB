#!/bin/bash

# Update and download latest version of packages
sudo apt update -y
echo "✔ Package list updated"

# Install latest versions of packages
sudo apt upgrade -y
echo "✔ Packages upgraded"

# Import MongoDB GPG key
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
echo "✔ MongoDB GPG key imported"

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
echo "✔ MongoDB repository added"

# Refresh package list to include MongoDB packages
sudo apt update -y
echo "✔ Package list refreshed"

# Install MongoDB
sudo apt install -y mongodb-org
echo "✔ MongoDB installed"

# Start MongoDB
sudo systemctl start mongod
echo "✔ MongoDB started"

# Enable MongoDB to start automatically on reboot
sudo systemctl enable mongod
echo "✔ MongoDB enabled on reboot"

# Allow external connections by changing bindIp to 0.0.0.0
sudo sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongod.conf
echo "✔ mongod.conf updated to allow external connections"

# Restart MongoDB to apply config change
sudo systemctl restart mongod
echo "✔ MongoDB restarted"