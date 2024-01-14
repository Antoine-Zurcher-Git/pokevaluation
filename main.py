from getCollectionData import *
from getPriceData import *
from collectionData import *
from pokedex import Pokedex
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from analyseValue import *

seriesNameSwitch = {
    "Promos Épée et Bouclier":"SWSH Black Star Promos",
    "Promos Écarlate et Violet":"SV Black Star Promos",
    "Promos Soleil et Lune":"SM Black Star Promos",
    "Promos X&Y":"XY Black Star Promos",
    "Promos Black Star Noir & Blanc":"BW Black Star Promos",
    "Promos Black Star HeartGold SoulSilver":"HGSS Black Star Promos",
    "Promos Black Star DP":"DP Black Star Promos",
    "Jumbo":"Tout",
    "SL Trainer Kit (Lougaroc)":"SM Kit du Dresseur: Lycanroc & Alolan Raichu",
    "SL Trainer Kit (Raichu d'Alola)":"SM Kit du Dresseur: Lycanroc & Alolan Raichu",
    "XY Trainer Kit (Pikachu Catcheur)":"XY Kit du Dresseur: Pikachu Libre & Suicune",
    "XY Trainer Kit (Suicune)":"XY Kit du Dresseur: Pikachu Libre & Suicune",
    "XY Trainer Kit (Nymphali)":"XY Kit du Dresseur",
    "XY Trainer Kit (Bruyverne)":"XY Kit du Dresseur",
    "B&W Trainer Kit (Zoroark)":"BW Kit du Dresseur",
    "B&W Trainer Kit (Minotaupe)":"BW Kit du Dresseur",
    "HS Trainer Kit (Léviator)":"HS Kit du Dresseur",
    "HS Trainer Kit (Raichu)":"HS Kit du Dresseur",
    "D&P Trainer Kit (Lucario)":"DP Kit Dresseur",
    "D&P Trainer Kit (Manaphy)":"DP Kit Dresseur",
    "Ex Trainer Kit 1 (Latios)":"EX Kit Dresseur",
    "Ex Trainer Kit 2 (Posipi)":"EX Kit Dresseur 2",
    "Ex Trainer Kit 2 (Negapi)":"EX Kit Dresseur 2",
    "Promo McDonald's 2018":"McDonald's Collection 2018 FR",
    "Promo McDonald's 2017":"McDonald's Collection 2017",
    "Promo McDonald's 2015":"McDonald's Collection 2015",
    "Promo McDonald's 2014":"McDonald's Collection 2014",
    "Promo McDonald's 2013":"McDonald's Collection 2013",
    "Promo McDonald's 2011":"McDonald's Collection 2011",
    "Topps":"Zacian + Zamazenta BOX",
    "Lamincards 2005":"Zacian + Zamazenta BOX",
    "Lamincards 2006":"Zacian + Zamazenta BOX",
    "Offensive Vapeur":"Steam Siege",
    "Impact des Destins":"Fates Collide",
    "Bienvenue à Kalos":"XY Kalos Starter Set",
    "Alliance Infaillible":"Unbroken Bonds",
    "Tonnerre Perdu":"Lost Thunder",
    "Duo de Choc":"Team Up"
}

englishSeriesRefs = {
    "Styles de Combat":"https://bulbapedia.bulbagarden.net/wiki/Battle_Styles_(TCG)", 
    "Voltage Éclatant":"https://bulbapedia.bulbagarden.net/wiki/Vivid_Voltage_(TCG)",
    "La Voie du Maître":"https://bulbapedia.bulbagarden.net/wiki/Champion%27s_Path_(TCG)",
    "Ténèbres Embrasées":"https://bulbapedia.bulbagarden.net/wiki/Darkness_Ablaze_(TCG)",
    "Clash des Rebelles":"https://bulbapedia.bulbagarden.net/wiki/Rebel_Clash_(TCG)",
    "Épée et Bouclier":"https://bulbapedia.bulbagarden.net/wiki/Sword_%26_Shield_(TCG)",
    "Éclipse Cosmique":"https://bulbapedia.bulbagarden.net/wiki/Cosmic_Eclipse_(TCG)",
    "Harmonie des Esprits":"https://bulbapedia.bulbagarden.net/wiki/Unified_Minds_(TCG)",
    "Alliance Infaillible":"https://bulbapedia.bulbagarden.net/wiki/Unbroken_Bonds_(TCG)",
    "Duo de Choc":"https://bulbapedia.bulbagarden.net/wiki/Team_Up_(TCG)",
    "Tonnerre Perdu":"https://bulbapedia.bulbagarden.net/wiki/Lost_Thunder_(TCG)",
    "Tempête Céleste":"https://bulbapedia.bulbagarden.net/wiki/Celestial_Storm_(TCG)",
    "Lumière Interdite":"https://bulbapedia.bulbagarden.net/wiki/Forbidden_Light_(TCG)",
    "Ultra-Prisme":"https://bulbapedia.bulbagarden.net/wiki/Ultra_Prism_(TCG)",
    "Invasion Carmin":"https://bulbapedia.bulbagarden.net/wiki/Crimson_Invasion_(TCG)",
    "Ombres Ardentes":"https://bulbapedia.bulbagarden.net/wiki/Burning_Shadows_(TCG)"
}

cardNameReplacements = [
    ["\u03b4 Espèces Delta","Delta"],
    ["Niv.X","Lv.X"]
]

errorLinkNotFoundName = "Error : Link Not Found"

def pokedexIntCardsForExg(pokedex: Pokedex, donneur: Collection, chercheur: Collection) -> List[Dict]:
    pokedexChercheur = {}
    for serie in chercheur.data:
        for card in serie.get("pkm_poss_info", []):
            findPkm, englElements = pokedex.getPokemonByFrName(card["name"])
            if findPkm == None:
                continue
            pokedexChercheur[findPkm["nom"]] = findPkm

    cardsExchangeabled: List[Dict] = []
    for serie in donneur.data:
        for card in serie.get("pkm_poss_info", []):
            findPkm, englElements = pokedex.getPokemonByFrName(card["name"])
            if findPkm == None:
                continue
            if findPkm["nom"] not in pokedexChercheur:
                theCard = card.copy()
                theCard["serie"] = serie["name"]
                cardsExchangeabled.append(card)
    
    return cardsExchangeabled

def collectionIntCardsForExg(donneur: Collection, chercheur: Collection):
    cardsChercheur = {}
    for serie in chercheur.data:
        for card in serie.get("pkm_poss_info", []):
            cardID = card["name"] + " " + card["numberRaw"]
            cardsChercheur[cardID]= card
    
    cardsExchangeabled: List[Dict] = []
    for serie in donneur.data:
        for card in serie.get("pkm_poss_info", []):
            cardID = card["name"] + " " + card["numberRaw"]
            if cardID not in cardsChercheur:
                theCard = card.copy()
                theCard["serie"] = serie["name"]
                cardsExchangeabled.append(card)

    return cardsExchangeabled

if __name__ == "__main__":
    parameters = {}
    try:
        with open('parameters.txt', 'r') as file:
            for line in file:
                lineSplit = line.strip().split("=")
                parameters[lineSplit[0].strip()] = lineSplit[1].strip()
    except FileNotFoundError:
        print("Error: Parameters File not found. Please make sure the file exists.")
        exit()
    except:
        print("Error with the parameters file")
        exit()


    ### ------ Parameters ------
    try:
        pokecardexNumber = parameters["pokecardex_number"]
    except:
        print("Missing parameters : pokecardex_number")
        exit()
    
    try:
        saveFilePath = parameters["collection_file_path"]
    except:
        saveFilePath = "collections/defaultCollectionName.json"
        print(f"Missing parameters : collection_file_path, default value : {saveFilePath}")

    try:
        savePokedexFilePath = parameters["pokedex_file_path"]
    except:
        savePokedexFilePath = "pokedex/pokedex.json"
        print(f"Missing parameters : pokedex_file_path, default value : {savePokedexFilePath}")

    try:
        getCollectionData = parameters["action_get_collection_data"].lower() == "true"
    except:
        getCollectionData = True
        print(f"Missing parameters : action_get_collection_data, default value : {getCollectionData}")
    
    try:
        searchPrice = parameters["action_search_price"].lower() == "true"
    except:
        searchPrice = False
        print(f"Missing parameters : action_search_price, default value : {searchPrice}")
    
    try:
        getAnalyse = parameters["action_get_analyse"].lower() == "true"
    except:
        getAnalyse = True
        print(f"Missing parameters : action_get_analyse, default value : {getAnalyse}")

    try:
        researchForLinkNotFound = parameters["action_research_for_link_not_found"].lower() == "true"
    except:
        researchForLinkNotFound = False
        print(f"Missing parameters : action_research_for_link_not_found, default value : {researchForLinkNotFound}")
    ### ------ Parameters ------


    data = None
    pokedex = None

    print("--- Start ---")

    if(getCollectionData or searchPrice or getAnalyse):
        print("---- Load collection ----")
        data = Collection(saveFilePath)

    if(searchPrice):
        print("---- Load pokedex ----")
        pokedex = Pokedex(savePokedexFilePath)

    if getCollectionData:
        print("---- Get Collection Data ----")
        urlMain = "https://www.pokecardex.com/collection/show/" + str(pokecardexNumber)
        urlSeries = "https://www.pokecardex.com/ajax/get_cartes_collection_grid/" + str(pokecardexNumber)

        # Handle Series Primary Data
        print("----- Get Series Primary Data -----")
        seriesPrimData = getWebsiteContent(urlMain)
        ne_series_info = processSeriesPrimData(seriesPrimData.text)
        data.updateSeriesPrimData(ne_series_info)

        # Prepare post request
        cookie = seriesPrimData.headers.get('Set-Cookie')
        csrf_test_name_value = findCsrfTestName(seriesPrimData.text)

        # Handle Series Card Data
        print("----- Get Series Card Data -----")
        getSeriesCardData(data, cookie, csrf_test_name_value, urlSeries)
        processSeriesCardData(data)
        data.removeSeriesRawData()
        data.updateCollection()

        # Synthese of the process
        nCards = 0
        seriesName = []
        seriesCpsName = ""
        for serie in data.data:
            nCards += len(serie["pkm_poss_info"])
            seriesName.append(serie["name"])
            seriesCpsName += serie["name"] + ", "
        if len(seriesCpsName) > 0:
            seriesCpsName = seriesCpsName[:-2] 
        print(f"The collection is composed of {nCards} cards in these {len(seriesName)} series :")
        print(seriesCpsName)
        print("---- Finished loading getting Collection Data")


    if searchPrice:
        print("---- Get Prices ----")

        # Verify if we still have card price data to search
        allCardsPricesFound = True
        allCardsPricesFoundBySeries = [True for serie in data.data]
        for iSerie, serie in enumerate(data.data):
            for card in serie["pkm_poss_info"]:
                if "prix_txt" not in card or (card["prix_txt"] == errorLinkNotFoundName and researchForLinkNotFound):
                    allCardsPricesFound = False
                    allCardsPricesFoundBySeries[iSerie] = False
                    break
        
        if not allCardsPricesFound:
            print("----- Setup Browser to search prices -----")
            driver = webdriver.Chrome()
            driver.implicitly_wait(0.5)
            driver.maximize_window()

            # Name and value of the series in the select on cardmarket site
            editionInfos = []

            for iSerie, serie in enumerate(data.data):
                # Don't search for price if already done
                if(allCardsPricesFoundBySeries[iSerie]):
                    continue

                # Don't search for price if no cards
                if len(serie.get("pkm_poss_info", [])) <= 0:
                    continue

                print("------ Get CardMarket Info of serie "+serie["name"]+" ------")

                loadCMInitialPage(driver)
                # We are on main page

                # Selection of the current serie
                selectSeriesBox = driver.find_element("name", "idExpansion")
                if len(editionInfos) <= 0:
                    getEditions( editionInfos, selectSeriesBox)
                editionTarget = getEditionInfo(editionInfos, seriesNameSwitch.get(serie["name"],serie["name"]))
                selectEdition = Select(selectSeriesBox)
                selectEdition.select_by_visible_text(editionTarget["name"])
                # Current serie selected

                for carte in serie["pkm_poss_info"]:
                    # Don't search for price if already has
                    if "prix_txt" in carte and (carte["prix_txt"] != errorLinkNotFoundName or not researchForLinkNotFound):
                        continue
                    
                    reasearchBox = driver.find_element("xpath", '//input[@name="searchString" and not(@id="ProductSearchInput")]')


                    cardName: str = carte["name"]

                    for repl in cardNameReplacements:
                        cardName = cardName.replace(repl[0], repl[1])
                    if editionTarget["name"] == "Tout":
                        cardName = carte["numberRaw"]
                    
                    # Test with French Name
                    print("------- Search Card in fr : " + cardName + " -------")
                    enterNameAndEnter(reasearchBox, cardName)
                    driver.implicitly_wait(5)
                    rndWait()
                    linkRep = getLinkInfo(driver, carte, cardName, carte["number"])
                    if linkRep == None:
                        englCarteName = pokedex.getEnglName(cardName)
                        if (englCarteName == None):
                            print("------- Engl Translation not found -------")
                            continue
                        print("------- Search Card in engl : " + englCarteName + " -------")
                        # Test with English Name
                        reasearchBox = driver.find_element("xpath", '//input[@name="searchString" and not(@id="ProductSearchInput")]')
                        enterNameAndEnter(reasearchBox, englCarteName)
                        driver.implicitly_wait(5)
                        rndWait()
                        linkRep = getLinkInfo(driver, carte, englCarteName, carte["number"], frName = cardName)
                        if linkRep == None:
                            carte["prix_txt"] = errorLinkNotFoundName

                    # Save the data gathered
                    data.updateCollection()

            driver.quit()
        else:
            print("----- All cards prices already known -----")
        print("---- Finished Getting Prices")

    if getAnalyse:
        report(data, errorLinkNotFoundName)

    print("--- Finish ---")


