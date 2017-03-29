#! python
# spellScraper.py - Launches a browser to go fetch spells from the selected class and level.
#

import requests
import bs4
import lxml
import csv
import sys

webSitePath = "https://dndtools.net/spells/?rulebook__dnd_edition__slug=core-35&rulebook__dnd_edition__slug=supplementals-35&page_size=1000"
class_input = raw_input("Please specified the class to fetch: ")
webSitePath += '&class_levels__slug=' + class_input
level_input = raw_input("Now please specified every levels you wish to get the spells from (comma separated): ")

_filename = class_input + '_level_'

for e in level_input:
    if e != ',':
        webSitePath += '&spellclasslevel_level=' + level_input
        _filename += '_'+level_input

_filename += '.csv'


ofile = open(_filename, "wb")
writer = csv.writer(ofile, delimiter=' ',quotechar='|',quoting=csv.QUOTE_MINIMAL)

# 'https://dndtools.net/spells/?rulebook__dnd_edition__slug=core-35&rulebook__dnd_edition__slug=supplementals-35&class_levels__slug=druid&spellclasslevel__level=0&spellclasslevel__level=1'
res = requests.get(webSitePath)

try:
    res.raise_for_status()
except Exception as e:
    print ('There was a problem : %s' %(e))

spellSoup = bs4.BeautifulSoup(res.text, 'lxml')

spellTable = spellSoup.select('.common')
spellTableSoup = bs4.BeautifulSoup(str(spellTable))

_array = []

for row in spellTableSoup.find_all('tr'):
    _row = list()
    for column in row:
        if column.name == 'th':
            print(column.string)
            writer.writerow()
        elif column.name == 'td':
            _row.append(str(column.string))
    if len(_row) > 0:
        _array.append(_row)

print(_array)
# rows = spellTableSoup.select("tr")
# spellTableSoup.chi
# for row in rows:
#    rowSoup = bs4.BeautifulSoup(str(row))
#    if rowSoup.

#for row in spellTable:
#    print row.getText()
