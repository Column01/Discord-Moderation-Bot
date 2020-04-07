import discord

from helpers.misc_functions import is_number, is_valid_duration
from helpers.embed_builder import EmbedBuilder

class UnMuteCommand:
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}unmute <user id>"
        self.invalid_user = "There is no user with the userID: {user_id}. {usage}"
        self.not_enough_arguments = "You must provide a user to unmute. {usage}"
        self.not_a_user_id = "{user_id} is not a valid user ID. {usage}"
    
    async def handle(self, message, command):
        if len(command) == 2:
            if is_number(command[1]):
                guild_id = str(message.guild.id)
                user_id = int(command[1])
                muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
                user = message.guild.get_member(user_id)
                muted_role = message.guild.get_role(muted_role_id)
                if user is not None:
                    # Remove the muted role from the user and remove them from the guilds muted users list
                    await user.remove_roles(muted_role, reason=f"Unmuted by {message.author.name}")
                    self.storage.settings["guilds"][guild_id]["muted_users"].pop(str(user_id))
                    await self.storage.write_settings_file_to_disk()
                    # Message the channel
                    await message.channel.send(f"**Unmuted user:** `{user.name}`.")
                    
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
                await message.channel.send(self.not_a_user_id.format(user_id=command[1], usage=self.usage))
        else:
            await message.channel.send(self.not_enough_arguments.format(usage=self.usage))
    
    
class MuteCommand:
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}mute <user id> [reason]"
        self.invalid_user = "There is no user with the userID: {user_id}. {usage}"
        self.not_enough_arguments = "You must provide a user to unmute. {usage}"
        self.not_a_user_id = "{user_id} is not a valid user ID. {usage}"
    
    async def handle(self, message, command):
        if len(command) >= 2:
            if is_number(command[1]):
                guild_id = str(message.guild.id)
                user_id = int(command[1])
                muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
                user = message.guild.get_member(user_id)
                muted_role = message.guild.get_role(muted_role_id)
                if len(command) >= 3:
                    # Collects everything after the first two items in the command and uses it as a reason.
                    temp  = [item for item in command if command.index(item) > 1]
                    reason = " ".join(temp)
                else:
                    reason = f"Muted by {message.author.name}"
                if user is not None:
                    # Add the muted role and store them in guilds muted users list. We use -1 as the duration to state that it lasts forever.
                    await user.add_roles(muted_role, reason=f"Muted by {message.author.name}")
                    self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)] = {}
                    self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["duration"] = -1
                    self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["reason"] = reason
                    await self.storage.write_settings_file_to_disk()
                    # Message the channel
                    await message.channel.send(f"**Permanently muted user:** `{user.name}`. **Reason:** `{reason}`")
                    
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
                await message.channel.send(self.not_a_user_id.format(user_id=command[1], usage=self.usage))
        else:
            await message.channel.send(self.not_enough_arguments.format(usage=self.usage))
    
    
class TempMuteCommand:
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}tempmute <user id> <duration> [reason]"
        self.invalid_user = "There is no user with the userID: {user_id}. {usage}"
        self.invalid_duration = "The duration provided is invalid. The duration must be a number above zero in seconds. {usage}"
        self.not_enough_arguments = "You must provide a user to unmute. {usage}"
        self.not_a_user_id = "{user_id} is not a valid user ID. {usage}"
    
    async def handle(self, message, command):
        if len(command) >= 3:
            if is_number(command[1]):
                if is_valid_duration(command[2]):
                    guild_id = str(message.guild.id)
                    user_id = int(command[1])
                    duration = int(command[2])
                    muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
                    user = message.guild.get_member(user_id)
                    muted_role = message.guild.get_role(muted_role_id)
                    if len(command) >= 4:
                        # Collects everything after the first three items in the command and uses it as a reason.
                        temp  = [item for item in command if command.index(item) > 2]
                        reason = " ".join(temp)
                    else:
                        reason = f"Temp muted by {message.author.name}"
                    if user is not None:
                        # Add the muted role and store them in guilds muted users list. We use -1 as the duration to state that it lasts forever.
                        await user.add_roles(muted_role, reason=f"Muted by {message.author.name}")
                        self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)] = {}
                        self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["duration"] = duration
                        self.storage.settings["guilds"][guild_id]["muted_users"][str(user_id)]["reason"] = reason
                        await self.storage.write_settings_file_to_disk()
                        # Message the channel
                        await message.channel.send(f"**Temporarily muted user:** `{user.name}` **for:** `{duration}` **seconds. Reason:** `{reason}`")
                        
                        # Build the embed and message it to the log channel
                        embed_builder = EmbedBuilder(event="tempmute")
                        await embed_builder.add_field(name="**Executor**", value=f"`{message.author.name}`")
                        await embed_builder.add_field(name="**Muted user**", value=f"`{user.name}`")
                        await embed_builder.add_field(name="**Reason**", value=f"`{reason}`")
                        await embed_builder.add_field(name="**Duration**", value=f"`{duration}`")
                        embed = await embed_builder.get_embed()
                        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
                        log_channel = message.guild.get_channel(log_channel_id)
                        if log_channel is not None:
                            await log_channel.send(embed=embed)
                    else:
                        await message.channel.send()
                else:
                    await message.channel.send(self.invalid_user.format(user_id=user_id, usage=self.usage))
            else:
                await message.channel.send(self.not_a_user_id.format(user_id=command[1], usage=self.usage))
        else:
            await message.channel.send(self.not_enough_arguments.format(usage=self.usage))
