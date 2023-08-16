#! /usr/bin/env sh

# RebornOS Welcome
# Please refer to the file `LICENSE` in the main directory for license information.
# For a high level documentation, please visit https://github.com/RebornOS-Team/rebornos-welcome

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2.

# Install Python dev tools
echo [ RebornOS Welcome Application ]
echo "Installing \`python\` and \`pip\`..."
sudo pacman -S --needed --noconfirm python python-pip
echo "Installing \`pipenv\` through \`pip\`"...
sudo pip install pipenv

# Install other packages
echo "Installing \`xdg-utils\`..."
sudo pacman -S --needed --noconfirm xdg-utils

# Install runtime dependencies
echo "Installing runtime dependencies..."
pipenv install

# Adding permissions
echo "Giving executable permissions to \`rebornos-welcome.sh\`..."
sudo chmod +x rebornos-welcome.sh

echo ""
echo "Setup completed. Please refer to the above messages for any errors..."
