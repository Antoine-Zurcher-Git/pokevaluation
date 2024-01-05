from typing import List, Dict
from dataManager import DataManager
import os

class Collection(DataManager):
    """
    This class handles the infos of a collection of pokemon cards
    The collection data is either loaded from "filePath" or initialized empty

    The collection data is stored in self.data as a list of dictionaries with these keys:
        - name          : name of the serie. Ex : "Faille Paradoxe"
        - nb_cards      : number of cards possessed in the serie. Ex : 83
        - pkcardex_nb   : index of this serie in pokecardex. Ex : 214
        - pkm_poss_info : Array of dictionaries containing the info of the cards possessed. Dict keys :
                - name      : name of the card. Ex : "Feuillajou"
                - numberRaw : number of the card. Ex : "4/182"
                - number     : processed number of the card. Ex : "4"
                - prix_txt  : price of the card. Ex : "0,03 \u20ac" ("0,03 €")
    """

    def __init__(self, filePath: str):
        """
        Initialize the collection with
        filePath (str): file that (will) store the collection data. Ex : "myCollection.json"
        And load the data
        """
        super().__init__(filePath)
        self.data: List[Dict] = []
        self.filePath: str = filePath

        if os.path.exists(filePath):
            self.data = self.loadData(errorAdv = "collection")
        else:
            self.updateCollection()
    
    def updateCollection(self):
        """ Save self.data in filePath as a JSON """
        self.writeData(self.data, errorAdv = "collection")

    def removeSeriesRawData(self):
        """ Clean the raw data of the series """
        for serie in self.data:
            serie.pop("raw_data", None)

    def updateSeriesPrimData(self, primData):
        """ Add series to data """
        existingSeries = set(item["name"] for item in self.data)
        for newSerie in primData:
            if newSerie["name"] not in existingSeries:
                self.data.append(newSerie)
        self.updateCollection()

