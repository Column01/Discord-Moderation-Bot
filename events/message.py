import inspect
import sys

from events.base import EventHandler


class MessageEvent(EventHandler):
    def __init__(self, client_instance):
        self.client = client_instance
        self.event = "on_message"
    
    async def handle(self, *args, **kwargs):
        # Get the message from the args
        message = args[0]

        # Get the user from the message
        user = message.author
        # Ignore messages from bots or if the message has no text.
        if user.bot or not message.content:
            return
        command = message.content.split()
        # Grab the base command from the message. This leaves "command" with the command arguments afterwards
        cmd = command.pop(0)
        if cmd.startswith(self.client.prefix):
            # Cut the prefix off the command
            cmd = cmd[self.client.prefix_length:]
            # Get the command handler and execute it
            command_handler = self.client.registry.get_command(cmd)
            if command_handler is not None:
                await command_handler(self.client).execute(message, command=cmd, args=command, storage=self.client.storage, instance=self.client)
            else:
                await message.channel.send("**Unknown command:** {}".format(cmd))


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
