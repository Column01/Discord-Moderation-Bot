# Discord Moderation Bot
A bot for moderating users on discord

## Requirements
- [**Python**](https://www.python.org/downloads/) *version 3.6+*
- [**discord.py**](https://pypi.org/project/discord.py/) *version 1.3.3*

Install python and run: `pip install discord.py==1.3.3`

## Command Info

- Default prefix: `!`
- `<argument>` = **Required argument**
- `[argument]` = **Optional argument**
- Durations can either be a formatted time that looks like the following: (`1w2d3h4m5s`) or time in seconds.
- Durations can also use single types like `2m` or `1w` for example
- All commands require you to be in a moderator role. See the commands below on how to add or remove a mod role (requires admin permission to add mod roles)
- Read how to get the User ID [here](#how-to-get-user-id)

### Commands

- `!mod <add|remove|list> <role ID>`
	- Adds, removes the role ID to the list of moderator roles.
	- If you want to `list` the roles, you do not need the role ID at the end.

- `!mute <user ID> [reason]`
	- Permanently mutes the user. Must be unmuted manually.

- `!tempmute <user ID> <duration> [reason]`
	- Temporarily mutes the user.

- `!unmute <user ID>`
	- Unmutes the user

- `!tempban <user ID> <duration> <reason>`
	- Temporarily bans the user from the server
	- Reason is required. If you do not have a reason, you should not be banning them.

- `!unban <user ID>`
	- Unbans the user from the server.

### How to get user ID
You should follow the discord guide [here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

**But the gist is:**

- Enable developer mode in discord
- Right click their username in chat or on the sidebar
- Click `Copy ID`
