#!/bin/bash

# Update and download latest version of packages
sudo apt update -y

# Install latest versions of packages
sudo apt upgrade -y

# Install and run nginx web server
sudo apt install nginx -y