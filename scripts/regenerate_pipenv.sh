#! /usr/bin/env sh

# Clean pipenv
pipenv uninstall fenix-library-running fenix-library-configuration numpy vext vext.gi sphinx sphinx-rtd-theme sphinxcontrib-mermaid pygobject pipenv
sudo pipenv uninstall fenix-library-running fenix-library-configuration numpy vext vext.gi sphinx sphinx-rtd-theme sphinxcontrib-mermaid pygobject pipenv
pipenv clean
sudo pipenv clean
pipenv --rm
sudo pipenv --rm

# Check if pipenv is cleaned
pipenv graph
sudo pipenv graph

# Regenerate pipenv
pipenv install -e git+https://gitlab.com/rebornos-team/fenix/libraries/running.git#egg=fenix_library-running -e git+https://gitlab.com/rebornos-team/fenix/libraries/configuration.git#egg=fenix_library-configuration numpy pygobject pipenv vext vext.gi
sudo pipenv install --dev sphinx sphinx-rtd-theme sphinxcontrib-mermaid

# Check if pipenv is regenerated
pipenv graph
sudo pipenv graph