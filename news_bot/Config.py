from common.LocaleManager import LocaleManager

from .Locales.TurkishLocale import TurkishLocale

class Config:
    ALARMS_TABLE = "Alarms"
    localeManager = LocaleManager(TurkishLocale)
    AUTH_ROLE = "NewsBotManager" # Role name for commanding the bot