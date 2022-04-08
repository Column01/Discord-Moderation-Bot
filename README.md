# Modular Discord Moderation Bot

A modular bot for moderating users on discord! Add custom commands and event handlers to customize the bot to your liking. Reload the bot using the builtin `!reload` or `!reload events` command to see your changes applied LIVE!

[Adding your own commands](DEVELOPING.md#custom-commands)

[Adding your own event handlers](DEVELOPING.md#custom-event-handlers)

[Adding your own storage file](DEVELOPING.md#custom-storage-file)

## About discord.py

It's back! You can safely install version 1.7.3 from PyPi and it will work for the foreseeable future. I will be updating the code to use the v2.0 code as soon as it's in a stable release.

## Requirements

- [**Python**](https://www.python.org/downloads/) *Version 3.6+ but just get the latest...*
- [**discord.py**](https://pypi.org/project/discord.py/) *Version 1.7.3*

Install python and run: `pip install discord.py`

## Running the bot

1. Place a text file named ``token.txt`` in the root directory (with `bot.py`) and place your auth token in it
2. Open a command prompt and use ``python bot.py`` to run the bot.

## Command Info

- Default prefix: `!`
- `<argument>` = **Required argument**
- `[argument]` = **Optional argument**
- Durations can either be a formatted time that looks like the following: (`1w2d3h4m5s`) or time in seconds.
- Durations can also use single types like `2m` or `1w` for example
- All commands require you to be in a moderator role. See the commands below on how to add or remove a mod role (requires admin permission to add mod roles)
- Read how to get the User ID [here](#how-to-get-user-id)

## Commands

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

## How to get user ID

You should follow the discord guide [here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

**But the gist is:**

- Enable developer mode in discord
- Right click their username in chat or on the sidebar
- Click `Copy ID`

## Issues with custom commands?

Ensure that:

- Your command is a subclass of the base command class. (use `from commands.base import Command` and then define the class like this: `class MyCommand(Command):` so it is a subclass of it)
- It has an `async def execute(self, message, **kwargs):` function to execute the command
- It doesn't have basic python syntax errors.
