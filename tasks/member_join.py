import time

from helpers.embed_builder import EmbedBuilder


class MemberJoin:
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = self.client.storage
        
    async def handle(self, member):
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
        await self.storage.write_settings_file_to_disk()
