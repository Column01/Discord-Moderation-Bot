import discord


class UnBanCommand:
    
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
    
    async def handle(self, message, command):
        await message.channel.send("Not implemented yet")
    

class TempBanCommand:
    
    def __init__(self, client_instance):
        self.client = client_instance
        self.storage = client_instance.storage
    
    async def handle(self, message, command):
        await message.channel.send("Not implemented yet")
