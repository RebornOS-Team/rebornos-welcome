.. _configuration:

Configuration - Customizing the Fenix Installer
************************************************
Configuration of **Fenix Installer** is done through :code:`JSON` files. They are similar to Python :code:`dict` s, except that **JSON** uses boolean values with the first letter not capitalized (for example, :code:`true` in **JSON** as opposed to :code:`True` in **Python**).
The configuration files are found at :code:`fenix-installer/configuration/`



installer.json
==============

.. todo::
    The documentation of installer.json

Below is a brief description of currently offered configuration variables:

:"build_directory":
    The absolute path to the directory in which you would like :code:`archiso` files to be copied before modifying them.

:"work_directory":
    The absolute path to the directory in which you would like :code:`mkarchiso` to install all the ISO packages and copies all the package caches before writing them all to an ISO.

pages.json
==============

.. todo::
    The documentation of pages.json

Below is a brief description of currently offered configuration variables:

:"build_directory":
    The absolute path to the directory in which you would like :code:`archiso` files to be copied before modifying them.

:"work_directory":
    The absolute path to the directory in which you would like :code:`mkarchiso` to install all the ISO packages and copies all the package caches before writing them all to an ISO.

system.json
============

.. todo::
    The documentation of system.json

Below is a brief description of currently offered configuration variables:

:"build_directory":
    The absolute path to the directory in which you would like :code:`archiso` files to be copied before modifying them.

:"work_directory":
    The absolute path to the directory in which you would like :code:`mkarchiso` to install all the ISO packages and copies all the package caches before writing them all to an ISO.

fenix-installer/configuration/user_selected/<mode>_mode_options.json
====================================================================

.. todo::
    The documentation of <mode>_mode_options.json

Below is a brief description of currently offered configuration variables:

:"build_directory":
    The absolute path to the directory in which you would like :code:`archiso` files to be copied before modifying them.

:"work_directory":
    The absolute path to the directory in which you would like :code:`mkarchiso` to install all the ISO packages and copies all the package caches before writing them all to an ISO.