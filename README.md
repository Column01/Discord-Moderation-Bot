# MyM Moderation Bot
A bot for moderating users on discord

## Requirements
- [**Python**](https://www.python.org/downloads/) *version 3.6+*
- [**discord.py**](https://pypi.org/project/discord.py/) *version 1.3.3*

Install python and run: `pip install discord.py==1.3.3`

## Command Info

- Default prefix: `mym!`
- `<argument>` = **Required argument**
- `[argument]` = **Optional argument**
- Durations can either be a formatted time that looks like the following: (`1w2d3h4m5s`) or time in seconds.
- Durations can also use single types like `2m` or `1w` for example
- Read how to get the User ID [here](#how-to-get-user-id)

### Commands
- `mym!mute <user ID> [reason]`
	- Permanently mutes the user. Must be unmuted manually.

- `mym!tempmute <user ID> <duration> [reason]`
	- Temporarily mutes the user.

- `mym!unmute <user ID>`
	- Unmutes the user

- `mym!tempban <user ID> <duration> <reason>`
	- Temporarily bans the user from the server
	- Reason is required. If you do not have a reason, you should not be banning them.

- `mym!unban <user ID>`
	- Unbans the user from the server.

### How to get user ID
You should follow the discord guide [here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

**But the gist is:**

- Enable developer mode in discord
- Right click their username in chat or on the sidebar
- Click `Copy ID`
