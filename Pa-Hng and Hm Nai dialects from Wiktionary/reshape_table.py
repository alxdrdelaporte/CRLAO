#!/usr/lib/python3.7
# -*-coding:utf-8 -*

"""
Alexander DELAPORTE - CRLAO
https://tekipaki.hypotheses.org/
https://github.com/alxdrdelaporte/CRLAO

Reshaping a table scrapped from Wiktionary page for Guillaume JACQUES's research project

INPUT
'Pa-Hng_and_Hm_Nai_dialects_FullTable.tsv' TSV file
Table extracted from https://en.wiktionary.org/wiki/Appendix:Pa-Hng_comparative_vocabulary_list
(last edited on 17 March 2020, at 06:10)
Wiktionary contents are available under the Creative Commons Attribution-ShareAlike License
https://creativecommons.org/licenses/by-sa/3.0/

OUTPUT
TSV file, one column for each language
"""

# CSV files processing
import csv


with open('Pa-Hng_and_Hm_Nai_dialects_FullTable.tsv', "r") as full_table, open('Pa-Hng_and_Hm_Nai_dialects.tsv', "w",
                                                                     encoding='utf8') as new_table:
    # Extracting data to set new table headers (= Chinese gloss + 1 column per language)
    languages = ['Chinese gloss']
    reader = csv.DictReader(full_table, delimiter='\t')
    for row in reader:
        language = row['Language (location)'].replace("]", "")
        if language not in languages:
            languages.append(language)
    full_table.seek(0)
    # Writing headers in output file
    writer = csv.DictWriter(new_table, fieldnames=languages, delimiter='\t')
    writer.writeheader()
    # Extracting data to fill table cells line by line
    glosses = []
    for row in reader:
        gloss = row['Chinese gloss']
        if gloss not in glosses and gloss != 'Chinese gloss':
            glosses.append(gloss)
    full_table.seek(0)
    # mini_dico dict = one line of data
    mini_dico = {}
    for gloss in glosses:
        mini_dico['Chinese gloss'] = gloss
        for row in reader:
            if row['Chinese gloss'] == gloss:
                lang = row['Language (location)'].replace("]", "")
                word = row["Word"]
                mini_dico[lang] = word
        writer.writerow(mini_dico)
        mini_dico = {}
        full_table.seek(0)
