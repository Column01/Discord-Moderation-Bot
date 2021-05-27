import inspect
import sys

from helpers.misc_functions import author_is_admin, is_number

from commands.base import Command


class ModCommand(Command):
    def __init__(self, client_instance):
        self.cmd = "mod"
        self.client = client_instance
        self.storage = client_instance.storage
        self.usage = f"Usage: {self.client.prefix}mod <add|remove|list> <role_id>"
        self.not_a_valid_role = "Sorry, that role is not a valid role ID."
        self.invalid_option = "The option: {option} is not an option"
        self.not_enough_arguments = "You must provide a role to make a moderator role."
        self.role_already_mod = "That role ID is already listed as a mod."

    async def execute(self, message, **kwargs):
        command = kwargs.get("args")
        if author_is_admin(message.author):
            if len(command) == 2:
                guild_id = str(message.guild.id)
                if command[0] == "add":
                    if is_number(command[1]):
                        role_id = int(command[1])
                        mod_role = message.guild.get_role(role_id)
                        # If the mod role exists
                        if mod_role is not None:
                            # Load the list of mod roles from disk
                            mod_roles = self.storage.settings["guilds"][guild_id].get("mod_roles")
                            # Create the section of mod roles if one doesn't exist
                            if mod_roles is None:
                                self.storage.settings["guilds"][guild_id]["mod_roles"] = []
                                await self.storage.write_settings_file_to_disk()
                                mod_roles = self.storage.settings["guilds"][guild_id].get("mod_roles")
                            if role_id not in mod_roles:
                                # Add the mod role to the settings storage
                                mod_roles.append(role_id)
                                await self.storage.write_settings_file_to_disk()
                                await message.channel.send(f"**Added** `{mod_role.name}` **as a moderator role.** ")
                            else:
                                # That role is already a mod
                                await message.channel.send(self.role_already_mod)
                        else:
                            await message.channel.send(self.not_a_valid_role)
                    else:
                        await message.channel.send(self.not_a_valid_role)
                elif command[0] == "remove":
                    if is_number(command[1]):
                        role_id = int(command[1])
                        # Get the mod role from the guild and assign the name as the role ID if it doesn't exist.
                        mod_role = message.guild.get_role(role_id)
                        if mod_role is None:
                            role_name = str(role_id)
                        else:
                            role_name = mod_role.name
                        # Get the mod roles from disk
                        mod_roles = self.storage.settings["guilds"][guild_id].get("mod_roles")
                        # Create the section if it doesn't exist
                        if mod_roles is None:
                            self.storage.settings["guilds"][guild_id]["mod_roles"] = []
                            await self.storage.write_settings_file_to_disk()
                            mod_roles = self.storage.settings["guilds"][guild_id].get("mod_roles")
                        # If the role is in the mods list, remove it.
                        if role_id in mod_roles:
                            mod_roles.remove(role_id)
                            await self.storage.write_settings_file_to_disk()
                            await message.channel.send(f"**Removed** `{role_name}` **from the moderator roles.**")
                        else:
                            # The role was not listed as a mod.
                            await message.channel.send(f"**The role ID** `{str(role_id)}` **is not a moderator role.**")
                    else:
                        await message.channel.send(self.not_a_valid_role)
                elif command[0] == "list":
                    await self.list_mods(message)
                else:
                    await message.channel.send(self.invalid_option.format(option=command[0]))

            elif len(command) == 1:
                if command[0] == "list":
                    await self.list_mods(message)
                else:
                    await message.channel.send(self.invalid_option.format(option=command[0]))
            else:
                await message.channel.send(self.not_enough_arguments)
        else:
            await message.channel.send("**You must be an Administrator to use this command.**")
    
    async def list_mods(self, message):
        # Get all mod roles from disk
        guild_id = str(message.guild.id)
        mod_roles = self.storage.settings["guilds"][guild_id].get("mod_roles")
        # Create the section if it doesn't exist
        if mod_roles is None:
            self.storage.settings["guilds"][guild_id]["mod_roles"] = []
            await self.storage.write_settings_file_to_disk()
            mod_roles = self.storage.settings["guilds"][guild_id].get("mod_roles")
        # If there is at least one mod role, send them to the channel.
        if len(mod_roles) >= 1:
            mod_roles = ", ".join([str(i) for i in mod_roles])
            await message.channel.send(f"**Here is a list of all moderator roles:** `{mod_roles}`")
        else:
            await message.channel.send("**You have not made any roles a moderator.**")


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
