#! /usr/bin/env sh

(# Go into a subshell to nullify directory changes
    cd packaging/archlinux \
    && makepkg -f --noextract \
    && sudo pacman -U --noconfirm *.pkg.tar.zst \
    && gpg --detach-sign --use-agent *.pkg.tar.zst
)