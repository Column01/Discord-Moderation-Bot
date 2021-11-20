import inspect
import sys

from tasks.check_punishments import check_punishments

from events.base import EventHandler


class ReadyEvent(EventHandler):
    def __init__(self, client_instance):
        self.client = client_instance
        self.event = "on_ready"
    
    async def handle(self, *args, **kwargs):
        print(f"Logged in as {self.client.user}")
        # Start the storage management and setup the guilds we are connected to.
        await self.client.storage.init()

        # If you added the custom storage class from the developing guide, it would get initialized by this
        if hasattr(self.client, "config"):
            await self.client.config.init()

        for guild in self.client.guilds:
            await self.client.setup_guild(guild)
        # Register some tasks
        self.client.loop.create_task(check_punishments(self.client))


# Collects a list of classes in the file
classes = inspect.getmembers(sys.modules[__name__], lambda member: inspect.isclass(member) and member.__module__ == __name__)
