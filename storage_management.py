import json
import os


class JsonFileManager:
    """ JsonFileManager class handles basic saving and loading of a json based settings file """
    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.file_path = ""
        self.settings = None

    async def init(self):
        """ Checks if the file exists, loads if it does, creates if it doesn't """
        if await self.file_exists():
            await self.load()
        else:
            await self.create_file()

    async def create_file(self):
        """ Create an empty JSON file, usually overwritten to provide config structure and defaults """
        self.settings = {}
        await self.write_file_to_disk()

    async def file_exists(self):
        """ Checks if the file exists """
        try:
            open(self.file_path, "r")
            return True
        except FileNotFoundError:
            return False

    async def load(self):
        """ Loads the json file from disk into self.settings """
        self.settings = await self.load_local()

    async def load_local(self):
        """ Returns the contents of the json file from disk, doesn't overwrite the stored settings. USE FOR READING VALUES ONLY! """
        with open(self.file_path, "r") as r:
            settings = json.load(r)
            r.close()
            return settings

    async def write_file_to_disk(self):
        """ Saves the contents of self.settings to disk """
        with open(self.file_path, "w+") as w:
            json.dump(self.settings, w, indent=4)
            w.close()


class StorageManagement(JsonFileManager):
    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.file_path = os.path.join(__location__, "settings.json")
        self.settings = None

    async def create_file(self):
        with open(self.file_path, "w+") as w:
            self.settings = w.read()
            w.close()
            self.settings = {
                "guilds": {}
            }
            await self.write_file_to_disk()
    
    async def has_guild(self, guild_id):
        guild_id = str(guild_id)
        if self.settings["guilds"].get(guild_id) is not None:
            return True
        else:
            return False

    async def add_guild(self, guild_id):
        guild_id = str(guild_id)
        self.settings["guilds"][guild_id] = {
            "muted_role_id": 0,
            "log_channel_id": 0,
            "mod_roles": [],
            "muted_users": {},
            "banned_users": {}
        }
        await self.write_file_to_disk()
        await self.load()


class ConfigManagement(JsonFileManager):
    """ Example custom config class to handle non guild-specific settings for customized features of the bot """
    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.file_path = os.path.join(__location__, "custom_config.json")
        self.settings = None

    async def create_file(self):
        self.settings = {
            "some_key": "some_value"
        }
        await self.write_file_to_disk()

    async def get_value(self, some_key):
        """ Example function loading a key from the config file """
        await self.load()
        return self.settings.get(some_key)

    async def set_value(self, some_key, some_value):
        """ Example function setting a value to the config file and saving it to disk """
        self.settings[some_key] = some_value
        await self.write_file_to_disk()
