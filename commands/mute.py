import inspect
import sys
import time

from helpers.embed_builder import EmbedBuilder
from helpers.misc_functions import (author_is_mod, is_number,
                                    is_valid_duration, parse_duration)

from commands.base import Command


class UnMuteCommand(Command):
    def __init__(self, client_instance):
        self.cmd = "unmute"
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}unmute <user id>"
        self.invalid_user = "There is no user with the userID: {user_id}. {usage}"
        self.not_enough_arguments = "You must provide a user to unmute. {usage}"
        self.not_a_user_id = "{user_id} is not a valid user ID. {usage}"

    async def execute(self, message, **kwargs):
        command = kwargs.get("args")
        if await author_is_mod(message.author, self.storage):
            if len(command) == 1:
                if is_number(command[0]):
                    guild_id = str(message.guild.id)
                    user_id = int(command[0])
                    muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
                    user = await message.guild.fetch_member(user_id)
                    muted_role = message.guild.get_role(muted_role_id)
                    if user is not None:
                        # Remove the muted role from the user and remove them from the guilds muted users list
                        await user.remove_roles(muted_role, reason=f"Unmuted by {message.author.name}")
                        self.storage.settings["guilds"][guild_id]["muted_users"].pop(str(user_id))
                        await self.storage.write_settings_file_to_disk()
                        # Message the channel
                        await message.channel.send(f"**Unmuted user:** `{user.name}`**.**")
                        
                        # Build the embed and message it to the log channel
                        embed_builder = EmbedBuilder(event="unmute")
                        await embed_builder.add_field(name="**Executor**", value=f"`{message.author.name}`")
                        await embed_builder.add_field(name="**Unmuted user**", value=f"`{user.name}`")
                        embed = await embed_builder.get_embed()
                        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
                        log_channel = message.guild.get_channel(log_channel_id)
                        if log_channel is not None:
                            await log_channel.send(embed=embed)
                    else:
                        await message.channel.send(self.invalid_user.format(user_id=user_id, usage=self.usage))
                else:
                    await message.channel.send(self.not_a_user_id.format(user_id=command[0], usage=self.usage))
            else:
                await message.channel.send(self.not_enough_arguments.format(usage=self.usage))
        else:
            await message.channel.send("**You must be a moderator to use this command.**")


class MuteCommand(Command):
    def __init__(self, client_instance):
        self.cmd = "mute"
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}mute <user id> [reason]"
        self.invalid_user = "There is no user with the userID: {user_id}. {usage}"
        self.not_enough_arguments = "You must provide a user to mute. {usage}"
        self.not_a_user_id = "{user_id} is not a valid user ID. {usage}"

    async def execute(self, message, **kwargs):
        command = kwargs.get("args")
        if await author_is_mod(message.author, self.storage):
            if len(command) >= 1:
                if is_number(command[0]):
                    guild_id = str(message.guild.id)
                    user_id = int(command[0])
                    muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
                    user = await message.guild.fetch_member(user_id)
                    muted_role = message.guild.get_role(muted_role_id)
                    if len(command) >= 2:
                        # Collects everything after the first item in the command and uses it as a reason.
                        temp = [item for item in command if command.index(item) > 0]
                        reason = " ".join(temp)
                    else:
                        reason = f"Muted by {message.author.name}"
                    if user is not None:
                        # Add the muted role and store them in guilds muted users list. We use -1 as the duration to state that it lasts forever.
                        await user.add_roles(muted_role, reason=f"Muted by {message.author.name}")
                        self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)] = {}
                        self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["duration"] = -1
                        self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["reason"] = reason
                        self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["normal_duration"] = -1
                        await self.storage.write_settings_file_to_disk()
                        # Message the channel
                        await message.channel.send(f"**Permanently muted user:** `{user.name}`**. Reason:** `{reason}`")
                        
                        # Build the embed and message it to the log channel
                        embed_builder = EmbedBuilder(event="mute")
                        await embed_builder.add_field(name="**Executor**", value=f"`{message.author.name}`")
                        await embed_builder.add_field(name="**Muted user**", value=f"`{user.name}`")
                        await embed_builder.add_field(name="**Reason**", value=f"`{reason}`")
                        embed = await embed_builder.get_embed()
                        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
                        log_channel = message.guild.get_channel(log_channel_id)
                        if log_channel is not None:
                            await log_channel.send(embed=embed)
                        
                    else:
                        await message.channel.send(self.invalid_user.format(user_id=user_id, usage=self.usage))
                else:
                    await message.channel.send(self.not_a_user_id.format(user_id=command[0], usage=self.usage))
            else:
                await message.channel.send(self.not_enough_arguments.format(usage=self.usage))
        else:
            await message.channel.send("**You must be a moderator to use this command.**")
    
    
class TempMuteCommand(Command):
    def __init__(self, client_instance):
        self.cmd = "tempmute"
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}tempmute <user id> <duration> [reason]"
        self.invalid_user = "There is no user with the userID: {user_id}. {usage}"
        self.invalid_duration = "The duration provided is invalid. The duration must be a string that looks like: 1w3d5h30m20s or a positive number in seconds. {usage}"
        self.not_enough_arguments = "You must provide a user to temp mute. {usage}"
        self.not_a_user_id = "{user_id} is not a valid user ID. {usage}"

    async def execute(self, message, **kwargs):
        command = kwargs.get("args")
        if await author_is_mod(message.author, self.storage):
            if len(command) >= 2:
                if is_number(command[0]):
                    user_id = int(command[0])
                    duration = parse_duration(command[1])
                    if is_valid_duration(duration):
                        guild_id = str(message.guild.id)
                        mute_duration = int(time.time()) + duration
                        muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
                        user = await message.guild.fetch_member(user_id)
                        muted_role = message.guild.get_role(muted_role_id)
                        if len(command) >= 3:
                            # Collects everything after the first two items in the command and uses it as a reason.
                            temp = [item for item in command if command.index(item) > 1]
                            reason = " ".join(temp)
                        else:
                            reason = f"Temp muted by {message.author.name}"
                        if user is not None:
                            # Add the muted role and store them in guilds muted users list. We use -1 as the duration to state that it lasts forever.
                            await user.add_roles(muted_role, reason=f"Muted by {message.author.name}")
                            self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)] = {}
                            self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["duration"] = mute_duration
                            self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["reason"] = reason
                            self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["normal_duration"] = command[1]
                            await self.storage.write_settings_file_to_disk()
                            # Message the channel
                            await message.channel.send(f"**Temporarily muted user:** `{user.name}` **for:** `{command[1]}`**. Reason:** `{reason}`")
                            
                            # Build the embed and message it to the log channel
                            embed_builder = EmbedBuilder(event="tempmute")
                            await embed_builder.add_field(name="**Executor**", value=f"`{message.author.name}`")
                            await embed_builder.add_field(name="**Muted user**", value=f"`{user.name}`")
                            await embed_builder.add_field(name="**Reason**", value=f"`{reason}`")
                            await embed_builder.add_field(name="**Duration**", value=f"`{command[1]}`")
                            embed = await embed_builder.get_embed()
                            log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
                            log_channel = message.guild.get_channel(log_channel_id)
                            if log_channel is not None:
                                await log_channel.send(embed=embed)
                        else:
                            await message.channel.send(self.invalid_user.format(user_id=user_id, usage=self.usage))
                    else:
                        await message.channel.send(self.invalid_duration.format(user_id=user_id, usage=self.usage))
                else:
                    await message.channel.send(self.not_a_user_id.format(user_id=command[0], usage=self.usage))
            else:
                await message.channel.send(self.not_enough_arguments.format(usage=self.usage))
        else:
            await message.channel.send("**You must be a moderator to use this command.**")


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
