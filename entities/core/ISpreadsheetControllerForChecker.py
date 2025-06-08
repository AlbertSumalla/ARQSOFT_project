from ..core.SpreadsheetController import SpreadsheetController

class ISpreadsheetFactoryForChecker:
    @staticmethod
    def createSpreadsheetController():
        return SpreadsheetController()
