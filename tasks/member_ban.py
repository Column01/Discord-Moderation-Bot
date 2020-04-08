import discord

from helpers.embed_builder import EmbedBuilder


class MemberBan:
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = self.client.storage
    
    async def handle(self, guild):
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
