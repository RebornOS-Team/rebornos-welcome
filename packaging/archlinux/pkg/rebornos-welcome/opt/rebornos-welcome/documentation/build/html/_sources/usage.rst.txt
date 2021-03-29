.. _usage:

Usage
*****

**Warning**: Make sure that you have read and followed the steps in :ref:`prerequisites` before proceeding.

Running - Launching Fenix Installer
===================================

On a terminal, ensure that you are in the project base directory (:code:`fenix-installer/`) and run: 

.. code-block:: bash

    ./fenix-installer.sh

Logging - Checking for progress and issues
==========================================

After you launch **Fenix Installer**, you can keep track of the progress and check for any errors by monitoring the log. You could do it in the following ways:

    * **On the GUI**: Click on a small label at the bottom of the installer window (on the Graphical User Interface) titled :code:`Console Output` to view the execution status of commands. The console output area can be extended by pulling up the bar at its top border.

    .. image:: images/console_output.gif
        :width: 600
        :alt: A GIF showing how to open and expand the console output on the graphical interface (GUI).

    OR

    * Open in an editor: Find the latest log in :code:`fenix-installer/log/` and open it in an editor. 

    OR

    * Print the latest messages: Run :code:`tail -f $( ls -t1 |  head -n 1 )` on a terminal after changing to the :code:`fenix-installer/log/` directory.
