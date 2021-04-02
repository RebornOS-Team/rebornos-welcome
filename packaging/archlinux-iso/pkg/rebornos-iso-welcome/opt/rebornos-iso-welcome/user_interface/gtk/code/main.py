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
from gi.repository import Gtk, GLib, GdkPixbuf # Gtk related modules for the graphical interface
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

    def __init__(self, commandline_arguments: Namespace, application_settings: JSONConfiguration) -> None:
        """
        Initialize the main window in Gtk

        Parameters
        ----------
        commandline_arguments: Namespace
            Contains the command line arguments
        """

        self.logging_handler = LoggingHandler(logger=logger)
        self.application_settings = application_settings

        LogMessage.Info("Creating a Gtk Builder and importing the UI from glade files...").write(self.logging_handler)
        self.builder = Gtk.Builder()
        self.builder.add_from_file( # extract the main form from the glade file
            os.path.join(
                "user_interface",
                commandline_arguments.user_interface,
                "forms",
                "main.glade"
            )
        ) 
        self.builder.connect_signals(self) # connect the signals from the Gtk forms to our event handlers (which are all defined in a class)

        LogMessage.Info("Displaying the main window...").write(self.logging_handler)
        self.builder.get_object("main").set_title("Welcome to RebornOS!")
        self.builder.get_object("main").show_all() # get the main form object and make it visible

        LogMessage.Debug("Detecting if the application is enabled at startup...").write(self.logging_handler)
        if self.application_settings["auto_start_enabled"]:
            self.builder.get_object("startup_toggle").set_active(True)
        else:
            self.builder.get_object("startup_toggle").set_active(False)

        if commandline_arguments.iso:
            rebornos_iso_welcome_icon_path = "media/icons/rebornos_iso_welcome_logo.svg"
            self.builder.get_object("main").set_icon_from_file(rebornos_iso_welcome_icon_path)
            about_dialog = self.builder.get_object("about")
            about_dialog.set_icon_from_file(rebornos_iso_welcome_icon_path)
            about_dialog.set_title("About RebornOS ISO Welcome Application")

            self.builder.get_object("about_application_name").set_label("RebornOS ISO Welcome Application")
            self.builder.get_object("about_logo").set_from_file(rebornos_iso_welcome_icon_path)
        else:
            self.builder.get_object("about").set_title("About RebornOS Welcome Application")

        LogMessage.Info("Starting the event loop...").write(self.logging_handler)
        Gtk.main() # start the GUI event loop

    def on_close(self, _):

        """
        Quit the graphical interface

        Called when the application is closedMainFormHandler
        """

        LogMessage.Info("User closed the application. Exiting...").write(self.logging_handler)
        # self.logging_handler.abort(wait=False)
        Gtk.main_quit() # Quit from the Gtk UI
        # exit(0)

    def on_about_clicked(self, _):
        LogMessage.Debug("Bringing up the \"About\" dialog...").write(self.logging_handler)
        self.builder.get_object("about").show_all()

    def on_log_clicked(self, _):
        LogMessage.Debug("Opening the log on the default editor...").write(self.logging_handler)
        command = Command(["xdg-open", self.application_settings["current_log_file_path"]])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_config_clicked(self, _):
        LogMessage.Debug("Opening the configuration file on the default editor...").write(self.logging_handler)
        user_settings_filepath = Path.home() / ".rebornos-welcome" / "configuration" / "settings.json"
        command = Command(
            [
                "xdg-open",
                str(user_settings_filepath.resolve())
            ]
        )
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_about_close(self, _):
        LogMessage.Debug("Hiding the \"About\" dialog...").write(self.logging_handler)
        self.builder.get_object("about").hide()

    def on_shivanandvp_mail(self, button):
        LogMessage.Debug("Opening mailing application for shivanandvp's email...").write(self.logging_handler)
        command = Command(["xdg-email", "shivanandvp@rebornos.org"])
        # command.run_and_log(self.logging_handler)
        command.start()


    def on_shivanandvp_git(self, button):
        LogMessage.Debug("Opening the git page for shivanandvp...").write(self.logging_handler)
        command = Command(["xdg-open", "https://gitlab.com/shivanandvp"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_startup_toggle(self, button):
        LogMessage.Debug("Startup checkbox toggled...").write(self.logging_handler)
        if button.get_active():
            LogMessage.Debug("Enabling auto start...").write(self.logging_handler)
            self.application_settings["auto_start_enabled"] = True
        else:
            LogMessage.Debug("Disabling auto start...").write(self.logging_handler)
            self.application_settings["auto_start_enabled"] = False
        self.application_settings.write_data()

    def on_website_clicked(self, _):
        LogMessage.Debug("Opening the RebornOS website on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://rebornos.org/"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_rebornos_wiki_clicked(self, _):
        LogMessage.Debug("Opening RebornOS Wiki on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://osdn.net/projects/rebornos/wiki/TitleIndex"])
        # command.run_and_log(self.logging_handler)
        command.start()
    
    def on_arch_wiki_clicked(self, _):
        LogMessage.Debug("Opening Arch Wiki on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://wiki.archlinux.org/"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_service_status_clicked(self, _):
        LogMessage.Debug("Opening Service Status page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://status.rebornos.org/"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_discord_clicked(self, _):
        LogMessage.Debug("Opening the Discord Server on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://discord.gg/cU5s6MPpQH"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_forum_clicked(self, _):
        LogMessage.Debug("Opening the RebornOS Forum page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://rebornos.discourse.group/"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_facebook_clicked(self, _):
        LogMessage.Debug("Opening the Facebook page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://www.facebook.com/rebornos/"])
        # command.run_and_log(self.logging_handler)
        command.start()
    
    def on_twitter_clicked(self, _):
        LogMessage.Debug("Opening the Twitter page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://twitter.com/rebornoslinux"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_feedback_clicked(self, _):
        LogMessage.Debug("Opening the Feedback page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://rebornos.org/pixpopup-item/feedback/"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_donate_clicked(self, _):
        LogMessage.Debug("Opening the donation page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://rebornos.org/donate/"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_project_clicked(self, _):
        LogMessage.Debug("Opening the Gitlab page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://gitlab.com/rebornos-team"])
        # command.run_and_log(self.logging_handler)
        command.start()

    def on_about_us_clicked(self, _):
        LogMessage.Debug("Opening the \"About us\" page on the default browser...").write(self.logging_handler)
        command = Command(["xdg-open", "https://rebornos.org/about-us/"])
        # command.run_and_log(self.logging_handler)
        command.start()


