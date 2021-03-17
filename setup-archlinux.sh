#! /usr/bin/env sh

# RebornOS Welcome
# Please refer to the file `LICENSE` in the main directory for license information.
# For a high level documentation, please visit https://gitlab.com/rebornos-team/applications/rebornos-welcome

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2.

# Install Python dev tools
echo [ Fenix Installer Initial Setup for Arch Linux ]
echo "Installing \`python\` and \`pip\`..."
sudo pacman -S --needed --noconfirm python python-pip
echo "Installing \`pipenv\` through \`pip\`"...
sudo pip install pipenv

# Install other packages
echo "Installing \`git\`, \`linux-headers\`, and \`arch-install-scripts\`..."
sudo pacman -S --needed --noconfirm git linux-headers arch-install-scripts

# Install runtime dependencies
echo "Installing runtime dependencies..."
pipenv install

# Adding permissions
echo "Giving executable permissions to \`fenix-installer.sh\`..."
sudo chmod +x fenix-installer.sh

echo ""
echo "Setup completed. Please refer to the above messages for any errors..."
