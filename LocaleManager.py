from .TurkishLocale import TurkishLocale

class LocaleManager:
    locale = TurkishLocale
    
    def initialize(self, locale):
        """
        Locale is a dictionary of 'string name - translation' pairs
        """
        LocaleManager.locale = locale
    
    @staticmethod
    def get(stringName):
        res = LocaleManager.locale.get(stringName)
        if not res:
            return "Text not found: '%s'"%stringName
        return res
    
    @staticmethod
    def setLocale(locale):
        LocaleManager.locale = locale


