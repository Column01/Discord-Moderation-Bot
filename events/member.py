import inspect
import sys
import time

import discord
from helpers.embed_builder import EmbedBuilder

from events.base import EventHandler


class MemberJoinEvent(EventHandler):
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = self.client.storage
        self.event = "on_member_join"
    
    async def handle(self, *args, **kwargs):
        # Get member from args
        member = args[0]

        guild = member.guild
        guild_id = str(guild.id)
        muted_role_id = int(self.storage.settings["guilds"][guild_id]["muted_role_id"])
        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
        muted_role = guild.get_role(muted_role_id)
        log_channel = guild.get_channel(log_channel_id)
        muted_users = self.storage.settings["guilds"][guild_id]["muted_users"]
        mutes_to_remove = []
        # Loop over the muted users
        for user_info in muted_users.items():
            user_id = int(user_info[0])
            duration = int(user_info[1]["duration"])
            normal_duration = user_info[1]["normal_duration"]
            user = await guild.fetch_member(user_id)
            # if the user_id for this user_info matches the member who joined the guild
            if user_id == member.id:
                if -1 < duration < int(time.time()):
                    # Mute is expired. Remove it from the guild's storage
                    mutes_to_remove.append(user_id)
                    # Build a mute expire embed and message it to the log channel
                    embed_builder = EmbedBuilder(event="muteexpire")
                    await embed_builder.add_field(name="**Unmuted user**", value=f"`{user.name}`")
                    await embed_builder.add_field(name="**Mute duration**", value=f"`{normal_duration}`")
                    embed = await embed_builder.get_embed()
                    await log_channel.send(embed=embed)
                else:
                    # Mute is not expired. Re-add it to the offender
                    await user.add_roles(muted_role, reason="Remuted user since they had an active mute when they rejoined the server")
        
        for user_id in mutes_to_remove:
            self.storage.settings["guilds"][guild_id]["muted_users"].pop(str(user_id))
        await self.storage.write_file_to_disk()


class MemberBanEvent(EventHandler):
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = self.client.storage
        self.event = "on_member_ban"
    
    async def handle(self, *args, **kwargs):
        # Get the guild from the args
        guild = args[0]

        guild_id = str(guild.id)
        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
        log_channel = guild.get_channel(log_channel_id)
        
        # Get the actions we already logged recently
        logged_actions = []
        async for message in log_channel.history(limit=25):
            for embed in message.embeds:
                for field in embed.fields:
                    if field.name == "**Audit Log ID**":
                        logged_actions.append(int(field.value.replace("`", "")))
                        
        # Get recent ban actions
        async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=5):
            # If the entry was made by the bot or it's entry ID has already been logged, skip it
            if entry.user == self.client.user or entry.id in logged_actions:
                continue
            else:
                # Build a ban embed with the info.
                embed_builder = EmbedBuilder(event="ban")
                await embed_builder.add_field(name="**Executor**", value=f"`{entry.user.name}`")
                await embed_builder.add_field(name="**Banned User**", value=f"`{entry.target.name}`")
                await embed_builder.add_field(name="**Reason**", value=f"`{entry.reason}`")
                await embed_builder.add_field(name="**Audit Log ID**", value=f"`{entry.id}`")
                embed = await embed_builder.get_embed()
                await log_channel.send(embed=embed)


class MemberKickEvent(EventHandler):
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = self.client.storage
        self.event = "on_member_remove"
    
    async def handle(self, *args, **kwargs):
        # Get the guild from the args
        guild = args[0]

        guild_id = str(guild.id)
        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
        log_channel = guild.get_channel(log_channel_id)
        
        # Get the actions we already logged recently
        logged_actions = []
        async for message in log_channel.history(limit=25):
            for embed in message.embeds:
                for field in embed.fields:
                    if field.name == "**Audit Log ID**":
                        logged_actions.append(int(field.value.replace("`", "")))

        # Get recent kick actions
        async for entry in guild.audit_logs(action=discord.AuditLogAction.kick, limit=5):
            # If the entry was made by the bot or it's entry ID has already been logged, skip it.
            if entry.user == self.client.user or entry.id in logged_actions:
                continue
            else:
                # Build a kick embed with the info.
                embed_builder = EmbedBuilder(event="kick")
                await embed_builder.add_field(name="**Executor**", value=f"`{entry.user.name}`")
                await embed_builder.add_field(name="**Kicked User**", value=f"`{entry.target.name}`")
                await embed_builder.add_field(name="**Reason**", value=f"`{entry.reason}`")
                await embed_builder.add_field(name="**Audit Log ID**", value=f"`{entry.id}`")
                embed = await embed_builder.get_embed()
                await log_channel.send(embed=embed)


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
