import os

from discord.ext import commands

from question_bot.QuestionBot import QuestionBot
from news_bot.NewsBot import NewsBot

Q_BOT_ACTIVE = False
N_BOT_ACTIVE = True

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_guild_join(guild):
    if Q_BOT_ACTIVE:
        await QuestionBot.on_guild_join(guild)
    if N_BOT_ACTIVE:
        await NewsBot.on_guild_join(guild)

@bot.event
async def on_guild_remove(guild):
    if Q_BOT_ACTIVE:
        await QuestionBot.on_guild_remove(guild)
    if N_BOT_ACTIVE:
        await NewsBot.on_guild_remove(guild)

if Q_BOT_ACTIVE:
    QuestionBot.initialize(bot)
if N_BOT_ACTIVE:
    NewsBot.initialize(bot)

bot.run(os.getenv('TOKEN'))