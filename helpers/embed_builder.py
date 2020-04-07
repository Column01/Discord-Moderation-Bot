import discord

class EmbedBuilder:
    def __init__(self, event):
        if event == "delete":
            self.embed = discord.Embed(title="Deleted Message", description="A message was Deleted", color=0xffff00)
        elif event == "mute":
            self.embed = discord.Embed(title="Muted user", description="A user was Muted", color=0xff8000)
        elif event == "tempmute":
            self.embed = discord.Embed(title="Temp-Muted user", description="A user was Temp-Muted", color=0xff8000)
        elif event == "unmute":
            self.embed = discord.Embed(title="Un-Muted user", description="A user was Un-Muted", color=0x00ff00)
        elif event == "tempban":
            self.embed = discord.Embed(title="Temp Banned user", description="A user was Temp Banned", color=0xff0000)
        elif event == "unban":
            self.embed = discord.Embed(title="Un-Banned user", description="A user was Un-Banned", color=0x00ff00)
        else:
            self.embed = discord.Embed(title="Embed")
        
    async def add_field(self, name, value, inline=False):
        self.embed.add_field(name=name, value=value, inline=inline)

    async def get_embed(self):
        return self.embed