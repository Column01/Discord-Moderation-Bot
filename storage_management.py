import json
import os


class StorageManagement:
    def __init__(self):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.settings_file_path = os.path.join(__location__, "settings.json")
        self.settings = None
            
    async def init(self):
        # Create the settings file and load it
        if await self.settings_file_exists():
            await self.load_settings()
        else:
            await self.create_settings_file()
    
    async def settings_file_exists(self):
        try:
            open(self.settings_file_path, "r")
            return True
        except FileNotFoundError:
            return False

    async def create_settings_file(self):
        with open(self.settings_file_path, "w+") as w:
            self.settings = w.read()
            w.close()
            self.settings = {}
            self.settings["guilds"] = {}
            await self.write_settings_file_to_disk()
    
    async def load_settings(self):
        with open(self.settings_file_path, "r") as r:
            self.settings = json.load(r)
            r.close()
        
    async def write_settings_file_to_disk(self):
        with open(self.settings_file_path, "w+") as w:
            json.dump(self.settings, w, indent=4)
            w.close()
            
    async def has_guild(self, guild_id):
        guild_id = str(guild_id)
        if self.settings["guilds"].get(guild_id) is not None:
            return True
        else:
            return False
        
    async def add_guild(self, guild_id):
        guild_id = str(guild_id)
        self.settings["guilds"][guild_id] = {}
        self.settings["guilds"][guild_id]["muted_role_id"] = 0
        self.settings["guilds"][guild_id]["log_channel_id"] = 0
        self.settings["guilds"][guild_id]["mod_roles"] = []
        self.settings["guilds"][guild_id]["muted_users"] = {}
        self.settings["guilds"][guild_id]["banned_users"] = {}
        await self.write_settings_file_to_disk()
        await self.load_settings()
