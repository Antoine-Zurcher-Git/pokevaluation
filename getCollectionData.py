import requests
import re
from collectionData import Collection
from typing import Optional, List, Dict


def findCsrfTestName(html_content: str) -> str:    
    # Define the regex pattern to find "csrf_test_name" value
    pattern = re.compile(r'name="csrf_test_name" value="(.*?)"')

    # Search for the pattern in the HTML content
    match = pattern.search(html_content)

    # Check if a match is found
    if match:
        return match.group(1)
    else:
        return ""


def getWebsiteContent(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def getSerieWebData(csrf_test_name_value: str, id_: int, cookie: str, url: str):
    content_type = "application/x-www-form-urlencoded; charset=UTF-8"
    body = f'id={id_}&csrf_test_name={csrf_test_name_value}'
    headers = {"Content-Type": content_type, "Cookie": cookie}
    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=body)
        return response

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def processSeriesPrimData(seriesPrimData: str) -> List[Dict]:
    """
    Return the processed value for the serie. List of dict of keys :
        - name          : name of the serie. Ex : "Faille Paradoxe"
        - nb_cards      : number of cards possessed in the serie. Ex : 83
        - pkcardex_nb   : index of this serie in pokecardex. Ex : 214
    """

    # Get the series raw name
    element_ref = "<div class='nom_ext'>"
    series_i = [m.start() for m in re.finditer(element_ref, seriesPrimData)]
    series_names_nb = []
    for i in series_i:
        i_end = seriesPrimData[i:].find('</div>')
        series_names_nb.append(seriesPrimData[i+len(element_ref):(i+i_end)].strip())

    # Get the series name and number of cards
    series_infos = []
    for name in series_names_nb:
        number_raw = re.search("\(\d+\/\d+\)", name).group(0)
        ipar = number_raw.find('(')
        isla = number_raw.find('/')
        nb = int(number_raw[ipar+1:isla])
        i_end = name.find(number_raw)
        series_infos.append({"name": name[:i_end-1], "nb_cards": nb})

    # Get the series index for pokecardex
    element_ref = 'option" value='
    seriesi_i = [m.start() for m in re.finditer(element_ref, seriesPrimData)]
    for i,sei in enumerate(seriesi_i):
        i_end = seriesPrimData[sei:].find('">')
        series_infos[i]["pkcardex_nb"] = int(seriesPrimData[sei+len(element_ref)+1:(sei+i_end)])

    ne_series_info = [d for d in series_infos if d["nb_cards"] > 0]
    return ne_series_info


def getSeriesCardData(data: Collection, cookie: str, csrf_test_name_value: str, url: str):
    """
    Gather possessed cards data from all the series
    """

    for serie in data.data:
        info_response = getSerieWebData(csrf_test_name_value, serie["pkcardex_nb"], cookie, url)
        serie["raw_data"] = info_response.text


def __processSerieCardData(raw_data: Optional[str]):
    if raw_data is None:
        return None
    serieRes = []
    startEx = 'alt="'
    endEx = '" />'

    iStartAll = re.finditer('data-original="',raw_data)
    iStartAllPoss = re.finditer('alt="Normale" title=""', raw_data)
    iStartAll = [(m.start()) for m in iStartAll]
    iStartAllPoss = [(m.start()) for m in iStartAllPoss]
    for iStartPoss in iStartAllPoss:
        iStartInfo = 0
        for iStartInfoP in iStartAll:
            if iStartInfoP > iStartPoss:
                break
            iStartInfo = iStartInfoP
        
        iStartName = raw_data[iStartInfo:iStartInfo+200].find(startEx)
        iEndName = raw_data[iStartInfo+iStartName:iStartInfo+iStartName+100].find(endEx)
        info = raw_data[iStartInfo+iStartName+len(startEx):iStartInfo+iStartName+iEndName]
        
        numberRaw = re.search('(?:\\b\d+\/\d+\\b|\\b[a-zA-Z]+\d+|\\b\d+[a-zA-Z]\\b)(?!.*(?:\\b\d+\/\d+\\b|\\b[a-zA-Z]+\d+|\\b\d+[a-zA-Z]\b))', info).group(0)
        nameRawI = info.find(numberRaw)
        serieRes.append({"name":info[:nameRawI-1], "numberRaw":numberRaw, "number":numberRaw.split("/")[0]})
    return serieRes


def processSeriesCardData(data: Collection):
    for serie in data.data:
        pkmSerieInfo = (__processSerieCardData(serie.get("raw_data", None)))
        if pkmSerieInfo is not None:
            if "pkm_poss_info" not in serie:
                # First time we get this serie : we directly add the infos
                serie["pkm_poss_info"] = pkmSerieInfo
            else:
                oldNames = [oldCard["name"] for oldCard in serie["pkm_poss_info"]]
                newNames = [newCard["name"] for newCard in pkmSerieInfo]
                # The serie already exist
                # Remove the no more existing cards
                for oldCard in serie["pkm_poss_info"]:
                    if oldCard["name"] not in newNames:
                        serie["pkm_poss_info"].remove(oldCard)
                # Add new cards
                for newCard in pkmSerieInfo:
                    if newCard["name"] not in oldNames:
                        serie["pkm_poss_info"].append(newCard)
                nbCards = len(serie["pkm_poss_info"])
                serie["nb_cards"] = nbCards
                

