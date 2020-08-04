import discord

from helpers.embed_builder import EmbedBuilder


class MessageDelete:
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = self.client.storage
        
    async def handle(self, message):
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
        log_channel_id = int(self.storage.settings["guilds"][guild_id]["log_channel_id"])
        log_channel = discord.utils.get(message.guild.text_channels, id=log_channel_id)
        if log_channel is not None:
            await log_channel.send(embed=embed)
