

def is_number(string):
    """Checks if the string is a number

    Args:
        string (str): The string to check

    Returns:
        Boolean: Whether the string could be converted to a number or not
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


def is_valid_duration(duration):
    """Checks if the duration is a positive number

    Args:
        duration (int, str): The duration to validate

    Returns:
        Boolean: If it is a valid duration
    """
    if is_number(duration):
        if int(duration) > 0:
            return True
        else:
            return False
    else:
        return False
    

def parse_duration(s):
    """Parses a duration in seconds from a duration string

    Args:
        s (str): Duration string to parse (1w3d10h30m20s)

    Returns:
        int: The time in seconds of the duration string
    """
    if is_number(s):
        return s
    else:
        values = {"w": 604800, "d": 86400, "h": 3600, "m": 60, "s": 1}
        nums = []
        tempnums = []
        for char in s:
            if char.isdigit():
                tempnums.append(char)
            else:
                multiple = values.get(char, 1)
                num = int("".join(tempnums))
                tempnums.clear()
                nums.append(num * multiple)
        if len(nums) > 0:
            return sum(nums)
        else:
            return -1
        
        
def author_is_admin(author):
    """Checks if the author is an administrator

    Args:
        author (discord.Member): Discord member object

    Returns:
        Boolean: If they are an administrator
    """
    return author.guild_permissions.administrator


async def author_is_mod(author, storage):
    """Checks if the author is a mod or administrator

    Args:
        author (discord.Member): Discord member object
        storage (StorageManagement): Instance of the storage management class

    Returns:
        Boolean: If they are a mod or administrator
    """
    if author_is_admin(author):
        return True
    guild_id = str(author.guild.id)
    mod_roles = storage.settings["guilds"][guild_id].get("mod_roles")
    if mod_roles is None:
        storage.settings["guilds"][guild_id]["mod_roles"] = []
        await storage.write_settings_file_to_disk()
        mod_roles = storage.settings["guilds"][guild_id].get("mod_roles")
    return set(mod_roles) & set(author.roles)
