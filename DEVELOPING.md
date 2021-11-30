# How to add custom commands and event handlers

## Table of Contents

- [Custom Commands](#custom-commands)
  - [Keyword Arguments](#available-keyword-arguments-for-command-handlers)
  - [Command Template](#command-template)
- [Custom Event Handler](#custom-event-handlers)
  - [Event Handler Template](#event-handler-template)

## Custom Commands

Custom commands are added by placing python scripts in the `commands` directory.

### Available keyword arguments for command handlers

Obtain each using `my_var = kwargs.get("key")` where `key` is an option from below

- `command`
  - The name of the command. In the example above, this would just be `test`
- `args`
  - A list of arguments following the `command`. This can be any length so ensure your code has proper checking for argument lengths and stuff
- `storage`
  - An instance of the storage handler class. Really should only be used if you know what you are doing! See `storage_management.py` for the code of that class.
- `instance`
  - An instance of the bot, should REALLY not be used but is available if absolutely needed

### Command template

All you should need to edit is `self.cmd` variable to be the start of the command (`!test` would be `self.cmd = "test"`). You can also define command aliases by making `self.cmd` a list of strings like this: `self.cmd = ["test", "test2"]`.

Once you have that you need to edit the code inside the `execute` function. In the template below there are some examples of additional information about commands as well as info on what you can get from the `kwargs` or `Key word arguments` that the bot fills. The `execute` function is run to execute your command, and is where you would reply to the user or do stuff with the command.

```py
import inspect
import sys

from commands.base import Command
""" DO NOT TOUCH ABOVE THIS LINE """
# Custom modules are allowed to be imported
from my_module import MyClass


class TemplateCommand(Command):
    def __init__(self, client_instance):
        # Change this variable to the command name you want the command to use. CaSe SeNsItIvE!
        self.cmd = "mycommandname"
        # You can also define multiple command names or aliases like this:
        self.cmd = ["mycommandname", "mcn"]
        # This is a reference to the main bot class. Allows for arbitrary access in case your command needs something specific that cannot be obtained from the kwargs. Really not recommended that you mess with this unless you know what you are doing!
        self.client = client_instance

    async def execute(self, message, **kwargs):
        """ The code here that will run when the command is recieved """
        # The command that was run
        cmd = kwargs.get("command")
        # Example of getting the command arguments (everything that follows "!cmd")
        cmd_args = kwargs.get("args")
        # Obtain access to the storage mangement class. Allows for adding custom user data storage. USE AT YOUR OWN RISK!
        storage = kwargs.get("storage")
        # Get a reference to the bot instance. This isn't strictly nessecary as the client instance is stored above in self.client, but is here for backwards compatibility.
        client = kwargs.get("instance")


        # Example sending a message to the channel. Other than the data you can obtain from the kwargs and message, you have FULL access to the discord.py api here.
        await message.channel.send(f"{message.author} executed the command: {cmd} with arguments {cmd_args}")


""" DO NOT TOUCH BELOW THIS LINE """
# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)

```

## Custom Event Handlers

Custom event handlers are added by placing python scripts in the `events` directory. Custom event handlers can handle any event from the events discord.py sends. See the [discord.py event reference](https://discordpy.readthedocs.io/en/stable/api.html#event-reference) for a list of events you can use.

### Event Handler Template

Again, you should only need to modify the event you want to listen to in `self.event`, and the code inside of the `handle` function. Unlike the commands, there are no keyword arguments provided by the bot. All `args` and `kwargs` are filled by `discord.py` when the event is fired. See the [discord.py](https://discordpy.readthedocs.io/en/stable/api.html) documentation for your event to see what you can get from the event.

```py
import inspect
import sys

from events.base import EventHandler
""" DO NOT TOUCH ABOVE THIS LINE """
# Custom modules are allowed to be imported
from my_module import MyClass

class OnMessageEvent(EventHandler):
    def __init__(self, client_instance):
        self.client = client_instance
        self.event = "on_message"
    
    async def handle(self, *args, **kwargs):
        # Args is a list of all arguments sent by discord.py in the event. 
        # If you want to obtain info from the event, you must grab it by it's index. 
        # The event documentation from discord.py will show you what is passed with the event and it will be in that order from the list. 
        # Advanced users can also replace "args" with the arguments from the event. (in this example, remove *args and use message in its place)
        message = args[0]
        await message.channel.send("Message recieved!")


""" DO NOT TOUCH BELOW THIS LINE """
# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)

```

## Custom Storage File

The bot has provisions for custom storage files. This allows you to store customized values in a separate file from the main one so that you don't accidentally mess stuff up.

### Initializing a custom config

In order to use a custom storage file, you must add a reference to it in the main bot script. To do so, edit `bot.py` and go to the main `__init__` function.

In that function, you may see a commented out section that looks like the following:

```python
# from storage_management import ConfigManagement
# self.config = ConfigManagement()
```

Un-commenting this will load a generic `ConfigManagement` class I've added as an example. You can edit this class inside `storage_management.py`.

Once you uncomment that, you will also need to run it's `init` function, currently there is a call to do this in the `events/ready.py` event handler once the class is enabled in the main bot script. If you want, you can create your own custom config class in that same file, but you will need to import it and initialize it as needed following the same method used with the example here (import it, add a class variable to `bot.py` and call the `init` function inside the ready event)

### Referencing values from your custom config

In order to get data from your custom config elsewhere, you need to obtain it's reference from the client instance. Following the command and event templates from above, you would do so like this:

```python
# Get config management class reference (only works if you have a reference to the client instance stored in "self.client_instance")
config = self.client_instance.config

# Get some value from config (loads contents from disk)
config_value = await config.get_value("some_key")
if config_value is not None:
    print(config_value)
else:
    print("Value not found in config file!")

# If you want to get values but do it in a way where it doesn't overwrite changes in the stored class values
# Use the "load_local" function to get a local reference

local_settings = await config.load_local()

# Sets and saves some value to disk
await config.set_value("some_key", "some_value")

# you should set values explicitly using the "settings" class variable of your custom config if you want to set more than one value
config.settings["some_key"] = "some_value"
# It can store list and sub objects too. Follow typical JSON structure!
config.settings["some_key2"] = ["some_value1", "some_value2"]
# Saves the settings after all your changes
await config.write_file_to_disk()

```

### Custom Config Template

Here is a template of the config handler class used in this example, you can rename it and add the required code (covered above) to initialize it.

**Make sure to substitute the new name of the class!**

```python
class ConfigManagement(JsonFileManager):
    """ Example custom config class to handle non guild-specific settings for customized features of the bot """
    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.file_path = os.path.join(__location__, "custom_config.json")
        self.settings = None

    async def create_file(self):
        self.settings = {
            "some_key": "some_value"
        }
        await self.write_file_to_disk()

    async def get_value(self, some_key):
        """ Example function loading a key from the config file """
        await self.load()
        return self.settings.get(some_key)

    async def set_value(self, some_key, some_value):
        """ Example function setting a value to the config file and saving it to disk """
        self.settings[some_key] = some_value
        await self.write_file_to_disk()

```
