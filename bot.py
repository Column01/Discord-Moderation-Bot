import json
import os
import time

import discord

from commands.ban import TempBanCommand, UnBanCommand
from commands.mute import MuteCommand, TempMuteCommand, UnMuteCommand
from helpers.embed_builder import EmbedBuilder
from storage_management import StorageManagement
from tasks.check_punishments import check_punishments
from tasks.member_ban import MemberBan
from tasks.member_join import MemberJoin
from tasks.member_kick import MemberKick
from tasks.message_delete import MessageDelete


class ModerationBot(discord.Client):
    def __init__(self):
        # Change to whatever prefix you want
        self.prefix = "mym!"
        self.prefix_length = len(self.prefix)
        self.storage = StorageManagement()
        # Permissions for the muted role and for the default role
        self.muted_permissions =  discord.PermissionOverwrite(
            send_messages=False, 
            add_reactions=False,
            attach_files=False,
            speak=False,
            send_tts_messages=False
        )
        self.default_permissions = discord.PermissionOverwrite(
            read_messages=False,
            send_messages=False
        )
        # Start the discord client
        discord.Client.__init__(self)
    
    ### DISCORD CLIENT EVENTS START HERE ###
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        # Start the storage management and setup the guilds we are connected to.
        await self.storage.init()
        for guild in self.guilds:
            await self.setup_guild(guild)
        # Register some tasks
        self.loop.create_task(check_punishments(self))
    
    async def on_message(self, message):
        user = message.author
        # Ignore messages from ourselves or other bots
        if user == self.user or user.bot or len(message.content) == 0:
            return
        # Split the message into a list of command arguments where command[0] is the command that was run and afterwards is the arguments.
        command = message.content.split()
        # If the first part of the message starts with the command prefix, interpret it as a command
        if command[0][:self.prefix_length] == self.prefix:
            if command[0] == self.prefix + "tempmute":
                temp_mute = TempMuteCommand(self)
                await temp_mute.handle(message, command)
            elif command[0] == self.prefix + "mute":
                mute = MuteCommand(self)
                await mute.handle(message, command)
            elif command[0] == self.prefix + "unmute":
                un_mute = UnMuteCommand(self)
                await un_mute.handle(message, command)
            elif command[0] == self.prefix + "tempban":
                temp_ban = TempBanCommand(self)
                await temp_ban.handle(message, command)
            elif command[0] == self.prefix + "unban":
                un_ban = UnBanCommand(self)
                await un_ban.handle(message, command)
            else:
                await message.channel.send(f"Unknown command: {message.content}")
                
    async def on_guild_join(self, guild):
        print(f"Adding a guild to the bot's system since they invited us. Guild name: {guild.name}")
        await self.setup_guild(guild)
    
    async def on_guild_remove(self, guild):
        print(f"Removing guild from guild storage since they removed the bot. Guild name: {guild.name}")
        self.storage.settings.pop(guild.id)
        await self.storage.write_settings_file_to_disk()
        
    async def on_message_delete(self, message):
        message_delete = MessageDelete(self)
        await message_delete.handle(message)
            
    async def on_member_join(self, member):
        member_join = MemberJoin(self)
        await member_join.handle(member)
        
    async def on_member_ban(self, guild, member):
        member_ban = MemberBan(self)
        await member_ban.handle(guild)
        
    async def on_member_remove(self, member):
        # Closest thing we have to kick event.
        member_kick = MemberKick(self)
        await member_kick.handle(member.guild)

    ### DISCORD CLIENT EVENTS END HERE ###
    
    async def setup_guild(self, guild):
        # Add the guild to the settings file if it doesn't exist
        if not await self.storage.has_guild(guild.id):
            await self.storage.add_guild(guild.id)
        # Checks if the muted role exists for that guild. If it doesn't, this creates it
        await self.check_for_muted_role(guild)
        # Add the muted role to the permissions of all channels on the server
        await self.add_muted_role_to_channels(guild)
        # Create the log channel if it doesn't exist
        await self.create_log_channel(guild)
         
    async def check_for_muted_role(self, guild):
        guild_id = str(guild.id)
        # Get the muted role ID from disk and try to get it from discord
        muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
        role_test = discord.utils.get(guild.roles, id=muted_role_id)
        if role_test is None:
            # The role doesn't exist so we create it
            muted_role = await guild.create_role(name="muted")
            self.storage.settings["guilds"][guild_id]["muted_role_id"] = muted_role.id
            await self.storage.write_settings_file_to_disk()
    
    async def add_muted_role_to_channels(self, guild):
        guild_id = str(guild.id)
        # Get the muted role ID from disk and then get it from discord
        muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
        muted_role = discord.utils.get(guild.roles, id=muted_role_id)
        # Edit all text and voice channels to deny the muted role from talking or doing certain actions
        for text_channel in guild.text_channels:
            await text_channel.set_permissions(target=muted_role, overwrite=self.muted_permissions)

        for voice_channel in guild.voice_channels:
            await voice_channel.set_permissions(target=muted_role, overwrite=self.muted_permissions)

    async def create_log_channel(self, guild):
        guild_id = str(guild.id)
        # Get the log channel ID from disk and then try to get it from discord
        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
        log_channel = discord.utils.get(guild.text_channels, id=log_channel_id)
        overwrites = {guild.default_role: self.default_permissions}
        if log_channel is None:
            # The log channel doesn't exist so we create it
            log_channel = await guild.create_text_channel(name="moderation", overwrites=overwrites)
            await log_channel.send("I created this channel for moderation logs. Please edit the channel permissions to allow what users you want to see this channel.")
            self.storage.settings["guilds"][guild_id]["log_channel_id"] = log_channel.id
            await self.storage.write_settings_file_to_disk()


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))          
if __name__ == "__main__":
    # Read the token from a file and strip newlines (Fixes issues when running the bot on linux)
    token = open(os.path.join(__location__, "token.txt"), "r").read().strip("\n")
    # Run the bot instance
    bot = ModerationBot()
    bot.run(token)
