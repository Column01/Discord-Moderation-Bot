import importlib
import os
import sys
import functools
import asyncio

from events.base import EventHandler


class EventRegistry:
    """ Event registry class that handles dyanmic class loading and getting info for an event handler """

    def __init__(self):
        self.event_handlers = {}
        self.py_files = []
        self.new_py_files = []
        self.modules = []
        self.module_changes = False
        print("Initializing the event registry handler. This does not start registering events!")
        self.get_py_files(overwrite=True)
    
    def set_instance(self, instance):
        """ Gives the event registry and instance of the bot """
        self.instance = instance

    def register(self, event, instance):
        """ Method that registers event modules """
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        if instance not in self.event_handlers[event]:
            self.event_handlers[event].append(instance)
        else:
            print("Event Instance already present: " + instance)

    def unregister(self, event, instance):
        """ Method to unregister an event module by name """
        try:
            self.event_handlers[event].remove(instance)
            # No more event handlers are registered for the event, remove it from the list and delete the event method from the bot
            if len(self.event_handlers[event]) == 0:
                self.event_handlers.pop(event)
                delattr(self.instance, event)
        except KeyError:
            pass

    def get_py_files(self, overwrite=False):
        """Gets a list of python files in the events directory, used when reloading
        Args:
            overwrite (bool, optional): Whether to overwrite the py_files class variable. Used for when scripts are being loaded initially. Defaults to False.
        """
        # Import the script location and load all .py files from the events directory
        from bot import __location__

        # Collects file names for all files in the events directory that end in .py
        new_py_files = [py_file for py_file in os.listdir(os.path.join(__location__, "events")) if os.path.splitext(py_file)[1] == ".py"]
        if len(new_py_files) != self.py_files:
            self.new_py_files = new_py_files
            self.module_changes = True
            # Overwrite the py_files list if the overwrite flag is set
            if overwrite:
                self.py_files = new_py_files

    def register_events(self):
        """ Registers all events with the bot """
        print("Registering events...")
        # Clear events storage
        self.event_handlers.clear()
        # Unload all event modules
        self.modules = [str(m) for m in sys.modules if m.startswith("events.")]
        for module in self.modules:
            del sys.modules[module]

        # Get all modules in all events folder, import them and register all events inside of them
        for event_file in self.py_files:
            fname = os.path.splitext(event_file)[0]
            # Ignore the base event file
            if fname == "base":
                continue
            event_module = importlib.import_module("events.{}".format(fname))
            classes = event_module.classes
            for class_info in classes:
                clazz = class_info[1](self.instance)
                # Check if the event handler class is an instance of the base event handler
                if isinstance(type(clazz), type(EventHandler)):
                    clazz.register_self()
                    event_name = clazz.event
                    if event_name is not None:
                        if not hasattr(self.instance, event_name):
                            setattr(self.instance, event_name, asyncio.coroutine(functools.partial(self.instance.event_template, event_name=event_name)))
                    else:
                        print("Event handler has no event name configured! This is an error and the event will not fire!")
                        clazz.unregister_self()
                    del clazz
                else:
                    print("Event handler class in file: {} is not a subclass of the base event handler class. Please fix this (see repository for details)!".format(fname))

    async def reload_events(self):
        """ Gets the changed python files list and reloads the events if there are changes """
        self.get_py_files()
        if self.module_changes:
            self.module_changes = False
            self.py_files = self.new_py_files
            self.register_events()
        
    def get_all_event_handlers(self):
        return self.event_handlers.keys()

    def get_event_handlers(self, event):
        try:
            return self.event_handlers[event]
        except KeyError:
            print("No event handlers registered for event.")


event_registry = EventRegistry()
