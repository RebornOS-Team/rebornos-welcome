#! /usr/bin/env sh

pipenv uninstall fenix_library-running
pipenv install -e git+https://gitlab.com/rebornos-team/fenix/libraries/running.git#egg=fenix_library-running
