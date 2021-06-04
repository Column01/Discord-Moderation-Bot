# Modular Discord Moderation Bot

A modular bot for moderating users on discord!

Please note: This bot was intended as a proof of concept and support may be slow. Sorry if you tried to use this and it has issues, please just post an issue report and I will try to address it when possible.

## Requirements

- [**Python**](https://www.python.org/downloads/) *version 3.6+*
- [**discord.py**](https://pypi.org/project/discord.py/)

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
- Read how to add your own commands (and reload them on the fly!) [here](#adding-your-own-commands)

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

### How to get user ID

You should follow the discord guide [here](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

**But the gist is:**

- Enable developer mode in discord
- Right click their username in chat or on the sidebar
- Click `Copy ID`

### Adding your own commands

1. You'll need to make a new file for your command. The best thing to do is copy `reload.py` inside the `commands` directory and rename it to the command name e.g. `test.py`
2. Open `<your_command>.py` in a text editor
3. Rename the class: `ReloadCommand` to a different name e.g.`TestCommand`
4. Edit the `self.cmd` variable to be the command you wish to use e.g. `test`
5. Inside the `self.execute` method, add the code that will run the command! (Please see below for info that command executors can obtain for use!)
6. Once you are done, save your file and use the `!reload` command to reload the command registry! You should be able to use the new command!

#### Available keyword arguments for command handlers

Obtain each using `my_var = kwargs.get("key")` where `key` is an option from below

- `command`
  - The name of the command. In the example above, this would just be `test`
- `args`
  - A list of arguments following the `command`. This can be any length so ensure your code has proper checking for argument lengths and stuff
- `storage`
  - An instance of the storage handler class. Really should only be used if you know what you are doing! See `storage_management.py` for the code of that class.
- `instance`
  - An instance of the bot, should REALLY not be used but is available if absolutely needed

#### Issues with custom commands?

Ensure that:

- Your command is a subclass of the base command class. (use `from commands.base import Command` and then define the class like this: `class MyCommand(Command):` so it is a subclass of it)
- It has an `async def execute(self, message, **kwargs):` function to execute the command
- It doesn't have basic python syntax errors.
