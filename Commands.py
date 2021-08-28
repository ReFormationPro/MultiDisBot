from LocaleManager import LocaleManager
from ReplitDatabase import ReplitDatabaseManager
from Session import Session, SessionManager

import re
from random import randint

class CommandManager:
    cmdList = []
    prefix = "!"

    @staticmethod
    def findCommandByName(cmdName):
        for cmd in CommandManager.cmdList:
            if cmd.cmdName == cmdName:
                return cmd

    @staticmethod
    def parseAndExec(str):
        if str[0] != CommandManager.prefix:
            return None
        l = len(CommandManager.prefix)
        idx = str.find(" ")
        if idx == -1:
            # set to len(str)
            idx = len(str)
        cmdName = str[l:idx]
        cmd = CommandManager.findCommandByName(cmdName)
        if cmd != None:
            return cmd.exec(str[idx+1:])

class ArgumentParser:
    """
    string: argument+
    argument: '"[^"]+"' | "'[^']+'" | '[a-zA-Z0-9]+'
    """

    @staticmethod
    def parse(string):
        pass

class Command:
    cmdName = ""
    argumentMatcher = '"(.+?)" +"(.+?)" *'
    QUESTION_TABLE = "Questions"
    
    def __init__(self, cmdName):
        self.cmdName = cmdName
    
    def help(self):
        return LocaleManager.get(self.cmdName)
    
    def exec(self, argStr):
        raise Error("Not implemented")


class HelpCommand(Command):
    def __init__(self):
        Command.__init__(self, "help")
        #Command.cmdList.append(self)
    
    def exec(self, argStr):
        print("Help: '" + argStr + "'")
        args = ArgumentParser.parse(argStr)
        if len(args) == 0:
            # Print general help message
            helpStr = LocaleManager.get("HelpCmdPretext") + "\n"
            for cmd in CommandManager.cmdList:
                helpStr += cmd.help() + "\n"
            return helpStr
        else:
            # Discard the rest of the arguments
            cmd = CommandManager.findCommandByName(args[0])
            if cmd != None:
                return cmd.help()
            else:
                return "%s: %s"%(LocaleManager.get("CmdNotFound"), cmd.cmdName)

class AddCommand(Command):
    def __init__(self):
        Command.__init__(self, "add")
        #Command.cmdList.append(self)
    
    def exec(self, argStr):
        """
        Takes two arguments
        First is the question, second is the answer
        Returns True if successful
        Otherwise False or error string
        """
        args = ArgumentParser.parse(argStr)
        if len(arg) != 2:
            return LocaleManager.get("AddCmdWrongArgumentCount")
        return DatabaseManager.add(Command.QUESTION_TABLE, args[0], args[1])

class RemoveCommand(Command):
    def __init__(self):
        Command.__init__(self, "remove")
        #Command.cmdList.append(self)
    
    def exec(self, argStr):
        """
        Takes one argument, index of question
        Returns True if successful
        Otherwise False or error string
        """
        args = ArgumentParser.parse(argStr)
        if len(arg) == 0:
            # Needs to take more
            return LocaleManager.get("RemoveCmdWrongArgumentCount")
        try:
            args = tuple(int(x) for x in args)
        except ValueError as ex:
            return LocaleManager.get("RemoveCmdWrongArgumentType")
        return DatabaseManager.removeAll(Command.QUESTION_TABLE, args)

class ListCommand(Command):
    def __init__(self):
        Command.__init__(self, "list")
        #Command.cmdList.append(self)
    
    def exec(self, argStr):
        """
        Takes no arguments, lists all questions
        TODO List by category
        """
        questions = DatabaseManager.list(Command.QUESTION_TABLE)
        s = LocaleManager.get("ListCmdPretext")
        for question in questions:
            s += "\n%i: %s"%(question["index"], question["text"])
        return s


class AnswerCommand(Command):
    def __init__(self):
        Command.__init__(self, "answer")
        #Command.cmdList.append(self)
    
    def exec(self, argStr):
        """
        Takes one argument, the answer to the question that was asked before
        """
        comparable = Session.makeComparable(argStr)
        result = SessionManager.suggestAnswer(comparable)
        if result:
            # If the right answer
            return LocaleManager.get("AnswerCmdCorrect")
        else:
            # Print nothing
            return False

class AskCommand(Command):
    def __init__(self):
        Command.__init__(self, "ask")
        #Command.cmdList.append(self)
    
    def exec(self, argStr):
        """
        Takes no arguments, asks a random question
        TODO Do not pick from asked questions, select by category
        """
        qCount = DatabaseManager.count(Command.QUESTION_TABLE)
        if qCount:
            return LocaleManager.get("AskCmdNoQuestionFound")
        idx = randint(0, qCount-1)
        question = DatabaseManager.getIdx(Command.QUESTION_TABLE, idx)
        # Start question session
        SessionManager.startSession(Session(question["answer"]))
        return "%s:\n%s"%(LocaleManager.get("AskCmdPretext"), question["text"])

CommandManager.cmdList = [
    AskCommand(),
    AnswerCommand(),
    ListCommand(),
    RemoveCommand(),
    AddCommand(),
    HelpCommand()
]

"""
for entry in dir():
    if entry == "Command":
        continue
    if entry[-7:] == "Command":
        CommandManager.cmdList.append()
"""


