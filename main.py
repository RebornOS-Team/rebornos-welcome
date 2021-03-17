#! /usr/bin/env python

# Fenix Installer
# Please refer to the file `LICENSE` in the main directory for license information. 
# For a high level documentation, please visit https://gitlab.com/rebornos-team/fenix/fenix-installer

# AUTHORS
# 1. Shivanand Pattanshetti (shivanand.pattanshetti@gmail.com)
# 2. 

# This is the Python entry point of the installer

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

# FENIX IMPORTS
from fenix_library.configuration import JSONConfiguration # For reading and writing settings files

class FenixInstaller():
    """
    An internal-use class to encapsulate the tasks associated with setting up Fenix installer

    """

    def __init__(self) -> None:
        """
        The main function.

        The following tasks are accomplished:
        - Configure logging
        - Set the current working directory,
        - Define and parse command line options
        - Start the installer based on command line options

        Parameters
        ----------
        None

        Returns
        -------
        Nothing
        """ 

        self.logger = self.setup_logger() # configure the logger. The resulting logger is assigned to nothing (underscore)
        self.installer_settings = JSONConfiguration("configuration/installer.json") # to access the settings stored in 'installer.json'
        self.set_current_working_directory() # set the base directory of the installer as the current working directory       
        commandline_arguments = self.handle_arguments() # handle command line arguments
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

        print("Fenix installer - RebornOS\n")

        self.delete_old_log_files(no_of_files_to_keep =5) # delete old log files

        logger = logging.getLogger('main.py') # create a new logger and name it
        logger.setLevel(logging.DEBUG) # set it to log anything of debugging and higher alert levels
        
        # Set up file-based logging
        log_file_path = pathlib.Path("log/" + "installer-" + FenixInstaller.get_time_stamp() + ".log")
        print("Writing the log file " + str(log_file_path) + "...\n\n")
        log_file_handler = logging.FileHandler(log_file_path) # for logging onto files
        log_file_handler.setLevel(logging.DEBUG) # log debug messages and higher
        # log_file_formatter = logging.Formatter('[%(asctime)s, %(levelname)-8s, %(name)s] %(message)s', '%Y-%m-%d, %H:%M:%S %Z') # old format of each log file entry
        log_file_formatter = logging.Formatter('[%(asctime)s, %(levelname)-8s] %(message)s', '%Y-%m-%d, %H:%M:%S %Z') # format of each log file entry
        log_file_handler.setFormatter(log_file_formatter)
        logger.addHandler(log_file_handler)

        # Set up standard console logging
        log_error_handler = logging.StreamHandler() # for logging onto the console
        log_error_handler.setLevel(logging.WARNING) # log warning messages and higher alert levels   
        log_error_formatter = logging.Formatter('[%(levelname)8s!] %(message)s') # format of each console log entry    
        log_error_handler.setFormatter(log_error_formatter)    
        logger.addHandler(log_error_handler)

        return logger

    @staticmethod
    def delete_old_log_files(no_of_files_to_keep: int) -> None:
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
            "ls -tp installer* | grep -v '/$' | tail -n +" 
                + str(no_of_files_to_keep + 1) 
                + " | xargs -I {} rm -- {}",
            shell=True,
            cwd=pathlib.Path("./log/")
        )

    @staticmethod
    def set_current_working_directory(installer_settings: JSONConfiguration) -> None: 
        """
        Set the current working directory
        
        The following tasks are accomplished
        - Set the current working directory of this script to the directory in which this file exists (i.e. the base directory of the installer)
        - Store the directory information in a configuration 
        
        Parameters
        ----------
        installer_settings: JSONConfiguration
            The JSONConfiguration object that points to the settings file which stores the current working directory

        Returns
        -------
        Nothing 
        """

        os.chdir( # change the current working directory to
            os.path.dirname( # get the directory's name for the file
                os.path.realpath( # get the full path of
                    __file__ # the current file
                )
            )
        )

        installer_settings["current_working_directory"] = os.getcwd() # Store the current working directory
        installer_settings.write_data() # write pending changes to the configuration file
    
    @staticmethod
    def handle_arguments(installer_settings: JSONConfiguration) -> Namespace:
        """
        Define and parse command line options

        Parameters
        ----------
        installer_settings: JSONConfiguration
            The JSONConfiguration object that points to the installer settings file

        Returns
        -------
        parsed_args: TypedDict
            The parsed arguments
        """

        argument_parser = argparse.ArgumentParser(description= 'Run Fenix Installer.') # define a parser for command line arguments

        argument_parser.add_argument( # define a command line argument for selecting UI toolkits
            '-ui', '--user_interface',
            choices= installer_settings.get_available_choices_for_item("ui-toolkits"),
            default= installer_settings.get_default_choice_for_item("ui-toolkits"),
            help= "specify the UI toolkit."
        )
        argument_parser.add_argument( # define a command line argument for selecting the installation mode
            '-m', '--mode',
            choices= installer_settings.get_available_choices_for_item("modes"),
            default= installer_settings.get_current_choice_for_item("modes"),
            help= "specify the mode of installation."
        )

        parsed_args = argument_parser.parse_args()
        if not parsed_args.mode == installer_settings.get_current_choice_for_item("modes"):
            installer_settings.set_current_choice_for_item("modes", parsed_args.mode)
            installer_settings.write_data()

        return parsed_args

    @staticmethod
    def load_UI(commandline_arguments: Namespace) -> None:
        """
        Loads the appropriate UI.
        
        Loads the appropriate UI based on the UI toolkit name passed as an argument to the program, if any. 
        The code for launching the UI is assumed to reside in a class called "Main" in user_interface/<ui_toolkit>/code/main.py

        commandline_arguments: TypedDict
            Command-line arguments parsed using the argparse parse_args() method
        """

        installer_mode = commandline_arguments.mode # Extract the mode option (defined in the method 'handle_arguments')

        page_settings = JSONConfiguration("configuration/pages.json") # to access installer page configuration data
        page_settings["added_pages"] = page_settings["mode_templates"][installer_mode]
        page_settings.write_data() # write all changes to the configuration file (configuration/pages.json)
        
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
        
        _ = ui_module.Main(commandline_arguments) # initialize the Main class of the main script for the chosen user interface toolkit

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
    FenixInstaller.Main()