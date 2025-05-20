from database.DAO import DAO

class Model:
    def __init__(self):
        pass
    def getYears(self):
        return DAO.getYears()

    def getCountry(self):
        return DAO.getCountry()
