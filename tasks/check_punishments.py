import asyncio
import time

from helpers.embed_builder import EmbedBuilder


async def check_punishments(client):
    while True:
        for guild in client.guilds:
            guild_id = str(guild.id)
            muted_role_id = int(client.storage.settings["guilds"][guild_id]["muted_role_id"])
            log_channel_id = int(client.storage.settings["guilds"][guild_id]["log_channel_id"])
            muted_role = guild.get_role(muted_role_id)
            log_channel = guild.get_channel(log_channel_id)
            
            # Get the muted users for the server
            muted_users = client.storage.settings["guilds"][guild_id]["muted_users"]
            mutes_to_remove = []
            for user_info in muted_users.items():
                user_id = int(user_info[0])
                duration = int(user_info[1]["duration"])
                normal_duration = user_info[1]["normal_duration"]
                if -1 < duration < int(time.time()):
                    # Mute is expired. Remove it from the user and remove it from the guild's storage
                    user = await guild.fetch_member(user_id)
                    # Happens if they leave the guild. We re-add the role when they return though so this doesn't bypass the mute.
                    if user is None:
                        continue
                    await user.remove_roles(muted_role, reason="Temp mute expired.")
                    mutes_to_remove.append(user_id)
                    
                    # Build a mute expire embed and message it to the log channel
                    embed_builder = EmbedBuilder(event="muteexpire")
                    await embed_builder.add_field(name="**Unmuted user**", value=f"`{user.name}`")
                    await embed_builder.add_field(name="**Mute duration**", value=f"`{normal_duration}`")
                    embed = await embed_builder.get_embed()
                    await log_channel.send(embed=embed)
                    
            # Loop over all the mutes to remove and remove them from the storage.
            # (This is done aftewards since if we do it in the loop, python complains the dict size changed)
            for user_id in mutes_to_remove:
                client.storage.settings["guilds"][guild_id]["muted_users"].pop(str(user_id))
            await client.storage.write_settings_file_to_disk()
            
            # Not added yet so I left it blank for now
            banned_users = client.storage.settings["guilds"][guild_id]["banned_users"]
            bans_to_remove = []
            for user_info in banned_users.items():
                user_id = int(user_info[0])
                duration = int(user_info[1]["duration"])
                normal_duration = user_info[1]["normal_duration"]
                if -1 < duration < int(time.time()):
                    # Ban is expired. Unban the user and remove it from the guild's storage
                    user = await client.fetch_user(user_id)
                    if user is None:
                        print(f"No user with id {user_id}")
                        continue
                    await guild.unban(user, reason="Temp ban expired")
                    bans_to_remove.append(user_id)
                    
                    # Build a ban expire embed and message it to the log channel.
                    embed_builder = EmbedBuilder(event="banexpire")
                    await embed_builder.add_field(name="**Unbanned user**", value=f"`{user.name}`")
                    await embed_builder.add_field(name="**Ban duration**", value=f"`{normal_duration}`")
                    embed = await embed_builder.get_embed()
                    await log_channel.send(embed=embed)
                    
            # Loop over all the mutes to remove and remove them from the storage.
            # (This is done aftewards since if we do it in the loop, python complains the dict size changed)
            for user_id in bans_to_remove:
                client.storage.settings["guilds"][guild_id]["banned_users"].pop(str(user_id))
            await client.storage.write_settings_file_to_disk()

        # Run every 5 seconds
        await asyncio.sleep(5)
