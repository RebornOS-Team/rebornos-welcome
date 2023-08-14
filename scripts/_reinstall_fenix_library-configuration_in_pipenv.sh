#! /usr/bin/env sh

pipenv uninstall fenix_library-configuration
pipenv install -e git+https://gitlab.com/rebornos-team/fenix/libraries/configuration.git#egg=fenix_library-configuration
