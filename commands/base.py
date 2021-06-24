class Command:
    def __init__(self, _):
        self.cmd = None

    def register_self(self):
        from command_registry import registry
        registry.register(self.cmd, self.__class__)

    def unregister_self(self):
        from command_registry import registry
        registry.unregister(self.cmd)

    async def execute(self, *args, **kwargs):
        pass
