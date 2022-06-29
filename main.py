#! /usr/bin/env python

# RebornOS Welcome
# Please refer to the file `LICENSE` in the main directory for license information. 
# For a high level documentation, please visit https://gitlab.com/rebornos-team/applications/rebornos-welcome

# AUTHORS
# 1. shivanandvp (shivanandvp@rebornos.org)
# 2. 

# This is the Python entry point of the welcome application

# IMPORTS
from argparse import Namespace
import os
import logging
import argparse
import importlib
import datetime
import subprocess
import pathlib
from typing import Optional
from types import ModuleType
import shutil

# FENIX IMPORTS
from fenix_library.configuration import JSONConfiguration # For reading and writing settings files
from fenix_library.running import LogMessage, LoggingHandler, Command

class RebornOSWelcome():
    """
    An internal-use class to encapsulate the tasks associated with setting up the 
    RebornOS Welcome application

    """

    @staticmethod
    def _recreate_settings_file(user_settings_filepath) -> None:
            user_settings_filepath.parents[0].mkdir(parents=True, exist_ok=True)
            os.chmod(user_settings_filepath.parents[0], 0o755)
            shutil.copy2(
                pathlib.Path("configuration/settings.json"),
                user_settings_filepath
            )
            os.chmod(user_settings_filepath, 0o666)

    def __init__(self) -> None:
        """
        The main function.

        The following tasks are accomplished:
        - Configure logging
        - Set the current working directory,
        - Define and parse command line options
        - Start the application based on command line options

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """ 

        print("\nRebornOS Welcome Application")

        commandline_arguments = self.handle_arguments() # handle command line arguments

        if commandline_arguments.iso:
            user_settings_filepath = pathlib.Path.home() / ".rebornos-iso-welcome" / "configuration" / "settings.json"
        else:
            user_settings_filepath = pathlib.Path.home() / ".rebornos-welcome" / "configuration" / "settings.json"
        
        if not os.path.isfile(user_settings_filepath):
            RebornOSWelcome._recreate_settings_file(user_settings_filepath)
        try:
            self.application_settings = JSONConfiguration(
                str(user_settings_filepath.resolve())
            ) # to access the settings stored in 'settings.json'
        except Exception as error:
            import traceback
            traceback.print_exception(type(error), error, error.__traceback__)
            try:
                RebornOSWelcome._recreate_settings_file(user_settings_filepath)
                self.application_settings = JSONConfiguration(
                    str(user_settings_filepath.resolve())
                )
            except Exception as inner_error:
                traceback.print_exception(type(inner_error), inner_error, inner_error.__traceback__)

        self.logger = self.setup_logger() # configure the logger
        self.logging_handler = LoggingHandler(logger=self.logger)

        self.set_current_working_directory() # set the base directory of the welcome application as the current working directory             
        if commandline_arguments.startup:
            if not self.application_settings["auto_start_enabled"]:
                LogMessage.Info("Application not enabled to run at startup. Exiting...").write(logging_handler=self.logging_handler)
                exit(0)
        self.load_UI(commandline_arguments) # load_data the user interface

    def setup_logger(self) -> logging.Logger:
        """
        Configure the logger

        The following tasks are accomplished:
        - Create a named logger
        - Setup logging to be done onto a file and the console
        - Define the format of log entries
        - Delete old log files

        Parameters
        ----------
        None

        Returns
        -------
        logger: logging.Logger
            The logger which has been set up
        """

        logger = logging.getLogger('rebornos_welcome') # create a new logger and name it
        logger.setLevel(logging.DEBUG) # set it to log anything of debugging and higher alert levels
        logger.propagate = False
        
        log_directory_path = []
        try:
            # Set up file-based logging
            log_directory_path = pathlib.Path(
                os.path.expanduser(
                    self.application_settings["log_directory"]
                )
            )
            log_directory_path.mkdir( parents=True, exist_ok=True )
            log_file_path = log_directory_path / ("welcome_app-" + RebornOSWelcome.get_time_stamp() + ".log")
            if not os.path.isdir(log_directory_path):
                raise FileNotFoundError("The directory '" + str(log_directory_path) + "' could not be created.")
            elif not os.access(log_directory_path, os.W_OK):
                raise PermissionError("The directory '" + str(log_directory_path) + "' does not have write permissions.")
        except Exception as error:
            import traceback
            traceback.print_exception(type(error), error, error.__traceback__)
            try:
                log_directory_path = pathlib.Path(
                    os.path.expanduser(
                        "~/.rebornos-welcome/log/"
                    )
                )
                log_directory_path.mkdir( parents=True, exist_ok=True )
                log_file_path = log_directory_path / ("welcome_app-" + RebornOSWelcome.get_time_stamp() + ".log")
                if not os.path.isdir(log_directory_path):
                    raise FileNotFoundError("The directory '" + str(log_directory_path) + "' could not be created.")
                elif not os.access(log_directory_path, os.W_OK):
                    raise PermissionError("The directory '" + str(log_directory_path) + "' does not have write permissions.")
            except Exception as inner_error:
                traceback.print_exception(type(inner_error), inner_error, inner_error.__traceback__)
                exit(1)

        self.application_settings["log_directory"] = str(log_directory_path)
        self.application_settings["current_log_file_path"] = str(log_file_path)
        self.application_settings.write_data()        
        print("Logging to " + str(log_file_path.resolve()) + "...\n")        
        self.application_settings.write_data()

        self.delete_old_log_files(log_directory_path, no_of_files_to_keep =5) # delete old log files

        log_file_handler = logging.FileHandler(log_file_path) # for logging onto files
        log_file_handler.setLevel(logging.DEBUG) # log debug messages and higher
        # log_file_formatter = logging.Formatter('[%(asctime)s, %(levelname)-8s, %(name)s] %(message)s', '%Y-%m-%d, %H:%M:%S %Z') # old format of each log file entry
        log_file_formatter = logging.Formatter('%(asctime)s [%(levelname)8s] %(message)s (%(pathname)s > %(funcName)s; Line %(lineno)d)', '%Y-%m-%d %H:%M:%S %Z') # format of each log file entry
        log_file_handler.setFormatter(log_file_formatter)
        logger.addHandler(log_file_handler)

        # Set up standard console logging
        log_error_handler = logging.StreamHandler() # for logging onto the console
        log_error_handler.setLevel(logging.INFO) # log info messages and higher alert levels   
        log_error_formatter = logging.Formatter('%(levelname)8s: %(message)s') # format of each console log entry    
        log_error_handler.setFormatter(log_error_formatter)    
        logger.addHandler(log_error_handler)

        return logger

    def set_current_working_directory(self) -> None: 
        """
        Set the current working directory
        
        The following tasks are accomplished
        - Set the current working directory of this script to the directory in which this file exists (i.e. the base directory of the app)
        - Store the directory information in a configuration 
        
        Parameters
        ----------
        None

        Returns
        -------
        Nothing 
        """

        working_directory = os.path.dirname( # get the directory's name for the file
            os.path.realpath( # get the full path of
                __file__ # the current file
            )
        )
        LogMessage.Info("Changing the working directory to " + working_directory + "...").write(self.logging_handler)
        os.chdir(working_directory)

        self.application_settings["current_working_directory"] = os.getcwd() # Store the current working directory
        self.application_settings.write_data() # write pending changes to the configuration file

    def handle_arguments(self) -> Namespace:
        """
        Define and parse command line options

        Parameters
        ----------
        none

        Returns
        -------
        parsed_args: TypedDict
            The parsed arguments
        """

        argument_parser = argparse.ArgumentParser(description= 'Run the RebornOS Welcome Application.') # define a parser for command line arguments

        argument_parser.add_argument( # define a command line argument for selecting UI toolkits
            '-ui', '--user_interface',
            choices= self.application_settings.get_available_choices_for_item("ui-toolkits"),
            default= self.application_settings.get_default_choice_for_item("ui-toolkits"),
            help= "specify the UI toolkit."
        )

        argument_parser.add_argument( # define a command line argument for selecting UI toolkits
            '-s', '--startup',
            action='store_true',
            default=False,
            help= "Indicate that the application is being launched at starup"
        )

        argument_parser.add_argument( # define a command line argument for selecting UI toolkits
            '-i', '--iso',
            action='store_true',
            default=False,
            help= "Indicate that the application is being launched from an ISO"
        )

        parsed_args = argument_parser.parse_args()

        return parsed_args

    def delete_old_log_files(self, log_directory_path, no_of_files_to_keep: int) -> None:
        """
        Delete old log files while keeping the newest ones whose count is specified by "no_of_files_to_keep"
        
        Parameters
        ----------
        no_of_files_to_keep: int
            The number of newest log files to keep

        Returns
        -------
        Nothing        
        """

        subprocess.Popen(
            "ls -tp welcome_app* | grep -v '/$' | tail -n +" 
                + str(no_of_files_to_keep + 1) 
                + " | xargs -I {} rm -- {}",
            shell=True,
            cwd=log_directory_path
        )
    
    def load_UI(self, commandline_arguments: Namespace) -> None:
        """
        Loads the appropriate UI.
        
        Loads the appropriate UI based on the UI toolkit name passed as an argument to the program, if any. 
        The code for launching the UI is assumed to reside in a class called "Main" in user_interface/<ui_toolkit>/code/main.py

        commandline_arguments: TypedDict
            Command-line arguments parsed using the argparse parse_args() method
        """
   
        ui_module: ModuleType = importlib.import_module(
            ".".join(
                [
                    "user_interface",
                    commandline_arguments.user_interface,
                    "code",
                    "main"
                ]
            )
        ) # search for and import user_interface/<ui_toolkit>/code/main.py
        LogMessage.Info("Loading the user-interface: " + commandline_arguments.user_interface + "...").write(self.logging_handler)
        _ = ui_module.Main(commandline_arguments, self.application_settings) # initialize the Main class of the main script for the chosen user interface toolkit

    @staticmethod
    def get_time_stamp() -> str:
        """
        Returns the timestamp in a particular format
        Example: 2020-01-31_23_58_59_GMT

        Parameters
        ----------
        None

        Returns 
        -------
        timestamp: str
            The timestamp in a particular format. Example: 2020-01-31_23_58_59_GMT
        """

        time_stamp: str = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S_")
        time_zone: Optional[str] = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
        
        if time_zone is None:
            time_zone = ""

        return (
            time_stamp + time_zone
        )

# THE EXECUTION STARTS HERE
if __name__ == '__main__': 
    _ = RebornOSWelcome()