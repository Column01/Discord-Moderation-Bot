# Discord Moderation Bot

A bot for moderating users on discord!

## Requirements

- [**Python**](https://www.python.org/downloads/) *version 3.6+*
- [**discord.py**](https://pypi.org/project/discord.py/)

Install python and run: `pip install discord.py`

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

- `!tempban <user ID> <duration> <reason>`
  - Temporarily bans the user from the server
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
5. Inside the `self.execute` method, add the code that will run the command!
5b. Please see below for info that command executors can obtain for use!
6. Once you are done, save your file and use the `!reload` command to reload the command registry! You should be able to sue the new command!

#### Available keyword arguments

Obtain each using `my_var = kwargs.get("key")` where `key` is an option from below

- `command`
  - The name of the command. In the example above, this would just be `test`
- `args`
  - A list of arguments following the `command`. This can be any length so ensure your code has proper checking for argument lengths and stuff
- `storage`
  - An instance of the storage handler class. Really should only be used if you know what you are doing! See `storage_management.py` for the code of that class.
- `instance`
  - An instance of the bot, should REALLY not be used but is available if absolutely needed
