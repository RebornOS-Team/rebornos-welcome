.. _prerequisites:

Prerequisites - What you need to run Fenix Installer
******************************************************

**Note**: Currently, **Fenix Installer** only supports **Arch Linux** and its derivatives (like *RebornOS*, *EndeavourOS*, *Manjaro*, etc.). Your build system (where you run **Fenix Installer**) should be booted into  **Arch Linux** or one of its derivates before proceeding.  

Follow :underlined:`one` of the below sections to set up **Fenix Installer** before running. The below commands must be run on a **terminal**.

Using the Setup Script
======================

1. **Download the project**:
    
    .. code-block:: bash

        git clone https://gitlab.com/rebornos-team/fenix/fenix-installer.git

2. **Run the setup script**:  

    .. code-block:: bash

        cd fenix-installer
        sh setup-archlinux.sh
        
If the script ran successfully, congratulations! You are ready to run **Fenix Installer**. Proceed to :ref:`usage` for further steps.

Manual Setup
============

**Warning**: Please skip this section if you have already run the setup script successfully.

1. **Install python dev tools**: 

    * Install the packages :code:`python` and :code:`pip`

    .. code-block:: bash
        
        sudo pacman -S --needed python python-pip

    * Install :code:`pipenv` through :code:`pip`

    .. code-block:: bash
        
        sudo pip install pipenv

3. **Install other packages**: :code:`xdg-utils` and :code:`git`

    .. code-block:: bash
            
        sudo pacman -S --needed git xdg-utils

4. **The program itself**: Download **Fenix Installer** into a directory of your choice

    .. code-block:: bash

        git clone https://gitlab.com/rebornos-team/fenix/fenix-installer.git

5. **Runtime dependencies**: Install the *python modules* required by **Fenix Installer**

    .. code-block:: bash

        cd fenix-installer
        pipenv install

6. **Executable permissions**: Provide executable permissions to the installer script

    .. code-block:: bash

        sudo chmod +x fenix-installer.sh

If you performed all the above steps successfully, congratulations! You are ready to run **Fenix Installer**. Proceed to :ref:`usage` for further steps.

