#! /usr/bin/env sh

(# Go into a subshell to nullify directory changes
    cd packaging/archlinux && makepkg -f --noextract
)