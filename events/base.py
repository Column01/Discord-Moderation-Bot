class EventHandler:
    def __init__(self, _):
        self.event = None

    def register_self(self):
        from event_registry import event_registry
        event_registry.register(self.event, self.__class__)

    def unregister_self(self):
        from event_registry import event_registry
        event_registry.unregister(self.event)

    async def execute(self, *args, **kwargs):
        pass
