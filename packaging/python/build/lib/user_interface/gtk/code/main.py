# RebornOS Welcome
# Please refer to the file `LICENSE` in the main directory for license information. 
# For a high level documentation, please visit https://gitlab.com/rebornos-team/applications/rebornos-welcome

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2. 

# IMPORTS
import os # for filepath related methods
import gi # Python GObject introspection module which contains Python bindings and support for Gtk
gi.require_version('Gtk', '3.0') # make sure that the Gtk version is at the required level
from gi.repository import Gtk, GLib # Gtk related modules for the graphical interface
from argparse import Namespace
from typing import List
from pathlib import Path
import logging

# FENIX IMPORTS
from fenix_library.configuration import JSONConfiguration
from fenix_library.running import LoggingHandler, LogMessage, Command

logger = logging.getLogger('rebornos_welcome.ui.gtk.code'+'.'+ Path(__file__).stem)

# THE EVENT HANDLER
class Main:  
    """
    Specify how this particular Gtk container handles user interaction events. 
    The names of handler functions (also called `signals` in Gtk) can be assigned in `Glade` under "Signals

    TODO
    ----
    - Splash screen before loading the pages and the main window, to avoid delay in getting some UI up for the user

    """

    def __init__(self, commandline_arguments: Namespace) -> None:
        """
        Initialize the main window in Gtk

        Parameters
        ----------
        commandline_arguments: Namespace
            Contains the command line arguments
        """

        self.logging_handler = LoggingHandler(logger=logger)

        LogMessage.Info("Creating a Gtk Builder and importing the UI from glade files...").write(self.logging_handler)
        builder = Gtk.Builder()
        builder.add_from_file( # extract the main form from the glade file
            os.path.join(
                "user_interface",
                commandline_arguments.user_interface,
                "forms",
                "main.glade"
            )
        ) 
        builder.connect_signals(self) # connect the signals from the Gtk forms to our event handlers (which are all defined in a class)

        LogMessage.Info("Displaying the main window...").write(self.logging_handler)
        builder.get_object("main").set_title("Welcome to RebornOS!")
        builder.get_object("main").show_all() # get the main form object and make it visible

        LogMessage.Info("Starting the event loop...").write(self.logging_handler)
        Gtk.main() # start the GUI event loop

    def on_close(self, _):

        """
        Quit the graphical interface

        Called when the application is closedMainFormHandler
        """

        Gtk.main_quit() # Quit from the Gtk UI

    def on_website_clicked(self, _):
        # command = Command(["ping", "-c", "5", "www.google.com"])
        # LogMessage.Info("Before ping...").write(self.logging_handler)
        # print("Before ping print...")
        # command.run_and_log(self.logging_handler)
        # LogMessage.Info("After ping...").write(self.logging_handler)
        # print("After ping print...")

        # command = Command(["ping", "-c", "5", "www.amazon.com"])
        # LogMessage.Info("Before ping 2...").write(self.logging_handler)
        # print("Before ping 2 print...")
        # command.run_and_log(self.logging_handler)
        # LogMessage.Info("After ping 2...").write(self.logging_handler)
        # print("After ping 2 print...")

        command = Command(["xdg-open", "https://rebornos.org/"])
        # LogMessage.Info("Before xdg-open...").write(self.logging_handler)
        # print("Before xdg-open print...")
        command.run_and_log(self.logging_handler)
        # LogMessage.Info("After xdg-open...").write(self.logging_handler)
        # print("After xdg-open print...")

    def on_rebornos_wiki_clicked(self, _):
        command = Command(["xdg-open", "https://osdn.net/projects/rebornos/wiki/TitleIndex"])
        command.run_and_log(self.logging_handler)
    
    def on_arch_wiki_clicked(self, _):
        command = Command(["xdg-open", "https://wiki.archlinux.org/"])
        command.run_and_log(self.logging_handler)

    def on_service_status_clicked(self, _):
        command = Command(["xdg-open", "https://status.rebornos.org/"])
        command.run_and_log(self.logging_handler)

    def on_discord_clicked(self, _):
        command = Command(["xdg-open", "https://discord.gg/cU5s6MPpQH"])
        command.run_and_log(self.logging_handler)

    def on_forum_clicked(self, _):
        command = Command(["xdg-open", "https://rebornos.discourse.group/"])
        command.run_and_log(self.logging_handler)

    def on_facebook_clicked(self, _):
        command = Command(["xdg-open", "https://www.facebook.com/rebornos/"])
        command.run_and_log(self.logging_handler)
    
    def on_twitter_clicked(self, _):
        command = Command(["xdg-open", "https://twitter.com/rebornoslinux"])
        command.run_and_log(self.logging_handler)

    def on_feedback_clicked(self, _):
        command = Command(["xdg-open", "https://rebornos.org/pixpopup-item/feedback/"])
        command.run_and_log(self.logging_handler)

    def on_donate_clicked(self, _):
        command = Command(["xdg-open", "https://rebornos.org/donate/"])
        command.run_and_log(self.logging_handler)

    def on_project_clicked(self, _):
        command = Command(["xdg-open", "https://gitlab.com/rebornos-team"])
        command.run_and_log(self.logging_handler)

    def on_about_us_clicked(self, _):
        command = Command(["xdg-open", "https://rebornos.org/about-us/"])
        command.run_and_log(self.logging_handler)
