#! /usr/bin/env sh

(
    cd documentation && make html
    ln -sf build/html/index.html documentation.html
)
