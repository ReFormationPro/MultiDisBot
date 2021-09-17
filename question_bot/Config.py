from common.LocaleManager import LocaleManager

from .Locales.TurkishLocale import TurkishLocale

class Config:
    QUESTION_TABLE = "Questions"
    SESSION_TABLE = "Sessions"
    localeManager = LocaleManager(TurkishLocale)