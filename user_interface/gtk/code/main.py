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
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk # Gtk related modules for the graphical interface
from argparse import Namespace
from typing import List
from pathlib import Path
import logging
import functools

# FENIX IMPORTS
from fenix_library.configuration import JSONConfiguration
from fenix_library.running import LoggingHandler, LogMessage, Command, LoggingLevel, BatchJob

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

    log_color: dict = {
        "CRITICAL": "#a40000" ,
        "ERROR": "#ff0000",
        "EXCEPTION": "#ff0000",
        "WARNING": "#ffa500",
        "INFO": "#0000ff",
        "DEBUG": "#808080",
        "NOTSET": "#808080",
        "": "#808080",
        None: "#808080"
    }

    def __init__(self, commandline_arguments: Namespace, application_settings: JSONConfiguration) -> None:
        """
        Initialize the main window in Gtk

        Parameters
        ----------
        commandline_arguments: Namespace
            Contains the command line arguments
        """

        self.commandline_arguments = commandline_arguments

        self.logging_handler = LoggingHandler(
            logger=logger,
            logging_functions=[self.log_console]
        )
        self.application_settings = application_settings

        provider = Gtk.CssProvider()
        provider.load_from_path("user_interface/gtk/forms/style.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

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

        self.console_buffer = self.builder.get_object("console_text_view").get_buffer()

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

    def get_confirmation_from_dialog(self, message: str) -> bool:
        message_dialog = Gtk.MessageDialog(
            parent= self.builder.get_object("main"),
            flags= Gtk.DialogFlags.DESTROY_WITH_PARENT,
            type= Gtk.MessageType.QUESTION,
            buttons= Gtk.ButtonsType.YES_NO,
            message_format= message
        )
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_DIALOG_QUESTION, Gtk.IconSize.DIALOG)
        image.show()
        message_dialog.set_image(image)
        user_response = message_dialog.run()
        message_dialog.destroy()
        return user_response == Gtk.ResponseType.YES

    def launch_third_party_utility(
        self,
        package_name: str,
        executable_name: str
    ):
        package_lookup_command = Command(
            [
                "pacman",
                "-Q",
                package_name
            ]
        )
        output = package_lookup_command.run_and_wait()
        output = output.strip()
        package_lookup_return_code = package_lookup_command.return_code
        LogMessage.Debug("Package lookup command output: " + output).write(logging_handler=self.logging_handler)
        LogMessage.Debug("Package lookup command return code: " + str(package_lookup_return_code)).write(logging_handler=self.logging_handler)

        if package_lookup_return_code == 0:
            LogMessage.Info("Launching `" + executable_name + "`...").write(logging_handler=self.logging_handler)
            command = Command([executable_name])
            # command.run_and_log(self.logging_handler)
            command.start()
        else:
            LogMessage.Warning("Could not find `" + package_name + "` on your system...").write(self.logging_handler)
            if not self.get_confirmation_from_dialog("`" + package_name + "` is not installed. Do you want to install it?"):
                LogMessage.Info("User declined to install `" + package_name + "`. Doing nothing...").write(self.logging_handler)
                return
            batch_job = BatchJob(logging_handler= self.logging_handler)
            batch_job += LogMessage.Info("Trying to install `" + package_name + "`...")
            batch_job += Command.Shell(
                "pkexec bash -c \"sudo pacman -S --needed --noconfirm " + package_name + "\""
            )
            batch_job += LogMessage.Info("Launching `" + executable_name + "`...")
            batch_job += Command(
                [
                    executable_name
                ]
            )
            batch_job.start()

    def log_console(
        self,
        logging_level: int,
        message: str,
        *args,
        loginfo_filename= "",
        loginfo_line_number= -1,
        loginfo_function_name= "",
        loginfo_stack_info= None,
        **kwargs
    ):
        logging_level_name = LoggingLevel(logging_level).name

        # Needed because Gtk doesn't prefer adding stuff on a different thread
        GLib.idle_add(
            lambda: ( # A temporary nameless function handle to make sure that console_buffer.get_end_iter() is valid by calling it right when the insert() method is called. They are both grouped together. Using GLib.idle_add directly was somehow invalidating get_end_iter(), resulting in runtime errors, which are now fixed
                self.console_buffer.insert_markup(
                    self.console_buffer.get_end_iter(),
                    "".join(
                        (
                            "- ",
                            "<span color=\"{:s}\">",
                            logging_level_name.rjust(8, " "),
                            ": ",
                            "</span>"
                        )
                    ).format(self.log_color[logging_level_name]),
                    -1
                )
            )
        ) 
        # Needed because Gtk doesn't prefer adding stuff on a different thread
        GLib.idle_add(
            lambda: ( # A temporary nameless function handle to make sure that console_buffer.get_end_iter() is valid by calling it right when the insert() method is called. They are both grouped together. Using GLib.idle_add directly was somehow invalidating get_end_iter(), resulting in runtime errors, which are now fixed
                self.console_buffer.insert(
                    self.console_buffer.get_end_iter(),
                    "".join(
                        (
                            message,
                            # "(", loginfo_filename, " > ", loginfo_function_name, "; ", "Line ", str(loginfo_line_number), ")"
                            "\n"
                        )
                    )
                )
            )
        )    

    # def on_refresh_pacman_mirrors(self, _):
    #     LogMessage.Info("Refreshing pacman mirrors...").write(self.logging_handler)
    #     command = Command(
    #         command_strings= [
    #             "pkexec",
    #             "sudo",
    #             "reflector",
    #             "--latest", "50",
    #             "--protocol", "https",
    #             "--sort", "rate",
    #             "--save", "/etc/pacman.d/mirrorlist",
    #         ],
    #         post_run_function= functools.partial(
    #             LogMessage.Info("Reflector finished... Please check the above messages for errors").write,
    #             self.logging_handler
    #         )
    #     )
    #     command.run_and_log(self.logging_handler)

    def on_main_message_resized(self, label, size):
        # A hack needed to wrap text dynamically, instead of Gtk making the window wide to accomodate it
        label.set_size_request(size.width -1, -1)

    def on_close(self, _):

        """
        Quit the graphical interface

        Called when the application is closedMainFormHandler
        """

        if self.commandline_arguments.iso:
            command = Command.Shell("pkexec bash -c \"sudo cnchi-start.sh\"")
            command.run_and_log(logging_handler=self.logging_handler)

        LogMessage.Info("User closed the application. Exiting...").write(self.logging_handler)
        # self.logging_handler.abort(wait=False)
        Gtk.main_quit() # Quit from the Gtk UI
        # exit(0)

    def console_expander_activated(self, expander):
        console_pane = self.builder.get_object("console_pane")
        height = self.builder.get_object("console_pane").get_allocated_height()
        if not expander.get_expanded():            
            console_pane.set_position(height-80)
        else:
            console_pane.set_position(height)

    def on_console_pane_resized(self, console_pane):
        pass
        # print("console_pane position: ", console_pane.get_position())
        # console_expander = self.builder.get_object("console_expander")
        # if console_pane.get_position() < 349:
        #     if not console_expander.get_expanded():
        #         self.builder.get_object("console_expander").set_expanded(True)
        # else:
        #     if console_expander.get_expanded():
        #         self.builder.get_object("console_expander").set_expanded(False)

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

    def on_pamac(self, _):
        self.launch_third_party_utility(
            package_name= "pamac-aur",
            executable_name = "pamac-manager"
        )  

    def on_stacer(self, _):
        self.launch_third_party_utility(
            package_name= "stacer",
            executable_name = "stacer"
        )  

    def on_hardinfo(self, _):
        self.launch_third_party_utility(
            package_name= "hardinfo",
            executable_name = "hardinfo"
        ) 

    def on_baobab(self, _):
        self.launch_third_party_utility(
            package_name= "baobab",
            executable_name = "baobab"
        ) 

    def on_bleachbit(self, _): 
        self.launch_third_party_utility(
            package_name= "bleachbit",
            executable_name = "bleachbit"
        ) 

    def on_reflector_simple(self, _):
        self.launch_third_party_utility(
            package_name= "reflector-simple",
            executable_name = "reflector-simple"
        ) 

    def on_pace(self, _): 
        self.launch_third_party_utility(
            package_name= "pace",
            executable_name = "pace"
        ) 

    def on_grub_customizer(self, _): 
        self.launch_third_party_utility(
            package_name= "grub-customizer",
            executable_name = "grub-customizer"
        ) 

    def on_gparted(self, _): 
        self.launch_third_party_utility(
            package_name= "gparted",
            executable_name = "gparted"
        ) 

    def on_pyakm(self, _): 
        self.launch_third_party_utility(
            package_name= "pyakm",
            executable_name = "pyakm-manager"
        )  

    def on_timeshift(self, _): 
        self.launch_third_party_utility(
            package_name= "timeshift",
            executable_name = "timeshift-launcher"
        )    
  