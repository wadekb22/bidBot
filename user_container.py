import Queue from queue
import datetime

class UserContainer:
    """Container for the user"""

    __calculatedRanking = -1        #Private internal calcuatedRanking
    __timeDropoff = 7               #Dropoff starts at one week
    __listing = Queue()

    def __init__(self, name):
        self.name = name

    def add_decision(self, value, reason):
        self.__listing.put([value, reason])
        self.__updateRank()
        return True

    def __updateRank():
        recompineVal
        curDate = datetime.uctnow()
