import inspect
import sys
from commands.base import Command


class ReloadCommand(Command):
    def __init__(self, _):
        self.cmd = ["reload", "rl"]

    async def execute(self, message, **kwargs):
        args = kwargs.get("args")
        if args is not None and "events" in args:
            from event_registry import event_registry
            print("Reloading event handlers")
            await event_registry.reload_events()
            print("New list of registered event handlers: " + ", ".join(event_registry.get_all_event_handlers()))
            await message.channel.send("Reloaded event registry!")
        else:
            from command_registry import registry
            print("Reloading command modules...")
            await registry.reload_commands()
            print("New list of commands: " + ", ".join(registry.get_command_names()))
            await message.channel.send("Reloaded commands!")


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
