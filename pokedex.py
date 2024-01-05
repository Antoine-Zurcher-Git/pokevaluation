import os
import requests
from bs4 import BeautifulSoup
from typing import Union
from unidecode import unidecode
from typing import List, Dict
from dataManager import DataManager

class Pokedex(DataManager):
    """
    This class handles the pokedex infos (english & french) 
    The pokedex data is loaded either from "filePath" or from
    https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_dans_l%27ordre_du_Pok%C3%A9dex_National

    The pokedex data is stored in self.data as a list of dictionaries with these keys :
        - nb : pokedex number of the pokemon
        - nom : french name of the pokemon
        - name : english name of the pokemon
    """

    nameRestrictions: List[str] = ["Forme ", "Temps ", "Motif ", "Aspect ", "Fleur ", "Taille ",
        "Mode ", "Style ", "Type ", "Lait ", "Tête ", "Mâle ", "Femelle ",
        "Héros ", "Épée ", "Famille ", "Plumage ", "Masque ", "Cape ", "50% "
        ]
    
    nameReplacements: Dict[str, str] = {"\u2642":" M", "\u2640":" F"}

    nameParticleTranslation: List[Dict] = [
        {"frPart":"-V", "enPart":" V","frPlace":-1,"enPlace":-1},
        {"frPart":"-VSTAR", "enPart":" VSTAR","frPlace":-1,"enPlace":-1},
        {"frPart":" ex", "enPart":" ex","frPlace":-1,"enPlace":-1},
        {"frPart":" Lv.X", "enPart":" Lv.X","frPlace":-1,"enPlace":-1},
        {"frPart":" Delta", "enPart":" Delta","frPlace":-1,"enPlace":-1},
        {"frPart":" de Team Magma", "enPart":"Team Magma's ","frPlace":-1,"enPlace":1},
        {"frPart":" de Team Aqua", "enPart":"Team Aqua's ","frPlace":-1,"enPlace":1},
        {"frPart":" d'Alola", "enPart":"Alolan ","frPlace":-1,"enPlace":1},
        {"frPart":" de Galar", "enPart":"Galarian ","frPlace":-1,"enPlace":1},
        {"frPart":" de Hisui", "enPart":"Hisuian ","frPlace":-1,"enPlace":1},
    ]

    def __init__(self, filePath: str):
        """
        Initialize the pokedex with
        filePath (str): file that (will) store the pokedex data. Ex : "pokedex.json"
        And load the data
        """
        super().__init__(filePath)
        self.data: List[Dict] = []
        self.filePath: str = filePath
        
        if os.path.exists(filePath):
            self.data = self.loadData(errorAdv = "pokedex")
        else:
            self.data = self.getOnlinePokedex()
            self.writeData(self.data, errorAdv = "pokedex")
    
    def __clearName(self, name: str) -> str:
        """
        Clear the raw pokemon name.
        Remove the name restrictions and remove fused phrases
        
        Parameters :
            name (str) : raw name of the pokemon

        Returns :
            str : cleared name
        """
        result:str = name
        # Clear from restrictions
        for rest in self.nameRestrictions:
            if rest in result:
                istart = result.find(rest)
                result = result[:istart]

        # Clear from fused phrases
        if " " in result:
            indexUp = -1
            for ic in range(1,len(result)):
                if(result[ic-1] not in [" ", "-", ".","_"] and result[ic].isupper()):
                    indexUp = ic
            if indexUp > 0:
                result = result[:indexUp]
        
        # Replacements
        for repl in self.nameReplacements:
            result = result.replace(repl, self.nameReplacements[repl])

        return result


    def getOnlinePokedex(self) -> List[Dict]:
        """
        Load data from internet to get pokedex infos

        Returns :
            dict : pokedex gathered online with keys :
                - nb : pokedex number of the pokemon
                - nom : french name of the pokemon
                - name : english name of the pokemon
        """

        responseTxt: str = requests.get("https://www.pokepedia.fr/Liste_des_Pok%C3%A9mon_dans_l%27ordre_du_Pok%C3%A9dex_National").text
        
        # Process the data into an array 
        soup = BeautifulSoup(responseTxt, 'html.parser')
        table_rows = soup.find_all('tr')
        table_data = []
        for row in table_rows[8:-11]:
            cells = row.find_all('td')[:4]
            row_data = [cell.get_text(strip=True) for cell in cells]
            table_data.append(row_data)
        encoded_data = [[cell.encode('utf-8').decode('utf-8') for cell in row] for row in table_data]

        # Construct the pokedex
        pokedex: List[Dict] = []
        for row in encoded_data:
            if len(row[0]) < 1:
                continue
            dico = {}
            dico["nb"] = int(row[0])
            dico["nom"] = self.__clearName(row[2])
            dico["name"] = self.__clearName(row[3])
            pokedex.append(dico)

        return pokedex

    def uniName(self, name: str) -> str:
        return unidecode(name.lower())

    def getEnglName(self, nom: str) -> Union[str, None]:
        """
        Translate the french pokemon name into english

        Returns :
            str : english name
            None : if no translation has been found
        """
        
        findPkm, englElements = self.getPokemonByFrName(nom)
        if findPkm == None:
            return findPkm
        englName = findPkm["name"]
        for rmvElm in range(len(englElements)):
            elm = englElements.pop()
            if(elm["enPlace"] < 0):
                englName += elm["enPart"]
            else:
                englName = elm["enPart"] + englName

        return englName
    
    def getPokemonByFrName(self, name: str):
        refName = self.uniName(name)

        elementChanged = True
        englElements = []
        while(elementChanged):
            elementChanged = False
            for partTransl in self.nameParticleTranslation:
                frPart = self.uniName(partTransl["frPart"])
                idxSearchStart = 0
                idxSearchEnd = len(refName)
                if(partTransl["frPlace"] < 0):
                    idxSearchStart = len(refName)-len(frPart)
                if(partTransl["frPlace"] > 0):
                    idxSearchEnd = len(frPart)
                idxStart = refName.find(frPart, idxSearchStart, idxSearchEnd)
                if(idxStart >= 0 and refName[idxStart:idxStart+len(frPart)] == frPart):
                    englElements.append(partTransl)
                    refName = refName[:idxStart] + refName[idxStart+len(frPart):]
                    elementChanged = True

        findPkm = None
        for pkm in self.data:
            testedName = self.uniName(pkm["nom"])
            if(refName == testedName):
                findPkm = pkm
                break

        return findPkm, englElements



if __name__ == "__main__":
    pokedex = Pokedex("pokVision/pokedex.json")
    # print(pokedex.getEnglName("Élecsprint"))
    # print(pokedex.getEnglName("Insecateur-Vtype"))
    # print(pokedex.getEnglName("Élecsprint d'Alola"))
    # print(pokedex.getEnglName("Élecsprint ex"))
    # print(pokedex.getEnglName("Élecsprint Lv.X"))
    # print(pokedex.getEnglName("Élecsprint-V"))
    # print(pokedex.getEnglName("Élecsprint-VSTAR"))
    # print(pokedex.getEnglName("Élecsprint Delta"))
    # print(pokedex.getEnglName("Élecsprint de Team Aqua"))
    # print(pokedex.getEnglName("Élecsprint de Team Magma"))
    # print(pokedex.getEnglName("Delta Élecsprint de Team Magma"))
    # print(pokedex.getEnglName("Élecsprint de Team Magma d'Alola"))
    # print(pokedex.getEnglName("Élecsprint d'Alola de Team Magma"))
    # print(pokedex.getEnglName("Mélofée exemple"))
