class Command:
    def __init__(self, _):
        self.cmd = None

    def register_self(self):
        from command_registry import registry
        if isinstance(self.cmd, list):
            for cmd in self.cmd:
                registry.register(cmd, self.__class__)
        elif isinstance(self.cmd, str):
            registry.register(self.cmd, self.__class__)
        else:
            raise ValueError(f"self.cmd must be of type list[str] or str!. Found type: {type(self.cmd)}")

    def unregister_self(self):
        from command_registry import registry
        if isinstance(self.cmd, list):
            for cmd in self.cmd:
                registry.unregister(cmd, self.__class__)
        elif isinstance(self.cmd, str):
            registry.unregister(self.cmd, self.__class__)
        else:
            raise ValueError(f"self.cmd must be of type list[str] or str!. Found type: {type(self.cmd)}")

    async def execute(self, *args, **kwargs):
        pass
