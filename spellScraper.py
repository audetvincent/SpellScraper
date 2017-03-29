#! python3
# spellScraper.py - Launches a browser to go fetch spells from the selected class and level.
#

import requests

webSitePath = 'https://dndtools.net/spells/'

res = requests.get(webSitePath)
