from difflib import SequenceMatcher
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import uniform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict

def rndWait(coeff = 1):
    sleep(3*coeff*uniform(0.3, 0.7))

def getEditionInfo(editionInfos: List[Dict],editionName: str):
    """
    On cardmarket, which serie to select ?

    Parameters :
        editionInfos : List of the series in cardmarket, dictionary of keys :
            - name : name of the serie
            - value : value link to the serie in the select
        editionName : Name of the serie that we want to select
    
    Return the element of editionInfos for which the name is the closest to editionName
    """
    result = max(editionInfos, key=lambda d: SequenceMatcher(None, editionName, d['name']).ratio())
    if SequenceMatcher(None, editionName, result["name"]).ratio() < 0.7:
        raise Exception(f"Error, serie {editionName} not found on cardmarket")
    return result

def getBestLink(links: List[WebElement], ref: str):
    """
    Parameters : 
        - ref (str) : Name of the card that we search
        - links (List[WebElement]) : list of the links found for this card

    Return the closest link to the name gaved
    """
    best = links[0]
    maxV = 0
    for link in links:
        if len(link.text) <= 0:
            continue
        value = SequenceMatcher(None, ref, link.text).ratio()
        if value > maxV:
            best = link
            maxV = value
    if maxV < 0.59:
        print(f"-------- {ref} not found, max similarity : {maxV} with {best.text}--------")
        return None
    return best


def loadCMInitialPage(driver: WebDriver):
    driver.get("https://www.cardmarket.com/fr/Pokemon/Products/Singles")
    driver.implicitly_wait(1.2)
    try:
        driver.find_element("xpath", "//*[contains(text(), 'Accepter tous les cookies')]").click()
    except:
        pass
    driver.implicitly_wait(0.6)

def getEditions(editionList, select_box):
    editionOptionsElms = [x for x in select_box.find_elements("tag name","option")]
    for edElm in editionOptionsElms:
        editionList.append({"name":edElm.text, "value":edElm.get_attribute("value")})

def enterNameAndEnter(textBox, name):
    textBox.send_keys(Keys.LEFT_CONTROL + "a")
    rndWait()
    textBox.send_keys(Keys.DELETE)
    rndWait()
    textBox.send_keys(name)
    rndWait()
    textBox.send_keys(Keys.ENTER)

def getLinkInfo(driver: WebDriver, carte: Dict, name: str, number: str, frName = ""):
    linksFound = driver.find_elements("xpath", '//div[@class="table-body"]//a')
    
    # No pertinent link found
    if len(linksFound) <= 0 or sum([len(l.text) for l in linksFound]) <= 0:
        return None
    
    bestLink = getBestLink(linksFound, name + " " + number)
    
    # In case there is not bestLink
    if bestLink == None:
        if len(frName) > 0:
            bestLink = getBestLink(linksFound, frName + " " + number)
            if bestLink == None:
                return None
        else:
            return None
    
    # Click on the link
    driver.execute_script("arguments[0].scrollIntoView();", bestLink)
    rndWait()
    driver.execute_script("arguments[0].click();", bestLink)
    driver.implicitly_wait(5)
    # We are on the card page

    # Get the price data
    elementPrix = driver.find_element("xpath",'//dt[text()="Prix moyen 30 jours"]/following-sibling::dd')
    carte["prix_txt"] = elementPrix.text

    rndWait(coeff=2)
    driver.back()
    return 1
    # Back to the research page

if __name__=="__main__":
    a = SequenceMatcher(None, "Lixy 3", "Lixy (PAL 003)").ratio()
    print(a)