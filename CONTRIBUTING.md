# Contributing

## Release Checklist

- [ ] Build and test packages locally
  - [ ] `sh packaging/setup.sh local`
  - [ ] `sh packaging_iso/setup.sh local`

- [ ] Update the version, and changelog in
  - [ ] [CHANGELOG.md](CHANGELOG.md)
  - [ ] [main.glade](user_interface/gtk/forms/main.glade)
    - [ ] Version in one place
    - [ ] Version and changelog in a second place

- [ ] Update the version in 
  - [ ] [The PKGBUILD for the stable variant of the welcome app](packaging/rebornos-welcome/PKGBUILD)
  - [ ] [The PKGBUILD for the git variant of the welcome app](packaging/rebornos-welcome-git/PKGBUILD)
  - [ ] [The PKGBUILD for the local variant of the welcome app](packaging/rebornos-welcome-local/PKGBUILD)
  - [ ] [The PKGBUILD for the stable variant of the ISO welcome app](packaging_iso/rebornos-iso-welcome/PKGBUILD)
  - [ ] [The PKGBUILD for the git variant of the ISO welcome app](packaging_iso/rebornos-iso-welcome-git/PKGBUILD)
  - [ ] [The PKGBUILD for the local variant of the ISO welcome app](packaging_iso/rebornos-iso-welcome-local/PKGBUILD)

- [ ] Commit and push all changes through git, for example `git commit -m "Some message" && git push`

- [ ] Create and push a tag, for example `git tag -a v0.0.58 -m "This is version 0.0.58" && git push origin v0.0.58`
- [ ] If there was a mistake and if you want to yank the release, run something like `git tag -d v0.0.58 && git push --delete origin v0.0.58`. Then the errors can be fixed and the previous step can be repeated to create a new tag.