Version 0.0.53
==============
1. The auto-update is fixed to filter out an interfering -debug package that seems to be generated in recent builds.

Version 0.0.52
==============
1. The ISO Welcome app is set to only update the installer if minor changes like patches are detected (Otherwise the package would have failed to install, and needs a newer ISO).

Version 0.0.51
==============
1. Added a status bar that displays the last status from the console log.
2. The ISO Welcome app now tries to update from GitHub if possible.

Version 0.0.50
==============
Update dependencies

Version 0.0.49
==============
1. Fixed DNS Server change when `systemd-resolved` is in use.
2. Fixed CI for automated builds and automated releases.
3. Build scripts revamped.
4. Icons do not use absolute paths (thanks @SoulHarsh007).
5. Update team GitHub organization URL.

Version 0.0.47
==============
1. Advanced options tab on the installer page which reverts back to the installer page when browsing other tabs
2. New UI for advanced options with the possibility to 
   a. use toggles for "Update", install "from Github" releases (*new*), and/or use an "Unstable" installer. Incompatible toggles are automatically disabled following your choice
   b. disable/re-enable some checks that the installer performs
   c. Change DNS Servers
3. The changes from advanced options that persist in the filesystem are stored and reloaded from their last state
4. Firewalld has been replaced with GUFW for simplicity and ease of use.
5. Using curl instead of Github CLI for release downloads

Version 0.0.45
==============
1. ISO Welcome configuration can now hide "Update" and "Git" switches
2. ISO Welcome configuration now allows custom installer and installer config package names
3. Newer settings are safely accessed to account for older config files
4. Installer packages no longer downgrade if the repository version is older
5. Bug that caused window to resize late fixed
6. Provision to run post-install commands for launching utilities
7. Firewall added to utilities
8. Reclassify log levels and dull debug messages for visibility of other logs
9. Fix status not turning back to ready after installer launch
10. Update pacman databases before checking for newer versions of packages

Version 0.0.42
==============
Change the git toggle button into a switch

Version 0.0.40
==============
1) Git toggle for installer in the ISO mode
2) Launch git or release versions. Automatically install/uninstall required packages in the process

Version 0.0.39
==============
1. Font changes
2. Console fixes

Version 0.0.38
==============
1. Moved console output to the bottom and made it smart so that it opens up when the window is enlarged. Minor aesthetic changes
2. Added overlays on titlebars with CSS theming

Version 0.0.37
==============
1. Fixes in UI sizing

Version 0.0.36
==============
1. More compact UI
2. Installation button style in ISO mode

Version 0.0.35
==============
1. Removed pyakm as it is no longer developed

Version 0.0.34
==============
1. All launches detached: close welcome without closing things you launched.
2. Red/Green signals to indicate busy status
3. Console now available in all pages
4. Greatly simplify UI and fit components better
5. Bug fixes

Version 0.0.33
==============
1. Separate working dirs for ISO and regular modes
2. refresh-mirrors installation fixed
3. Mandatory versioning of configs and replacement of old user configs

Version 0.0.30
==============
1. Launch improvements
2. Installer fix

Version 0.0.29
==============
1. Replace Cnchi with Calamares on the ISO version
2. Fix executable launching 

Version 0.0.28
==============
Rebuilt for Python v3.10

Version 0.0.27
==============

1. Fixed extra log permissions and moved the log to home by default
2. Error handling for when the log file cannot be created

Version 0.0.26
==============

1) The `About` and `Close` buttons now follow the same style as the other buttons, so background issues are reduced.

2) Changelog background is made dark to be consistent. 

3) Changelong font changed and removed custom color and highlighting
   
4) RebornOS FIRE launch button made lighter to prevent text from blending in some themes.

Version 0.0.25
==============

1) Added `rebornos-fire` launch button centered at the top, separate from the grid of applications. The button displays in RebornOS logo's dark blue color in most themes (an exception being Adwaita).

2) A new pop-up dialog that displays when the "Utilities" page is visible to tell the user that apps are not pre-installed, but will be installed before launch. The dialog can be hidden for future visits by unchecking a checkbox (which can be re-enabled in the configuration file).

3) Changed permissions of .desktop files from 755 to 644 in the PKGBUILDS of both regular and ISO versions.

4) Changed launch script to not use pipenv and created separate launch scripts for pipenv launches. New launch script for the ISO version, taking any extra arguments.

5) Fixed symlinks in `/usr/bin` to point to the correct launch script paths. Can be run as `rebornos-welcome` or `rebornos-iso-welcome`. Changed `.desktop` files to use these shortcuts.

6) Replaced manual installations and deletions after makepkg with makepkg arguments.

7) New key in the application configuration called "show_install_info" to toggle an information dialog about installation. Failsafe implemented to create the key if it does not exist in older configuration files from previous versions of the application.

8) New function for the launch of detached processes that do not get terminated even if the Welcome app is immedietly closed after launching the process. Handles both executables and commands. 

9)  Replaced `yay` with `pacman`.

10) Consistent use of CSS to theme the inner and outer background colors (a two-tone style). 

11) In the ISO version, replaced .desktop launches with full path of the executables of Cnchi.

12) Changed relative to absolute path within the launch scripts while following any symlink.

Version 0.0.22
==============
Fixed the installer selection text in the ISO mode

Version 0.0.21
==============

1) Font for the RebornOS and Welcome logo (ttf-righteous-regular) added as a dependency

2) Added the installer selection and launcher in the ISO mode.

3) Fixed size inefficiences by loading pages after determining the launch mode.

Version 0.0.20
==============

Recover from corrupted settings file.

Version 0.0.19
==============

Replaced `reflector-simple` with `refresh-mirrors-rebornos`, which runs `rate-mirrors`. 

Version 0.0.18
==============

Fixed changelog scaling.

Version 0.0.17
==============

Fixed missing top image.

Version 0.0.16
==============

1) Windows are made resizeable: It took time to do this because I had used image overlays for a hacky way to set colored backgrounds. They only worked for fixed sizes. I finally learnt the basics of how to use CSS to decorate Gtk widgets and made them look almost the same as how they had when I used image overlays. This part took me a while to get right, with manual adjustments to widget sizes and layouts until they looked "correct".

2) Scrollbars appear for vertical scrolling: When widgets overflow due to font scaling, vertical scrollbars appear automatically.

3) The color shades have been changed a bit to look better in various different dark and light themes.

4) The container sizes have been adjusted to look good in various different themes.

5) The "About" Window has undergone an overhaul with margins, alignments, background color, and a changelog button!