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

All you should need to edit is `self.cmd` variable to be the start of the command (`!test` would be `self.cmd = test`) as well as the code inside the `execute` function. In the execute function there are some examples of additional information you can get from the `kwargs` or `Key word arguments` that the bot fills.

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
