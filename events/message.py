import inspect
import sys

import discord
from helpers.embed_builder import EmbedBuilder

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


class MessageDeleteEvent(EventHandler):
    def __init__(self, client_instance):
        self.client = client_instance
        self.event = "on_message_delete"
    
    async def handle(self, *args, **kwargs):
        # Get the message from the args
        message = args[0]

        # Ignore deletes of bot messages or messages from ourselves
        if message.author == self.client.user or message.author.bot:
            return
        # Build an embed that will log the deleted message
        embed_builder = EmbedBuilder(event="delete")
        await embed_builder.add_field(name="**Channel**", value=f"`#{message.channel.name}`")
        await embed_builder.add_field(name="**Author**", value=f"`{message.author.name}`")
        await embed_builder.add_field(name="**Message**", value=f"`{message.content}`")
        await embed_builder.add_field(name="**Created at**", value=f"`{message.created_at}`")
        embed = await embed_builder.get_embed()
        
        # Message the log channel the embed of the deleted message
        guild_id = str(message.guild.id)
        log_channel_id = int(self.client.storage.settings["guilds"][guild_id]["log_channel_id"])
        log_channel = discord.utils.get(message.guild.text_channels, id=log_channel_id)
        if log_channel is not None:
            await log_channel.send(embed=embed)
        else:
            print("No log channel found with that ID")


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
