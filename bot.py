import os

import discord

from storage_management import StorageManagement

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class ModerationBot(discord.Client):
    def __init__(self, intents):
        # Change to whatever prefix you want
        self.prefix = "!"
        self.prefix_length = len(self.prefix)
        self.storage = StorageManagement()
        
        # Example of adding a custom config file, see below imported class
        # from storage_management import ConfigManagement
        # self.config = ConfigManagement()

        # Initialize the command registry
        from command_registry import registry
        self.registry = registry
        self.registry.set_instance(self)
        self.registry.register_commands()
        print("The bot has been initialized with the following commands: " + ", ".join(self.registry.get_command_names()))

        # Initialize event registry
        from event_registry import event_registry
        self.event_registry = event_registry
        self.event_registry.set_instance(self)
        self.event_registry.register_events()
        print("The bot has been initialized with the following events: " + ", ".join(self.event_registry.get_all_event_handlers()))

        # Permissions for the muted role and for the default role
        self.muted_permissions = discord.PermissionOverwrite(
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
        discord.Client.__init__(self, intents=intents)
    
    async def event_template(self, *args, **kwargs):
        """ The template event function used to replicate event functions dynamically.
        See event_registry.EventRegistry.register_events() where setattr() is used to add event handlers to this class
        This basically allows us to write one cookie-cutter function instead of implementing the whole discord.py event API
        """
        event_name = kwargs.get("event_name")
        event_handlers = self.event_registry.get_event_handlers(event_name)
        if event_handlers is not None:
            for event_handler in event_handlers:
                handler = event_handler(self)
                await handler.handle(*args, **kwargs)
    
    """ DISCORD CLIENT EVENTS START HERE (DEPRECATED, USE EVENT HANDLERS!) """
                
    async def on_guild_join(self, guild):
        print(f"Adding a guild to the bot's system since they invited us. Guild name: {guild.name}")
        await self.setup_guild(guild)
    
    async def on_guild_remove(self, guild):
        print(f"Removing guild from guild storage since they removed the bot. Guild name: {guild.name}")
        self.storage.settings.pop(guild.id)
        await self.storage.write_file_to_disk()
        
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        guild_id = str(guild.id)
        muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
        muted_role = discord.utils.get(guild.roles, id=muted_role_id)
        if muted_role is not None:
            await channel.set_permissions(target=muted_role, overwrite=self.muted_permissions)
        else:
            return

    """ DISCORD CLIENT EVENTS END HERE (DEPRECATED, USE EVENT HANDLERS!) """
    
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
            await self.storage.write_file_to_disk()
        else:
            return
        
    async def add_muted_role_to_channels(self, guild):
        guild_id = str(guild.id)
        # Get the muted role ID from disk and then get it from discord
        muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
        muted_role = discord.utils.get(guild.roles, id=muted_role_id)
        if muted_role is None:
            # Run the role check again to make sure they didn't delete the role or something went wrong in the flow of things.
            await self.check_for_muted_role(guild)
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
            await self.storage.write_file_to_disk()
        else:
            return


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
if __name__ == "__main__":
    # Read the token from a file and strip newlines (Fixes issues when running the bot on linux)
    try:
        token = open(os.path.join(__location__, "token.txt"), "r").read().strip("\n")
    except FileNotFoundError:
        quit("Please create a token.txt file and place your token in it!")
    if token is None:
        quit("Please create a token.txt file and place your token in it!")
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    # Run the bot instance
    bot = ModerationBot(intents)
    bot.run(token)
