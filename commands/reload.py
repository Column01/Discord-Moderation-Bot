import inspect
import sys


class ReloadCommand:
    def __init__(self, _):
        self.cmd = "reload"

    def register_self(self):
        from command_registry import registry
        self.registry = registry
        self.registry.register(self.cmd, self.__class__)

    def unregister_self(self):
        from command_registry import registry
        registry.unregister(self.cmd)

    async def execute(self, message, **kwargs):
        from command_registry import registry
        print("Reloading command modules...")
        await registry.reload_commands()
        print("New list of commands: " + ", ".join(registry.get_command_names()))
        await message.channel.send("Reloaded commands!")


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
