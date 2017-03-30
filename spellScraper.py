#! /usr/bin/env python
# spellScraper.py - Launches a browser to go fetch spells from the selected class and level.
#

import requests
import bs4
import lxml
import csv
import sys

LEVELS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
webSiteRoot = "https://dndtools.net"
webSitePath = webSiteRoot + "/spells/?rulebook__dnd_edition__slug=core-35&rulebook__dnd_edition__slug=supplementals-35&page_size=1000"
class_input = input("Please specified the class to fetch: ")
classSitePath = webSitePath + '&class_levels__slug=' + class_input
level_input = input("Now please specified every levels you wish to get the spells from (comma separated): ")

for e in level_input:
    if str(e) in LEVELS:
        levelSitePath = classSitePath +'&spellclasslevel__level=' + e
        _filename = class_input + '_level_' + e + '.csv'

        ofile = open(_filename, "w")
        writer = csv.writer(ofile, delimiter=' ')

        # 'https://dndtools.net/spells/?rulebook__dnd_edition__slug=core-35&rulebook__dnd_edition__slug=supplementals-35&class_levels__slug=druid&spellclasslevel__level=0&spellclasslevel__level=1'
        res = requests.get(levelSitePath)

        try:
            res.raise_for_status()
        except Exception as e:
            print('There was a problem : %s' %(e))

        spellSoup = bs4.BeautifulSoup(res.text, 'lxml')

        spellTable = spellSoup.select('.common')
        spellTableSoup = bs4.BeautifulSoup(str(spellTable), 'lxml')

        for row in spellTableSoup.find_all('tr'):
            _row = list()
            for column in row:
                if column.name == 'th':
                    if column.string:
                        _row.append(str(column.string))
                    for child in column.children:
                        if child.name == 'abbr':
                            _row.append(child.string)

                if column.name == 'td':
                    for child in column.children:
                        if child.name == 'a' and not _row:
                            spellLink = '=HYPERLINK("%s", "%s")' %(webSiteRoot+str(child['href']), str(child.string))
                            _row.append(spellLink)
                        elif child.name == 'a':
                            _row.append(str(child.string))
                        if child.name == 'img':
                            _row.append(child['alt'])

            if "Rulebook" in _row[8] or "Complete" in _row[8] or "Player" in _row[8] or "Races of Stone" in _row[8] \
                    or "Races of the Wild" in _row[8] or "Races of the Dragon" in _row[8]:
                writer.writerow(_row)
