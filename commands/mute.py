import discord


class UnMuteCommand:
    
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
    
    async def handle(self, message, command):
        await message.channel.send("Not implemented yet")
    
    
class MuteCommand:
    
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
    
    async def handle(self, message, command):
        await message.channel.send("Not implemented yet")
    
    
class TempMuteCommand:
    
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
    
    async def handle(self, message, command):
        await message.channel.send("Not implemented yet")