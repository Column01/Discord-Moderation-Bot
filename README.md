# Modular Discord Moderation Bot

A modular bot for moderating users on discord! Add custom commands and event handlers to customize the bot to your liking. Reload the bot using the builtin `!reload` or `!reload events` command to see your changes applied LIVE!

[Adding your own commands](DEVELOPING.md#custom-commands)

[Adding your own event handlers](DEVELOPING.md#custom-event-handlers)

[Adding your own storage file](DEVELOPING.md#custom-storage-file)

## Installation/Setup

### Installing Requirements

- [**Python**](https://www.python.org/downloads/) *Version 3.8+ but just get the latest...*
- [**discord.py**](https://pypi.org/project/discord.py/) *Version 2.0.0*
  - Windows install: `python -m pip install discord.py`
  - Linux install: `pip3 install discord.py`

### Creating a bot account with Discord

1. Go to the [discord developer portal](https://discord.com/developers/applications) and create a new application
2. Navigate to the `Bot` section and click `Add a bot`. Fill in the necessary info (like name and an image if you like)
3. Scroll down to the `Privileged Gateway Intents` section and make sure to select the `SERVER MEMBERS INTENT` and `MESSAGE CONTENT INTENT`. **Click save so it saves your changes!**
4. Now scroll back up and click the `Reset Token` button, follow the screen prompts until you can copy that token. This is how the program will log in as this bot account. **DO NOT SHARE THIS TOKEN WITH ANYONE!**
5. Paste the newly copied token into a text file called `token.txt` in the same folder as the `bot.py` file.

### Inviting the bot to your server

1. On the application page for your bot in the [discord developer portal](https://discord.com/developers/applications), click the `OAuth2` section.
2. Now click the `URL Generator` section on the sidebar
3. Select the `bot` scope and then select the `Administrator` permission in the newly displayed Bot Permissions checkbox list
4. Copy the URL from the bottom and paste it into your browser. Follow the onscreen prompts to invite the bot to your server. You must be an administrator to invite the bot to the server.

### Running the bot

1. Open a command prompt in the root directory of the bot files (where `bot.py` is) and run the command `python bot.py` to run the bot.
2. You should see some output on the screen talking about loading commands and logging in as the bot. If that all works, now you can use the bot!
3. Add any moderator roles you want to the bot using the commands below!

## Bot Information

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

- `!ban <user ID> <duration> <reason>`
  - Bans the user from the server for the duration specified
  - Reason is required. If you do not have a reason, you should not be banning them.

- `!unban <user ID>`
  - Unbans the user from the server.

- `!reload`
  - Reloads the command registry for any changes that were made to commands

- `!reload events`
  - Reloads the event registry for any changes that were made

### How to get user ID

You should follow the discord guide [here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

**But the gist is:**

- Enable developer mode in discord
- Right click their username in chat or on the sidebar
- Click `Copy ID`

### Issues with custom commands?

Ensure that:

- Your command is a subclass of the base command class. (use `from commands.base import Command` and then define the class like this: `class MyCommand(Command):` so it is a subclass of it)
- It has an `async def execute(self, message, **kwargs):` function to execute the command
- It doesn't have basic python syntax errors.
