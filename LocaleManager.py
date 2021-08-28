

class LocaleManager:
    locale = None
    
    def __init__(self, locale):
        """
        Locale is a dictionary of 'string name - translation' pairs
        """
        self.locale = locale
    
    def get(self, stringName):
        res = self.locale.get(stringName)
        if not res:
            return "Text not found: '%s'"%stringName
        return res
    
    def setLocale(self, locale):
        self.locale = locale


