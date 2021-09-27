#! /usr/bin/env sh

(# Go into a subshell to nullify directory changes
    cd packaging/archlinux \
    && makepkg --cleanbuild --noextract --clean --force --install --syncdeps #\
    # && gpg --detach-sign --use-agent *.pkg.tar.zst
)

