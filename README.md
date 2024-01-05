<!-- GETTING STARTED -->
## Getting Started

To execute this code, you first need python (it was made with version 3.9.0), and you also need to install the following librairies :

### Libraries

* selenium
```sh
  python -m pip install selenium
```

* requests
```sh
  python -m pip install requests
```

* beautifulsoup4
```sh
  python -m pip install beautifulsoup4
```



### Installation

```sh
git clone https://github.com/Antoine-Zurcher-Git/pokevaluation.git
```

### Execution
1. Setup parameters (ln 117-125 of main.py)
    * pokecardexNumber : Number of your pokecardex profil (ex : 012345)
    * saveFilePath : path to save the collection data file (ex : "collections/defaultCollectionName.json")
    * savePokedexFilePath : path to save the pokedex data file (ex : "pokedex/pokedex.json")
    * getCollectionData : True if you want to get the collection data from pokecardex
    * searchPrice : True if you want to gather the price data for a collection
    * getAnalyse : True if you want a recap of the collection data
    * researchForLinkNotFound : True if you want to research for prices that hasn't been found previously
2. Run :
```sh
python main.py
```


