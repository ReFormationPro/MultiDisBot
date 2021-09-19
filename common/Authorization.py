from discord.ext import commands

class NotAuthorized(commands.CheckFailure):
    pass

class AuthorizationManager:
    @staticmethod
    async def isAuthorized(ctx):
        """
        Checks if authorized

        Override this method to implement your own authorization
        """
        return True