#! /usr/bin/env sh

# Fenix Installer
# Please refer to the file `LICENSE` in the main directory for license information.
# For a high level documentation, please visit https://gitlab.com/rebornos-team/fenix/fenix-installer

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2.

sudo rm -rf build
sudo rm -rf source/_autosummary
make html
