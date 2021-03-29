.. _contributing:

How to Contribute to Fenix Installer
**************************************

Testing
=======

Testing of **Fenix Installer** can be done either on a Virtual Machine, or on actual hardware, when booted into a live Arch Linux based ISO.

**WARNING**: The current status of **Fenix Installer** is such that it will **erase** the hard drive. So it is strongly advised that this be carried out on a **Virtual Machine (VM)** :underlined:`only` and **not** by booting the ISO on any actual hardware.  

1. Boot the *Live ISO* of an **Arch Linux** based distribution on a **Virtual Machine**. If you do not want to download a large ISO file, please consider building one by using `Fenix ISO Builder <https://gitlab.com/rebornos-team/fenix/fenix-iso-builder>`_ .

2. Ensure that the prerequisites listed in :ref:`prerequisites` are satisfied in the ISO.
   
3. Copy the base directory (usually named :code:`fenix-installer`) to where you can access it.

4. Modify the file :code:`fenix-installer/configuration/installer.json` to change from

    .. code-block:: JSON

        "on_a_virtual_machine": false

    to 

    .. code-block:: JSON

        "on_a_virtual_machine": true

    **WARNING**: The above change will tell **Fenix Installer** that it can run dangerous commands that can **even wipe your entire hard drive**.

5. Follow the instructions in ::ref:`usage` to run the installer 

Development
===========

1. **Runtime Prerequisites**: Follow the instructions in :ref:`prerequisites`.
   
2. **Packages**: Install the Arch Linux packages :code:`base-devel`, :code:`graphviz`, and :code:`fontconfig`.

    .. code-block:: bash

        sudo pacman -S --needed base-devel graphviz fontconfig

3. **Dev Dependencies**: Run the following commands on a terminal after changing to the project directory: 

    .. code-block:: bash

        cd fenix-installer
        sudo pipenv install --system --dev

4. **API Documentation**: Consult :ref:`api_documentation` for an overview of the code.
   
5. **Git Repository**: *Fork* or *clone* the project from its **Gitlab** page and edit the source code of the project. For the *Git* URL, please refer to :ref:`prerequisites`. 
   
6. **Code Editor**: Make sure that you have a code editor installed (like :code:`vscode`, :code:`atom`, :code:`gedit`, or an IDE like :code:`pycharm`). We recommend *VSCode* since if you open the file :code:`installer.code-workspace` (found in the directory :code:`fenix-installer/`) in *VSCode*, the :underlined:`recommended` *extensions* and *settings* are preconfigured to make your job easy and less error prone.

    .. code-block:: bash

        sudo pacman -S --needed code
   
7. **Terminal**: Of course, you also need a terminal to run commands and to debug. 

Directory Structure
~~~~~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
    A[fenix-installer-python]
    subgraph "The Back-End"
        A --> B(configuration)
        A --> C(log)
        A --> D(scripts)
    end
    subgraph "The Front-End"
        A --> L(media) 
        A --> E(user-interface)
        E --> F(gtk)
        F --> G(code)
        F --> H(forms)
        F --> K(utilities)
    end

+---+----------------+---------------------------------------------------------------------------------+
|   | Folder         | Description                                                                     |
+===+================+=================================================================================+
| 1 | configuration  | Files that store settings for Fenix. Can affect the installer behavior          |                                    
+---+----------------+---------------------------------------------------------------------------------+
| 2 | log            | Log files that contain debugging messages. File names have time stamps          |                              
+---+----------------+---------------------------------------------------------------------------------+
| 3 | media          | Multimedia files - pictures, audio and video                                    |
+---+----------------+---------------------------------------------------------------------------------+
| 4 | scripts        | Scripts that need frequent updates and modification                             |
+---+----------------+---------------------------------------------------------------------------------+
| 5 | user-interface | :code:`Python` code and UI forms for the installer window and its *pages*       |                                                
+---+----------------+---------------------------------------------------------------------------------+

Tutorial: Adding a page (Gtk UI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three parts to adding a page: 
1. Design the UI in Glade 
2. Code the page in Python 
3. Edit the configuration file

Part I. Adding a page: Design the UI form in Glade
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Design the user interface in :code:`Glade` by following a tutorial like `this <http://www.holmes4.com/wda/MyBooks/PythonGTK/PyGTK_Development-Dynamic_User_Interfaces-Glade.html>`__, **for one page** in `Glade <https://glade.gnome.org/>`__ and save the :code:`.glade` file in :code:`user-interface/gtk/forms/:`. **Note: Make sure that the main container is :code:`Gtk.Box:code:` and it houses everything else inside it. Also ensure that the Gtk ID for this is the same as the page name.**
2. Assign handler names for the signals that you will handle, corresponding to any user interaction. Check `this link <http://www.holmes4.com/wda/MyBooks/PythonGTK/PyGTK_Development-Dynamic_User_Interfaces-Glade.html>`__ again and scroll down to the section on **Signals**.
3. Save the file with a ".glade" extension (for example :code:`partitioning.glade`) in the folder :code:`user-interface/gtk/forms`.

Part II. Adding a page: Code the page in Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Make a copy of an existing page, for example :code:`user-interface/gtk/code/welcome.py` in the same folder and rename the duplicate to the same name as the glade file in Part I while preserving the .py extension (for example :code:`partitioning.py`)

2. Change the *first* demarcated section in the Python page file to modify the name of the class. For example:

    In **user-interface/gtk/code/partitioning.py**

    .. code:: python

        # ----------- Modify this ---------- #
        CURRENT_PAGE_NAME = "welcome"
        # ----------- Modify this ---------- #

   can become

    In **user-interface/gtk/code/partitioning.py**

    .. code:: python

        # ----------- Modify this ---------- #
        CURRENT_PAGE_NAME = "partitioning"
        # ----------- Modify this ---------- #

3. For readability, sections are demarcated for custom code

   a. :code:`# CUSTOM IMPORTS` section for external dependencies
   b. :code:`Custom code` section in the :code:`__init__` *method* for code to be run once in the beginning:

    .. code:: python

        # ---------- Custom code ----------- #
        # -------- Custom code ends -------- #

   c. The :code:`# EVENT HANDLERS` sectio, can define user event handlers (the names of which should already be set in the **Signals** tab on :code:`Glade`)
   d. :code:`# CUSTOM METHODS` section for *methods* (or *functions*)

Part III. Adding a page: Edit the configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In :code:`fenix-installer/configuration/pages.json`, populate "page\_directory", "added\_pages" and "mode\_templates" to include your new page

For example: > In **fenix-installer/configuration/pages.json**

.. code:: JSON

    {
        "page_directory": {
            "welcome": {
                "filename": "welcome",
                "Gtk_ID": "welcome",
                "displayed_title": "Welcome"
            },
            "introduction": {
                "filename": "introduction",
                "Gtk_ID": "introduction",
                "displayed_title": "Introduction"
            },
            "mode": {
                "filename": "mode",
                "Gtk_ID": "mode",
                "displayed_title": "Mode"
            }
        },
        "added_pages": [
            "locale",        
            "users",
            "installing",
            "finish"
        ],
        "mode_templates": {
            "semi_automatic": [
                "locale",
                "users",
                "installing",
                "finish"
            ]
        }
    }

can become

In **fenix-installer/configuration/pages.json**

.. code:: JSON

    {
        "page_directory": {
            "welcome": {
                "filename": "welcome",
                "Gtk_ID": "welcome",
                "displayed_title": "Welcome"
            },
            "introduction": {
                "filename": "introduction",
                "Gtk_ID": "introduction",
                "displayed_title": "Introduction"
            },
            "mode": {
                "filename": "mode",
                "Gtk_ID": "mode",
                "displayed_title": "Mode"
            },
            "partitioning": {
                "filename": "partitioning",
                "Gtk_ID": "partitioning",
                "displayed_title": "Partitioning"
            }
        },
        "added_pages": [        
            "locale",
            "partitioning",        
            "users",
            "installing",
            "finish"
        ],
        "mode_templates": {
            "semi_automatic": [
                "locale",
                "partitioning",
                "users",
                "installing",
                "finish"
            ]
        }
    }

In the above :code:`.json` file, 1. **"filename"** refers to the names of the .glade and .py files created for the installer. If you used "partitioning.glade" and "partitioning.py", then "filename" will be "partitioning". 2. **"Gtk\_ID"** refers to the ID assigned to the top-level Gtk.Box that you created in Part I to house all the UI. If you do not know it yet, assign an ID for it in the right hand side panel of Glade after opening the .glade file for this page. **Ensure that this is the same as the file name** 3. **"displayed\_title"** refers to the title that shows up for the corresponding page in the installer.
