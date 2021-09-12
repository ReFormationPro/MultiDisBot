
class BaseCommandManager():
    # TODO Must every subclass redeclare this?
    bot = None
    # Add defined commands here
    COMMANDS = []

    @classmethod
    def initialize(cls, bot):
        cls.bot = bot
        for cmd in cls.COMMANDS:
            bot.add_command(cmd)
    
    @classmethod
    def getCommand(cls, cmdName):
        for cmd in cls.COMMANDS:
            # TODO Get names from active locale
            if cmd.__name__ == cmdName:
                return cmd
    
    @classmethod
    def getCmdHelp(cls, cmdName):
        raise "Method is not overriden"
    
    @staticmethod
    def getGuildName(ctx):
        if ctx.guild:
            return ctx.guild.name
        else:
            return None

    @staticmethod
    def getChannelName(ctx):
        # TODO Handle DMChannel
        return ctx.channel.name