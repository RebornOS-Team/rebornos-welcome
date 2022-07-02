#! /usr/bin/env sh

(# Go into a subshell to nullify directory changes
    cd packaging/archlinux-iso \
    && makepkg --cleanbuild --noextract --clean --force --syncdeps "$@" #\
    # && gpg --detach-sign --use-agent *.pkg.tar.zst
)