#!/bin/bash

# Update and download latest version of packages
sudo apt update -y
echo "✔ Package list updated"

# Install latest versions of packages
sudo apt upgrade -y
echo "✔ Packages upgraded"

# Install and run nginx web server
sudo apt install nginx -y
echo "✔ Nginx installed and running"