import inspect
import sys
from commands.base import Command
from cool_utils import Terminal

class ReloadCommand(Command):
    def __init__(self, _):
        self.cmd = "reload"

    async def execute(self, message, **kwargs):
        args = kwargs.get("args")
        if args is not None and "events" in args:
            from event_registry import event_registry
            Terminal.display("Reloading event handlers")
            await event_registry.reload_events()
            Terminal.display("New list of registered event handlers: " + ", ".join(event_registry.get_all_event_handlers()))
            await message.channel.send("Reloaded event registry!")
        else:
            from command_registry import registry
            Terminal.display("Reloading command modules...")
            await registry.reload_commands()
            Terminal.display("New list of commands: " + ", ".join(registry.get_command_names()))
            await message.channel.send("Reloaded commands!")


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
