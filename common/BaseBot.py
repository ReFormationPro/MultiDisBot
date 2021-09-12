class BaseBot():
    @staticmethod
    def initialize(bot):
        raise "Method is not overriden"

    @staticmethod
    async def on_guild_join(guild):
        raise "Method is not overriden"
    
    @staticmethod
    async def on_guild_remove(guild):
        raise "Method is not overriden"