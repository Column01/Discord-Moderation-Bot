import importlib
import os
import sys
from typing import Optional

from bot import ModerationBot
from commands.base import Command


class CommandRegistry:
    """ Command registry class that handles dyanmic class loading and getting info for a command """
    commands = {}
    py_files = []
    new_py_files = []
    modules = []
    module_changes = False

    def __init__(self) -> None:
        print("Initializing the command registry handler. This does not start registering commands!")
        self.get_py_files(overwrite=True)

    def set_instance(self, instance: ModerationBot) -> None:
        """ Gives the command registry and instance of the bot """
        self.instance = instance

    def register(self, cmd: str, instance: ModerationBot) -> None:
        """ Method that registers command modules """
        if cmd not in self.commands:
            self.commands[cmd] = instance
        else:
            print("Command Instance already present: " + cmd)

    def unregister(self, cmd: str) -> None:
        """ Method to unregister a command module by name """
        try:
            self.commands.pop(cmd)
        except KeyError:
            pass

    def get_command_names(self) -> list:
        """ Gets all the command names """
        return [cmd for cmd, _ in self.commands.items()]

    def get_py_files(self, overwrite: Optional[bool] = False) -> None:
        """Gets a list of python files in the commands directory, used when reloading
        Args:
            overwrite (bool, optional): Whether to overwrite the py_files class variable. Used for when scripts are being loaded initially. Defaults to False.
        """
        # Import the script location and load all .py files from the commands directory
        from bot import __location__

        # Collects file names for all files in the commands directory that end in .py
        new_py_files = [py_file for py_file in os.listdir(os.path.join(__location__, "commands")) if os.path.splitext(py_file)[1] == ".py"]
        if len(new_py_files) != self.py_files:
            self.new_py_files = new_py_files
            self.module_changes = True
            # Overwrite the py_files list if the overwrite flag is set
            if overwrite:
                self.py_files = new_py_files

    def register_commands(self) -> None:
        """ Registers all commands with the bot """
        print("Registering commands...")
        # Clear commands storage
        self.commands.clear()
        # Unload all command modules
        self.modules = [str(m) for m in sys.modules if m.startswith("commands.")]
        for module in self.modules:
            if "base" not in module:
                del sys.modules[module]

        # Get all modules in all command folder, import them and register all commands inside of them
        for command_file in self.py_files:
            fname = os.path.splitext(command_file)[0]
            # Ignore the base command file
            if fname == "base":
                continue
            command_module = importlib.import_module("commands.{}".format(fname))
            classes = dict(command_module.classes)
            for name, class_info in classes.items():
                # Check if the command class is a subclass of the base command
                if issubclass(class_info, Command):
                    clazz = class_info(self.instance)
                    clazz.register_self()
                else:
                    print("Command class: {} in file: {} is not a subclass of the base command class. Please fix this (see repository for details)!".format(name, command_file))

    async def reload_commands(self) -> None:
        """ Gets the changed python files list and reloads the commands if there are changes """
        self.get_py_files()
        if self.module_changes:
            self.module_changes = False
            self.py_files = self.new_py_files
            self.register_commands()

    def get_command(self, cmd) -> Command:
        """Get a command by it's name
        Args:
            cmd (str): The name of the command to get
        Returns:
            class: A reference to the command's class to initialize and execute the command
        """
        return self.commands.get(cmd)


registry = CommandRegistry()
