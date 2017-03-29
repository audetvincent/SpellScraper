#! python
# spellScraper.py - Launches a browser to go fetch spells from the selected class and level.
#

import requests
import bs4
import sys

webSitePath = "https://dndtools.net/spells/?rulebook__dnd_edition__slug=core-35&rulebook__dnd_edition__slug=supplementals-35&page_size=1000"
class_input = raw_input("Please specified the class to fetch: ")
webSitePath += '&class_levels__slug=' + class_input
level_input = raw_input("Now please specified every levels you wish to get the spells from (comma separated): ")
for e in level_input:
    if e != ',':
        webSitePath += '&spellclasslevel__level=' + level_input

# 'https://dndtools.net/spells/?rulebook__dnd_edition__slug=core-35&rulebook__dnd_edition__slug=supplementals-35&class_levels__slug=druid&spellclasslevel__level=0&spellclasslevel__level=1'
res = requests.get(webSitePath)
print webSitePath

try:
    res.raise_for_status()
except Exception as e:
    print ('There was a problem : %s' %(e))

spellSoup = bs4.BeautifulSoup(res.text)

spellTable = spellSoup.select('.common')

for row in spellTable:
    print row.getText()
