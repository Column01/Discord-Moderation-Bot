from bot import ModerationBot


class EventHandler:
    def __init__(self, _: ModerationBot) -> None:
        self.event = None

    def register_self(self) -> None:
        from event_registry import event_registry
        event_registry.register(self.event, self.__class__)

    def unregister_self(self) -> None:
        from event_registry import event_registry
        event_registry.unregister(self.event)

    async def handle(self, *args, **kwargs) -> None:
        pass
