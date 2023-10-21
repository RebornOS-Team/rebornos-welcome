# RebornOS Welcome Application

[![Discord Server](https://dcbadge.vercel.app/api/server/cU5s6MPpQH?style=flat)](https://discord.gg/cU5s6MPpQH)
![GitHub](https://img.shields.io/github/license/rebornos-team/rebornos-welcome)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/rebornos-team/rebornos-welcome)
[![Release](https://github.com/RebornOS-Team/rebornos-welcome/actions/workflows/release.yml/badge.svg)](https://github.com/RebornOS-Team/rebornos-welcome/actions/workflows/release.yml)
[![Pre-Release (Git)](https://github.com/RebornOS-Team/rebornos-welcome/actions/workflows/pre_release.yml/badge.svg)](https://github.com/RebornOS-Team/rebornos-welcome/actions/workflows/pre_release.yml)


RebornOS Welcome is the application that displays on the RebornOS ISO and on first use of RebornOS after installation. 
It contains basic links to help get started on RebornOS as a new user.

## Useful locations

- [The License](LICENSE)
- [The Changelog](CHANGELOG.md)
- [The Contributing Guidelines](CONTRIBUTING.md)
  
- [The UI Code](user_interface/gtk/code/main.py)
- [The UI Forms](user_interface/gtk/forms/main.glade)
- [The Main Executable](main.py)


## Cloning

In order to download the source code to your local computer for testing, or for development, you can clone from the remote repository using either SSH, or HTTPS. Below are instructions on how to do so using GitHub hosted code as remote.

### HTTPS

```bash
git clone https://github.com/RebornOS-Team/rebornos-welcome.git 
```

OR

### SSH

```bash
git clone git@github.com:RebornOS-Team/rebornos-welcome.git
```

## Packaging

Change to the project directory (`cd crebornos-welcome`) and run any of the below scripts:
- `sh packaging/setup.sh <MODE>`: Builds and installs a package
- `sh packaging/build-package.sh <MODE>`: Just builds a package without installing it locally
- `sh packaging/install-package.sh <MODE>`: Just installs a package locally, except if no built package is detected, a package is built.
 
OR

- `sh packaging_iso/setup.sh <MODE>`: Builds and installs a package
- `sh packaging_iso/build-package.sh <MODE>`: Just builds a package without installing it locally
- `sh packaging_iso/install-package.sh <MODE>`: Just installs a package locally, except if no built package is detected, a package is built.

where `<MODE>` can be one of the below
     1. `local`: Selects *rebornos-welcome-local* from the local project that you have cloned already.
     2. `git`: Selects *rebornos-welcome-git* from the latest git commit.
     3. `stable`: Selects *rebornos-welcome* from the git tag corresponding to the [`pkgver` specified in the PKGBUILD](https://github.com/RebornOS-Team/rebornos-welcome/blob/main/packaging/rebornos-welcome/PKGBUILD#L5). If `pkgver=0.1.2`, then the git tag `v0.1.2` is used for packaging. 
     
> **Note**: Any additional parameters passed to the above scripts are automatically sent to `makepkg` or `pacman` (whichever is applicable).

