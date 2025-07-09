# RebornOS Welcome
# Please refer to the file `LICENSE` in the main directory for license information. 
# For a high level documentation, please visit https://github.com/RebornOS-Team/rebornos-welcome

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2. 

# IMPORTS
import os # for filepath related methods
import gi # Python GObject introspection module which contains Python bindings and support for Gtk
gi.require_version('Gtk', '3.0') # make sure that the Gtk version is at the required level
from gi.repository import Gtk, GLib, GdkPixbuf, Gdk # Gtk related modules for the graphical interface
from argparse import Namespace
from typing import List, Union, Tuple, Optional, Any
from pathlib import Path
import logging
import functools
import sys

from pysetting import JSONConfiguration
from pyrunning import LoggingHandler, LogMessage, Command, LoggingLevel, BatchJob, Function

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
        self.is_iso = False
        self.initialized = False
        self.expander_deactivate_clicked = False
        self.expander_previous_height=-1

        self.commandline_arguments = commandline_arguments

        self.logging_handler = LoggingHandler(
            logger=logger,
            logging_functions=[
                self.log_console,
                self.log_status,
            ]
        )
        self.application_settings: JSONConfiguration = application_settings

        LogMessage.Info("Loading CSS styles...").write(self.logging_handler)
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
        
        self.builder.get_object("main_window").set_title("Welcome to RebornOS!") 

        self.console_buffer = self.builder.get_object("console_text_view").get_buffer()
        self.status_label = self.builder.get_object("status_label")
        self.builder.get_object("console_text_view").modify_base(Gtk.StateFlags.NORMAL, Gdk.color_parse('black'))     

        LogMessage.Debug("Detecting if the application is enabled at startup...").write(self.logging_handler)
        if self.application_settings["auto_start_enabled"]:
            self.builder.get_object("startup_toggle").set_active(True)
        else:
            self.builder.get_object("startup_toggle").set_active(False)

        self.builder.get_object("green_light").set_visible(True)
        self.builder.get_object("red_light").set_visible(True)
        
        self.builder.get_object("show_installinfo_again").set_active(self.settings_safe_get("show_install_info", True))

        page_stack = self.builder.get_object("page_stack")

        if commandline_arguments.iso:
            self.is_iso = True
            LogMessage.Info("Running in the 'ISO' mode...").write(self.logging_handler)

            self.builder.get_object("main_window").resize(1,1) # resize the window to fit contents

            self.show_update_toggle = self.settings_safe_get("show_update_toggle", True)            
            if not self.show_update_toggle:
                self.builder.get_object("installer_update_switch_box").hide()
                LogMessage.Info("Update toggle is hidden...").write(self.logging_handler)

            self.show_git_toggle = self.settings_safe_get("show_git_toggle", True)            
            if not self.show_git_toggle:
                self.builder.get_object("git_switch_box").hide()
                LogMessage.Info("Git toggle is hidden...").write(self.logging_handler)  

            self.use_github_toggle = self.settings_safe_get("show_from_github_toggle", True)            
            if not self.use_github_toggle:
                self.builder.get_object("use_github_switch_box").hide()
                LogMessage.Info("\"from GitHub\" toggle is hidden...").write(self.logging_handler)                     

            self.installer_package_name_stub = self.settings_safe_get("installer_package_name_stub", "calamares-core")
            LogMessage.Info(f"Set to detect installer package name {self.installer_package_name_stub}...").write(self.logging_handler)
            self.installer_config_package_name_stub = self.settings_safe_get("installer_config_package_name_stub", "calamares-configuration")
            LogMessage.Info(f"Set to detect installer config package name {self.installer_config_package_name_stub}...").write(self.logging_handler)

            self.installer_github_url_stub = self.settings_safe_get("installer_github_url_stub", "rebornos-team/calamares-core")
            self.installer_config_github_url_stub = self.settings_safe_get("installer_config_github_url_stub", "rebornos-team/calamares-configuration")

            LogMessage.Info("Loading the 'Install' tab...").write(self.logging_handler)
            install_page = self.builder.get_object("install_page")
            page_stack.add_titled(
                child = install_page,
                name = "install_page",
                title = "Install"
            )

            self.builder.get_object("startup_toggle").hide()
            self.builder.get_object("startup_toggle_text").hide()

            rebornos_iso_welcome_icon_path = "media/icons/rebornos_iso_welcome_logo.svg"
            self.builder.get_object("main_window").set_icon_from_file(rebornos_iso_welcome_icon_path)
            about_dialog = self.builder.get_object("about")
            about_dialog.set_icon_from_file(rebornos_iso_welcome_icon_path)
            about_dialog.set_title("About RebornOS ISO Welcome Application")

            self.builder.get_object("internet_check").set_active(self.settings_safe_get("internet_check_toggled", True))
            self.builder.get_object("memory_check").set_active(self.settings_safe_get("memory_check_toggled", True))
            self.builder.get_object("storage_check").set_active(self.settings_safe_get("storage_check_toggled", True))
            self.builder.get_object("isp_dns_radio_button").set_active(self.settings_safe_get("isp_dns_toggled", True))
            self.builder.get_object("cloudflare_dns_radio_button").set_active(self.settings_safe_get("cloudflare_dns_toggled", False))
            self.builder.get_object("google_dns_radio_button").set_active(self.settings_safe_get("google_dns_toggled", False))

            self.builder.get_object("about_application_name").set_label("RebornOS ISO Welcome Application")
            self.builder.get_object("about_logo").set_from_file(rebornos_iso_welcome_icon_path)
        else:            
            self.builder.get_object("about").set_title("About RebornOS Welcome Application")

        LogMessage.Info("Loading the 'Links' tab...").write(self.logging_handler)
        links_page = self.builder.get_object("links_page")
        page_stack.add_titled(
            child = links_page,
            name = "links_page",
            title = "Links"
        )

        LogMessage.Info("Loading the 'Utilities' tab...").write(self.logging_handler)
        utilities_page = self.builder.get_object("utilities_page")        
        page_stack.add_titled(
            child = utilities_page,
            name = "utilities_page",
            title = "Utilities"
        )

        LogMessage.Info("Displaying the main window...").write(self.logging_handler)
        self.builder.get_object("main_window").resize(1,1) # resize the window to fit contents
        self.builder.get_object("main_window").show() # get the main form object and make it visible 

        self.initialized = True 

        LogMessage.Info("Starting the event loop...").write(self.logging_handler)
        Gtk.main() # start the GUI event loop

    def settings_safe_get(self, key: str, default_value: Any) -> Any :
        try:
            return self.application_settings[key]
        except KeyError as _:
            self.application_settings[key] = default_value
            self.application_settings.write_data()
            return default_value

    def get_confirmation_from_dialog(self, message: str) -> bool:
        message_dialog = Gtk.MessageDialog(
            parent= self.builder.get_object("main_window"),
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

    def is_any_package_missing(
        self,
        package_name: Union[str, List[str]]
    ):
        package_lookup_command = None
        if type(package_name) == str: 
            package_lookup_command = Command(
                [
                    "pacman",
                    "-Q",
                    package_name
                ]
            )           
        elif type(package_name) == list:
            package_lookup_command = Command(
                [
                    "pacman",
                    "-Q",
                    *package_name
                ]
            )   
        LogMessage.Debug("Checking if missing: " + str(package_name)).write(logging_handler=self.logging_handler)
        if package_lookup_command is not None: 
            output = package_lookup_command.run_and_wait()
            output = output.strip()
            package_lookup_return_code = package_lookup_command.return_code
            LogMessage.Debug("Package lookup command output: " + output).write(logging_handler=self.logging_handler)
            LogMessage.Debug("Package lookup command return code: " + str(package_lookup_return_code)).write(logging_handler=self.logging_handler)
            if package_lookup_return_code == 0:
                LogMessage.Info("Package(s) found installed: " + str(package_name)).write(logging_handler=self.logging_handler)
                return False
            else:
                LogMessage.Debug("Package(s) not found installed: " + str(package_name)).write(logging_handler=self.logging_handler)
                return True
        else:
            LogMessage.Warning("Wrong package_name format: " + str(package_name)).write(logging_handler=self.logging_handler)
            return True

    def run_executable(
        self,
        executable_name: Union[str, List[str]],
        detached: bool = False,
        batch_job: BatchJob | None = None
    ) -> Optional[BatchJob]:
        import subprocess
        import shlex

        executable_name_joined: str = ""
        if type(executable_name) == list:
            executable_name_joined = ' '.join(executable_name)
        elif type(executable_name) == str:
            executable_name_joined = str(executable_name)
        else:
            executable_name_joined = str(executable_name)

        launch_message = LogMessage.Info("Launching `" + executable_name_joined + "`...")

        run_entity: Command | Function | None = None
        if detached:
            run_entity = Function(
                subprocess.Popen,
                shlex.split(executable_name_joined),
                start_new_session=True
            )
        else:
            run_entity =  Command(
                shlex.split(executable_name_joined)
            )

        if batch_job is None:
            launch_message.write(logging_handler=self.logging_handler)
            if isinstance(run_entity, Command):
                run_entity.run_log_and_wait(self.logging_handler)
            elif isinstance(run_entity, Function):
                run_entity.run_and_log(self.logging_handler)
            return None
        else:
            batch_job += launch_message
            batch_job += run_entity
            return batch_job

    def is_package_old(self, single_package_name: str) -> bool:
        version_check_command = Command.Shell(
            f"vercmp \"$(pacman -Q {single_package_name} | cut -d \' \'  -f 2)\" \"$(pacman -Ss {single_package_name} | head -n 1 | cut -d \' \'  -f 2)\""
        )
        try:
            version_check_command_output = version_check_command.run_and_wait().strip()
            if int(version_check_command_output) < 0:
                return True
            else:
                return False
        except:
            return True # For when the package is not found

    def is_new_github_package_available(self, single_package_name: str, url_stub: str) -> Tuple[bool, str, str]:
        import requests        

        local_version = Command.Shell(
            f"pacman -Q {single_package_name} | cut -d \' \'  -f 2 | cut -d \'-\'  -f 1"
        ).run_and_wait().strip()

        github_version = ""
        try:
            github_version = requests.get(f'https://api.github.com/repos/{url_stub}/releases/latest').json()["tag_name"];
        except: 
            return (False, local_version, github_version)
        if github_version[0] == 'v':
            github_version = github_version[1:].strip()
        
        version_check_command = Command.Shell(
            f"vercmp {local_version} {github_version}"
        )

        try:
            version_check_command_output = version_check_command.run_and_wait().strip()
            if int(version_check_command_output) < 0:
                return (True, local_version, github_version)
            else:
                return (False, local_version, github_version)
        except: 
            return (False, local_version, github_version)

    def filter_old_packages(
        self,
        package_names: Union[str, List[str]]
    ) -> Union[str, List[str]]:
        if type(package_names) == list:
            old_package_names = list(
                filter(self.is_package_old, package_names)
            )
            return old_package_names
        elif type(package_names) == str:
            if self.is_package_old(str(package_names)):
                return str(package_names)
            else:
                return "" 
        return []       


    def install_package(
        self,
        package_name: Union[str, List[str]],
        post_install_command: Optional[Union[str, List[str]]] = None,
        update: bool= False,
        batch_job: BatchJob | None = None,
    ) -> BatchJob | None:
        import subprocess
        import shlex

        if update:          
            LogMessage.Debug("Checking if newer versions exist for: " + str(package_name)).write(logging_handler=self.logging_handler)
            if self.is_iso:
                Command.Shell("pkexec rm /var/lib/pacman/db.lck").run_log_and_wait(self.logging_handler)
            Command(["pkexec", "pacman", "-Sy"]).run_log_and_wait(self.logging_handler)
            package_name = self.filter_old_packages(package_name)
            LogMessage.Debug("Package(s) which need updates: " + str(package_name)).write(logging_handler=self.logging_handler)

            package_name_joined: str = ""
            if type(package_name) == list:
                package_name_joined = ' '.join(package_name)
            elif type(package_name) == str:
                package_name_joined = str(package_name)
            else:
                package_name_joined = str(package_name)
                          
            package_name_joined = package_name_joined.strip()
            if package_name_joined == "":
                return batch_job                       

            install_message = LogMessage.Info("Trying to update: `" + str(package_name) + "`...")
            # install_command = Command.Shell(
            #     "pkexec bash -c \"pacman -S --needed --noconfirm " + package_name_joined + "\""
            # )
            install_command = Command(
                [
                    "pkexec",
                    "pacman",
                    "-Sy",
                    "--needed",
                    "--noconfirm" ,
                    *shlex.split(package_name_joined),
                ]
            )
        else: 
            package_name_joined: str = ""
            if type(package_name) == list:
                package_name_joined = ' '.join(package_name)
            elif type(package_name) == str:
                package_name_joined = str(package_name)
            else:
                package_name_joined = str(package_name)

            install_message = LogMessage.Info("Trying to install: `" + str(package_name) + "`...")
            # install_command = Command.Shell(
            #     "pkexec bash -c \"pacman -Sy --needed --noconfirm " + package_name_joined + "\""
            # )
            install_command = Command(
                [
                    "pkexec",
                    "pacman",
                    "-S",
                    "--needed",
                    "--noconfirm" ,
                    *shlex.split(package_name_joined),
                ]
            )

        if batch_job is None:
            install_message.write(logging_handler=self.logging_handler)
            install_command.run_log_and_wait(self.logging_handler)
            if post_install_command is not None:
                if isinstance(post_install_command, list): 
                    Command(post_install_command).run_log_and_wait(self.logging_handler)
                elif isinstance(post_install_command, str):
                    Command.Shell(post_install_command).run_log_and_wait(self.logging_handler)
            return None
        else:
            batch_job += install_message
            batch_job += install_command
            if post_install_command is not None:
                
                if isinstance(post_install_command, list): 
                    batch_job += Command(post_install_command)
                elif isinstance(post_install_command, str):
                    batch_job += Command.Shell(post_install_command)
            return batch_job

    def uninstall_package(
        self,
        package_name: Union[str, List[str]],
        batch_job: BatchJob | None = None,
    ) -> BatchJob | None:
        import subprocess
        import shlex

        package_name_joined: str = ""
        if type(package_name) == list:
            filtered_package_list = list(
                filter(
                    lambda p: not self.is_any_package_missing(p),
                    package_name
                )
            )
            if not filtered_package_list:
                return
            package_name_joined = ' '.join(filtered_package_list)
        elif type(package_name) == str:
            if self.is_any_package_missing(package_name):
                return None
            package_name_joined = str(package_name)
        else:
            package_name_joined = str(package_name)

        uninstall_message = LogMessage.Info("Trying to uninstall: `" + str(package_name) + "`...")

        # uninstall_command = Command.Shell(
        #     "pkexec bash -c \"pacman -Rdd --noconfirm " + package_name_joined + "\""
        # )
        uninstall_command = Command(
            [
                "pkexec",
                "pacman",
                "-Rdd",
                "--noconfirm" ,
                *shlex.split(package_name_joined),
            ]
        )

        if batch_job is None:
            uninstall_message.write(logging_handler=self.logging_handler)
            uninstall_command.run_log_and_wait(self.logging_handler)
            return None
        else:
            batch_job += uninstall_message
            batch_job += uninstall_command
            return batch_job            

    def launch_third_party_utility(
        self,
        package_name: Union[str, List[str]],
        executable_name: Union[str, List[str]],
        post_install_command: Optional[Union[str, List[str]]] = None,
        detached: bool = True,
        update: bool = False,
        batch_job: BatchJob | None = None,
    ) -> BatchJob | None:        
        if batch_job is None:            
            self.display_busy()
            batch_job = BatchJob(
                logging_handler= self.logging_handler,
                post_run_function=functools.partial(
                    self.display_ready
                ),
            )
        if update or self.is_any_package_missing(package_name): 
            batch_job = self.install_package(
                package_name= package_name,
                post_install_command= post_install_command,
                update= update,
                batch_job= batch_job
            )
        batch_job = self.run_executable(
            executable_name= executable_name,
            detached= detached,
            batch_job= batch_job
        )
        if batch_job is not None:
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
        message = message.strip()
        if message == "":
            return

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

        if LoggingLevel(logging_level) != LoggingLevel.DEBUG:
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
        else:
            GLib.idle_add(
                lambda: ( # A temporary nameless function handle to make sure that console_buffer.get_end_iter() is valid by calling it right when the insert() method is called. They are both grouped together. Using GLib.idle_add directly was somehow invalidating get_end_iter(), resulting in runtime errors, which are now fixed
                    self.console_buffer.insert_markup(
                        self.console_buffer.get_end_iter(),
                        "".join(
                            (
                                "<span color=\"{:s}\">",
                                GLib.markup_escape_text(message),                                
                                # "(", loginfo_filename, " > ", loginfo_function_name, "; ", "Line ", str(loginfo_line_number), ")"
                                "</span>"
                                "\n",                                
                            )
                        ).format(self.log_color[logging_level_name]),
                        -1,
                    )
                )
            )

    def log_status(
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
        message = message.strip()
        if message == "":
            return
        
        # logging_level_name = LoggingLevel(logging_level).name

        # Needed because Gtk doesn't prefer adding stuff on a different thread
        GLib.idle_add(self.status_label.set_text, message) 

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
    #         post_start_function= functools.partial(
    #             LogMessage.Info("Reflector finished... Please check the above messages for errors").write,
    #             self.logging_handler
    #         )
    #     )
    #     command.run_log_and_wait(self.logging_handler)

    def on_main_message_resized(self, label, size):
        # A hack needed to wrap text dynamically, instead of Gtk making the window wide to accomodate it
        label.set_size_request(size.width -1, -1)

    def on_close(self, _):

        """
        Quit the graphical interface

        Called when the application is closedMainFormHandler
        """

        LogMessage.Info("User closed the application. Exiting...").write(self.logging_handler)
        # self.logging_handler.abort(wait=False)
        Gtk.main_quit() # Quit from the Gtk UI
        # exit(0)

    def console_expander_activated(self, expander):
        expander = self.builder.get_object("console_expander")
        if expander.get_expanded():    
            self.expander_deactivate_clicked = True             

    def on_console_expander_resized(self, _item1, _item2):
        expander = self.builder.get_object("console_expander")   
        height = expander.get_allocated_height()

        if height == self.expander_previous_height:
            return

        if not self.expander_previous_height:
            self.expander_previous_height = -1

        if height < self.expander_previous_height and height < 105 and expander.get_expanded():
            expander.set_expanded(False)
        elif height > self.expander_previous_height and height > 20 and not expander.get_expanded() and self.expander_previous_height != -1:
            expander.set_expanded(True)
        elif height <= 20:
            self.expander_deactivate_clicked = False

        self.expander_previous_height = height

    def display_busy(self):
        green_light = self.builder.get_object("green_light")
        green_light.set_from_file("media/icons/grey.svg")
        red_light = self.builder.get_object("red_light")
        red_light.set_from_file("media/icons/red.svg")
        # self.builder.get_object("green_light").set_visible(False)
        # self.builder.get_object("red_light").set_visible(False)

    def display_ready(self):
        green_light = self.builder.get_object("green_light")
        green_light.set_from_file("media/icons/green.svg")
        red_light = self.builder.get_object("red_light")
        red_light.set_from_file("media/icons/grey.svg")
        # self.builder.get_object("green_light").set_visible(False)
        # self.builder.get_object("red_light").set_visible(False)

    def on_about_clicked(self, _):
        LogMessage.Debug("Bringing up the \"About\" dialog...").write(self.logging_handler)
        self.builder.get_object("about").show_all()

    def on_log_clicked(self, _):
        LogMessage.Debug("Opening the log on the default editor...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", self.application_settings["current_log_file_path"]],
        )

    def on_config_clicked(self, _):
        from pathlib import Path
        LogMessage.Debug("Opening the configuration file on the default editor...").write(self.logging_handler)
        user_settings_filepath = Path(self.application_settings.filepath)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = [
                "xdg-open",
                str(user_settings_filepath.resolve())
            ],
        )


    def on_about_close(self, _):
        LogMessage.Debug("Hiding the \"About\" dialog...").write(self.logging_handler)
        self.builder.get_object("about").hide()

    def on_shivanandvp_mail(self, button):
        LogMessage.Debug("Opening mailing application for shivanandvp's email...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-email", "shivanandvp@rebornos.org"],
        )

    def on_shivanandvp_git(self, button):
        LogMessage.Debug("Opening the git page for shivanandvp...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://github.com/shiva-patt-oss"],
        )

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
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://rebornos.org/"],
        )

    def on_rebornos_wiki_clicked(self, _):
        LogMessage.Debug("Opening RebornOS Wiki on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://wiki.rebornos.org"],
        )
    
    def on_arch_wiki_clicked(self, _):
        LogMessage.Debug("Opening Arch Wiki on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://wiki.archlinux.org/"],
        )

    def on_service_status_clicked(self, _):
        LogMessage.Debug("Opening Service Status page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://status.rebornos.org/"],
        )

    def on_discord_clicked(self, _):
        LogMessage.Debug("Opening the Discord Server on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://discord.gg/cU5s6MPpQH"],
        )

    def on_forum_clicked(self, _):
        LogMessage.Debug("Opening the RebornOS Forum page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://rebornos.discourse.group/"],
        )

    def on_facebook_clicked(self, _):
        LogMessage.Debug("Opening the Facebook page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://www.facebook.com/rebornos/"],
        )
    
    def on_twitter_clicked(self, _):
        LogMessage.Debug("Opening the Twitter page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://twitter.com/rebornoslinux"],
        )

    def on_feedback_clicked(self, _):
        LogMessage.Debug("Opening the Feedback page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://www.rebornos.org/contact"],
        )

    def on_donate_clicked(self, _):
        LogMessage.Debug("Opening the donation page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://rebornos.org/donate/"],
        )

    def on_project_clicked(self, _):
        LogMessage.Debug("Opening the GitHub page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://github.com/rebornos-team"],
        )

    def on_about_us_clicked(self, _):
        LogMessage.Debug("Opening the \"About us\" page on the default browser...").write(self.logging_handler)
        self.launch_third_party_utility(
            package_name= "xdg-utils",
            executable_name = ["xdg-open", "https://rebornos.org/about/"],
        )

    def on_pamac(self, _):
        self.launch_third_party_utility(
            package_name= "pamac-aur",
            executable_name = "pamac-manager",
        )  

    def on_stacer(self, _):
        self.launch_third_party_utility(
            package_name= "stacer",
            executable_name = "stacer",
        )  

    def on_hardinfo2(self, _):
        self.launch_third_party_utility(
            package_name= "hardinfo2",
            executable_name = "hardinfo2",
        ) 

    def on_baobab(self, _):
        self.launch_third_party_utility(
            package_name= "baobab",
            executable_name = "baobab",
        ) 

    def on_bleachbit(self, _): 
        self.launch_third_party_utility(
            package_name= "bleachbit",
            executable_name = "bleachbit",
        ) 

    def on_refresh_mirrors(self, _):
        self.launch_third_party_utility(
            package_name= "refresh-mirrors",
            executable_name = ["gtk-launch", "refresh-mirrors"],
        ) 

    def on_pace(self, _): 
        self.launch_third_party_utility(
            package_name= "pace",
            executable_name = "pace",
        ) 

    def on_grub_customizer(self, _): 
        self.launch_third_party_utility(
            package_name= "grub-customizer",
            executable_name = "grub-customizer",
        ) 

    def on_gparted(self, _): 
        self.launch_third_party_utility(
            package_name= "gparted",
            executable_name = "gparted",
        ) 

    def on_timeshift(self, _): 
        self.launch_third_party_utility(
            package_name= "timeshift",
            executable_name = "timeshift-launcher",
        )  

    def on_firewall(self, _): 
        self.launch_third_party_utility(
            package_name= "gufw",
            executable_name = [
                "gtk-launch",
                "gufw"
            ],
            post_install_command= [
                "pkexec",
                "systemctl",
                "enable",
                "--now",
                "ufw"
            ]
        )   

    def install_latest_installer_github_release(
        self,
        batch_job: Optional[BatchJob] = None, 
    ) -> Optional[BatchJob]:
        LogMessage.Debug(f"Checking if a newer Github package exists for `{self.installer_config_package_name_stub}`...").write(logging_handler=self.logging_handler)
        (is_new_installer_config_github_package_available, local_version, github_version) = self.is_new_github_package_available(self.installer_config_package_name_stub, self.installer_config_github_url_stub)
        import re
        local_version_parts = re.split('[._]', local_version)
        github_version_parts = re.split('[._]', github_version)
        # Ensure that a new package is assumed to exist only if there is a new patch version and not more major changes
        for (local_version_part, github_version_part) in zip(local_version_parts[:-1], github_version_parts[:-1]):
            if local_version_part != github_version_part:
                is_new_installer_config_github_package_available = False
                LogMessage.Info(f"New Github package exists for`{self.installer_config_package_name_stub}`, but has a major change, so a newer ISO is needed...").write(logging_handler=self.logging_handler)
                break

        if not is_new_installer_config_github_package_available:
            LogMessage.Debug(f"No new compatible Github package exists for`{self.installer_config_package_name_stub}`...").write(logging_handler=self.logging_handler)
        else:
            LogMessage.Info(f"New Github package exists for `{self.installer_config_package_name_stub}`...").write(logging_handler=self.logging_handler)
        
        LogMessage.Debug(f"Checking if a newer Github package exists for `{self.installer_package_name_stub}`...").write(logging_handler=self.logging_handler)
        (is_new_installer_github_package_available, local_version, github_version) = self.is_new_github_package_available(self.installer_package_name_stub, self.installer_github_url_stub)     
        import re
        local_version_parts = re.split('[._]', local_version)
        github_version_parts = re.split('[._]', github_version)
        # Ensure that a new package is assumed to exist only if there is a new patch version and not more major changes
        for (local_version_part, github_version_part) in zip(local_version_parts[:-1], github_version_parts[:-1]):
            if local_version_part != github_version_part:
                is_new_installer_github_package_available = False
                LogMessage.Info(f"New Github package exists for`{self.installer_package_name_stub}`, but has a major change, so a newer ISO is needed...").write(logging_handler=self.logging_handler)
                break

        if not is_new_installer_github_package_available:
            LogMessage.Debug(f"No new compatible Github package exists for`{self.installer_package_name_stub}`...").write(logging_handler=self.logging_handler)
        else:
            LogMessage.Info(f"New Github package exists for `{self.installer_package_name_stub}`...").write(logging_handler=self.logging_handler)

        if not is_new_installer_config_github_package_available and not is_new_installer_github_package_available:
            return None
        
        LogMessage.Info("Will download and install from GitHub...").write(self.logging_handler)
        download_path = "/tmp/downloaded_from_github"
        if batch_job is None:
            self.display_busy()
            batch_job = BatchJob(
                logging_handler= self.logging_handler,
                post_run_function=functools.partial(
                    self.display_ready
                ),
            )
        batch_job += LogMessage.Debug("Removing temporary download directory: " + download_path)
        batch_job += Command.Shell(
            "rm -rf" + " " + download_path
        )
        batch_job += LogMessage.Debug("(Re)creating temporary download directory: " + download_path)
        batch_job += Command.Shell(
            "mkdir -p" + " " + download_path
        )
        if is_new_installer_config_github_package_available:
            batch_job += LogMessage.Debug(f"Downloading `{self.installer_config_package_name_stub}` from GitHub...")
            batch_job += Command.Shell(
                "curl --silent"
                + " " + "--output" + " " + download_path + "/" + f"{self.installer_config_package_name_stub}.pkg.tar.zst"
                + " " + "--location" + " " + f"$(curl --silent \'https://api.github.com/repos/{self.installer_config_github_url_stub}/releases/latest\' | jq \'.assets[] | select(.name | endswith(\".zst\")).browser_download_url\' | grep -v debug | cat | cut -d \'\"\' -f 2)"
            )
        if is_new_installer_github_package_available:
            batch_job += LogMessage.Debug(f"Downloading `{self.installer_package_name_stub}` from GitHub...")
            batch_job += Command.Shell(
                "curl --silent"
                + " " + "--output" + " " + download_path + "/" + f"{self.installer_package_name_stub}.pkg.tar.zst"
                + " " + "--location" + " " + f"$(curl --silent \'https://api.github.com/repos/{self.installer_github_url_stub}/releases/latest\' | jq \'.assets[] | select(.name | endswith(\".zst\")).browser_download_url\' | grep -v debug | cat | cut -d \'\"\' -f 2)"
            )
        # batch_job += Command.Shell(
        #     "rm -rf" + " " + download_path + "/" + "*.md5sum"
        # )
        batch_job += LogMessage.Debug("Installing downloaded files...")
        batch_job += Command.Shell(
            "pkexec rm /var/lib/pacman/db.lck"
        )
        batch_job += Command.Shell(
            "pkexec pacman -U --noconfirm" + " " + download_path + "/" + "*.pkg.tar.*",
        )
        batch_job += LogMessage.Debug("GitHub download and install task finished...")
        return batch_job

    def on_online_installer(self, _):
        self.display_busy()
        batch_job = BatchJob(
            logging_handler= self.logging_handler,
            post_run_function=functools.partial(
                self.display_ready
            ),
        )
        if not self.builder.get_object("git_switch").get_active():    
            batch_job = self.uninstall_package(
                [
                    f"{self.installer_package_name_stub}-git",
                    f"{self.installer_config_package_name_stub}-git", 
                    f"{self.installer_package_name_stub}-local", 
                    f"{self.installer_config_package_name_stub}-local",
                ],
                batch_job= batch_job,
            )
            if self.builder.get_object("use_github_switch").get_active():
                batch_job = self.install_latest_installer_github_release(batch_job= batch_job)
            self.launch_third_party_utility(
                package_name= [f"{self.installer_config_package_name_stub}", f"{self.installer_package_name_stub}"],
                executable_name = ["gtk-launch", "calamares_online"],
                detached= True,
                update= self.builder.get_object("installer_update_switch").get_active(),
                batch_job= batch_job,
            ) 
        else:
            batch_job = self.uninstall_package(
                [
                    f"{self.installer_package_name_stub}",
                    f"{self.installer_config_package_name_stub}",
                    f"{self.installer_package_name_stub}-local", 
                    f"{self.installer_config_package_name_stub}-local",                                    
                ],
                batch_job= batch_job
            )
            self.launch_third_party_utility(
                package_name= [f"{self.installer_config_package_name_stub}-git", f"{self.installer_package_name_stub}-git"],
                executable_name = ["gtk-launch", "calamares_online"],
                detached= True,
                update= self.builder.get_object("installer_update_switch").get_active(),
                batch_job= batch_job,
            )

    def on_offline_installer(self, _):    
        self.display_busy()    
        batch_job = BatchJob(
            logging_handler= self.logging_handler,
            post_run_function=functools.partial(
                self.display_ready
            ),
        )        
        if not self.builder.get_object("git_switch").get_active(): 
            batch_job = self.uninstall_package(
                [
                    f"{self.installer_package_name_stub}-git",
                    f"{self.installer_config_package_name_stub}-git", 
                    f"{self.installer_package_name_stub}-local", 
                    f"{self.installer_config_package_name_stub}-local", 
                ],
                batch_job= batch_job
            ) 
            if self.builder.get_object("use_github_switch").get_active():
                batch_job = self.install_latest_installer_github_release(batch_job= batch_job)            
            self.launch_third_party_utility(
                package_name= [f"{self.installer_config_package_name_stub}", f"{self.installer_package_name_stub}"],
                executable_name = ["gtk-launch", "calamares_offline"],
                detached= True,
                update= self.builder.get_object("installer_update_switch").get_active(),
                batch_job= batch_job
            ) 
        else:
            batch_job = self.uninstall_package(
                [
                    f"{self.installer_package_name_stub}",
                    f"{self.installer_config_package_name_stub}",
                    f"{self.installer_package_name_stub}-local", 
                    f"{self.installer_config_package_name_stub}-local",                                  
                ],
                batch_job= batch_job
            )
            self.launch_third_party_utility(
                package_name= [f"{self.installer_config_package_name_stub}-git", f"{self.installer_package_name_stub}-git"],
                executable_name = ["gtk-launch", "calamares_offline"],
                detached= True,
                update= self.builder.get_object("installer_update_switch").get_active(),
                batch_job= batch_job
            )          

    def on_rebornos_fire(self, _):
        self.launch_third_party_utility(
            package_name= "rebornos-fire",
            executable_name = "rebornos-fire",
        ) 

    def on_utilities_page_shown(self, _):
        if self.application_settings["show_install_info"] is True:
            LogMessage.Debug("Bringing up the installation info dialog...").write(self.logging_handler)
            self.builder.get_object("show_installinfo_again").set_active(True)
            self.builder.get_object("installinfo").show_all()
        else: 
            LogMessage.Debug("Not bringing up the installation info dialog because the user disabled it...").write(self.logging_handler)

    def on_installinfo_close(self, _):
        LogMessage.Debug("Hiding the installation info dialog...").write(self.logging_handler)
        self.builder.get_object("installinfo").hide()

    def on_show_installinfo_again_toggled(self, _):
        self.application_settings["show_install_info"] = self.builder.get_object("show_installinfo_again").get_active()
        self.application_settings.write_data()
        
    def on_use_github_switch_state_set(self, state: bool, _):
        if state:
            self.builder.get_object("git_switch").set_active(False)

    def on_git_switch_state_set(self, state: bool, _):
        if state:
            self.builder.get_object("use_github_switch").set_active(False)

    def on_app_stack_switcher_button_released(self, _event, _):
        if self.is_iso:
            # While browsing the main app tabs, revert the installer page to its 
            # original state in case the advanced options tab was clicked on the
            # ISO Welcome         
            self.builder.get_object("installer_page_stack").set_visible_child_name("install_page") 

    def on_internet_check_toggled(self, _):
        if not self.initialized:
            return # Do nothing when initial values are being set based on current status
        self.display_busy()
        if self.builder.get_object("internet_check").get_active():
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "sed -i 's/# - internet/- internet/g' /etc/calamares/modules/welcomeq_online.conf" 
                + " && " + "sed -i 's/# - internet/- internet/g' /etc/calamares/modules/welcomeq_offline.conf"
            ]).run_log_and_wait(self.logging_handler)
        else:
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "sed -i 's/- internet/# - internet/g' /etc/calamares/modules/welcomeq_online.conf"
                + " && " + "sed -i 's/- internet/# - internet/g' /etc/calamares/modules/welcomeq_offline.conf" 
            ]).run_log_and_wait(self.logging_handler)
        self.application_settings["internet_check_toggled"] = self.builder.get_object("internet_check").get_active()
        self.application_settings.write_data()
        self.display_ready()

    def on_memory_check_toggled(self, _):
        if not self.initialized:
            return # Do nothing when initial values are being set based on current status        
        self.display_busy()
        if self.builder.get_object("memory_check").get_active():
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "sed -i 's/# - ram/- ram/g' /etc/calamares/modules/welcomeq_online.conf" 
                + " && " + "sed -i 's/# - ram/- ram/g' /etc/calamares/modules/welcomeq_offline.conf"
            ]).run_log_and_wait(self.logging_handler)
        else:
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "sed -i 's/- ram/# - ram/g' /etc/calamares/modules/welcomeq_online.conf"
                + " && " + "sed -i 's/- ram/# - ram/g' /etc/calamares/modules/welcomeq_offline.conf" 
            ]).run_log_and_wait(self.logging_handler)
        self.application_settings["memory_check_toggled"] = self.builder.get_object("memory_check").get_active()
        self.application_settings.write_data()
        self.display_ready()

    def on_storage_check_toggled(self, _):
        if not self.initialized:
            return # Do nothing when initial values are being set based on current status        
        self.display_busy()
        if self.builder.get_object("storage_check").get_active():
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "sed -i 's/# - storage/- storage/g' /etc/calamares/modules/welcomeq_online.conf" 
                + " && " + "sed -i 's/# - storage/- storage/g' /etc/calamares/modules/welcomeq_offline.conf"
            ]).run_log_and_wait(self.logging_handler)
        else:
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "sed -i 's/- storage/# - storage/g' /etc/calamares/modules/welcomeq_online.conf"
                + " && " + "sed -i 's/- storage/# - storage/g' /etc/calamares/modules/welcomeq_offline.conf" 
            ]).run_log_and_wait(self.logging_handler)
        self.application_settings["storage_check_toggled"] = self.builder.get_object("storage_check").get_active()            
        self.application_settings.write_data()
        self.display_ready()  

    def on_isp_dns_toggled(self, _):  
        if not self.initialized:
            return # Do nothing when initial values are being set based on current status              
        if self.builder.get_object("isp_dns_radio_button").get_active():
            self.display_busy()
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "rm -f /etc/NetworkManager/conf.d/dns-servers.conf" 
                + " && " + "rm -f /etc/systemd/resolved.conf.d/dns-servers.conf"
                + " && " + "systemctl reload-or-restart NetworkManager.service"
                + " && " + "systemctl reload-or-restart systemd-resolved.service"
            ]).run_log_and_wait(self.logging_handler) 
            self.application_settings["isp_dns_toggled"] = True
            self.application_settings["cloudflare_dns_toggled"] = False
            self.application_settings["google_dns_toggled"] = False
            self.application_settings.write_data()                    
            self.display_ready()
    
    def on_cloudflare_dns_toggled(self, _):   
        if not self.initialized:
            return # Do nothing when initial values are being set based on current status             
        if self.builder.get_object("cloudflare_dns_radio_button").get_active():
            self.display_busy()
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "cp -rf /opt/rebornos-iso-welcome/configuration/dns-servers.conf_NetworkManager_cloudflare /etc/NetworkManager/conf.d/dns-servers.conf"
                + " && " + "mkdir -p /etc/systemd/resolved.conf.d" + " && " + "cp -rf /opt/rebornos-iso-welcome/configuration/dns-servers.conf_systemd-resolved_cloudflare /etc/systemd/resolved.conf.d/dns-servers.conf"
                + " && " + "systemctl reload-or-restart NetworkManager.service"
                + " && " + "systemctl reload-or-restart systemd-resolved.service"
            ]).run_log_and_wait(self.logging_handler)  
            self.application_settings["isp_dns_toggled"] = False
            self.application_settings["cloudflare_dns_toggled"] = True
            self.application_settings["google_dns_toggled"] = False
            self.application_settings.write_data()                        
            self.display_ready() 

    def on_google_dns_toggled(self, _):  
        if not self.initialized:
            return # Do nothing when initial values are being set based on current status              
        if self.builder.get_object("google_dns_radio_button").get_active():
            self.display_busy()
            Command([
                "pkexec",
                "/bin/bash", "-c",
                "cp -rf /opt/rebornos-iso-welcome/configuration/dns-servers.conf_NetworkManager_google /etc/NetworkManager/conf.d/dns-servers.conf"
                + " && " + "mkdir -p /etc/systemd/resolved.conf.d" + " && " + "cp -rf /opt/rebornos-iso-welcome/configuration/dns-servers.conf_systemd-resolved_google /etc/systemd/resolved.conf.d/dns-servers.conf"
                + " && " + "systemctl reload-or-restart NetworkManager.service"
                + " && " + "systemctl reload-or-restart systemd-resolved.service"
            ]).run_log_and_wait(self.logging_handler)    
            self.application_settings["isp_dns_toggled"] = False
            self.application_settings["cloudflare_dns_toggled"] = False
            self.application_settings["google_dns_toggled"] = True
            self.application_settings.write_data()                      
            self.display_ready()             
