from common.Authorization import *
from .Config import Config

class AuthorizationManager(AuthorizationManager):
    @staticmethod
    async def isAuthorized(ctx):
        """
        Checks if authorized based on ranks
        """
        for r in ctx.author.roles:
            if r.name == Config.AUTH_ROLE:
                return True
        raise NotAuthorized()