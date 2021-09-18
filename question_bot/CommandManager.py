from random import randint

from discord.ext import commands

from common.LocaleManager import LocaleManager
from common.BaseCommandManager import BaseCommandManager
from database.ReplitDatabase import ReplitDatabaseManager as RDM

from .Session import Session, SessionManager
from .Config import Config

def makeQuestion(question, answer):
    return {"text": question, "answer": answer}

def getGuildName(ctx):
    if ctx.guild:
        return ctx.guild.name
    else:
        return None

def getChannelName(ctx):
    # TODO Handle DMChannel
    return ctx.channel.name

@commands.command()
async def helpme(ctx, cmdName="help"):
    help = None
    if cmdName == "help":
        # Print general help message
        help = LocaleManager.get("HelpCmdPretext") + "\n"
        for cmd in CommandManager.COMMANDS:
            cmdHelp = CommandManager.getCmdHelp(cmd.__name__)
            if cmdHelp:
                help += cmdHelp + "\n"
            else:
                help += "%s: %s"%(LocaleManager.get("CmdNotFound"), cmd.__name__)
    else:
        help = CommandManager.getCmdHelp(cmdName)
        if help == None:
            help = "%s: %s"%(LocaleManager.get("CmdNotFound"), cmdName)
    await ctx.send(help)

@commands.command()
async def add(ctx, questionText, answerText):
    """
    Returns True if successful
    Otherwise False or error string
    """
    # TODO Handle this better
    if questionText == "" or answerText == "":
        message = LocaleManager.get("AddCmdWrongArgumentCount")
        await ctx.send(message)
        return
    server = getGuildName(ctx)
    RDM.add(server, Config.QUESTION_TABLE, 
      makeQuestion(questionText, answerText))

@commands.command()
async def remove(ctx, *qIdx):
    """
    qIdx is the list of the indexes of the questions
    Returns True if successful
    Otherwise False or error string
    """
    try:
        qIdx = tuple(int(x) for x in qIdx)
    except ValueError as ex:
        await ctx.send(LocaleManager.get("RemoveCmdWrongArgumentType"))
        return
    RDM.removeAll(
        getGuildName(ctx), Config.QUESTION_TABLE, qIdx)

@commands.command()
async def list(ctx):
    """
    Lists all questions
    TODO List by category
    """
    questions = RDM.list(
        getGuildName(ctx), Config.QUESTION_TABLE)
    s = LocaleManager.get("ListCmdPretext")
    for i, question in questions.items():
        s += "\n%s: %s"%(i, question["text"])
    await ctx.send(s)

@commands.command()
async def answer(ctx, answer):
    """
    Takes one argument, the answer to the question that was asked before
    """
    server = getGuildName(ctx)
    channel = getChannelName(ctx)
    comparable = Session.makeComparable(answer)
    result = SessionManager.suggestAnswer(server, channel, comparable)
    if result == None:
        await ctx.send(LocaleManager.get("AnswerCmdNoSession"))
    elif result:
        # If the right answer
        await ctx.send(LocaleManager.get("AnswerCmdCorrect"))
    else:
        await ctx.send(LocaleManager.get("AnswerCmdIncorrect"))

@commands.command()
async def ask(ctx):
    """
    Asks a random question
    TODO Do not pick from asked questions, select by category
    """
    server = getGuildName(ctx)
    channel = getChannelName(ctx)
    qCount = RDM.count(server, Config.QUESTION_TABLE)
    if qCount == 0:
        await ctx.send(LocaleManager.get("AskCmdNoQuestionFound"))
        return
    idx = randint(0, qCount-1)
    question = RDM.getAtIdx(server, Config.QUESTION_TABLE, idx)
    # Start question session
    SessionManager.startSession(server, channel, 
        Session(channel, question["answer"]))
    await ctx.send("%s:\n%s"%(LocaleManager.get("AskCmdPretext"), 
        question["text"]))

class CommandManager(BaseCommandManager):
    bot = None
    # Every command defined above
    COMMANDS = [helpme, add, remove, list, answer, ask]
    
    @classmethod
    def getCmdHelp(cls, cmdName):
        return LocaleManager.get(cmdName)