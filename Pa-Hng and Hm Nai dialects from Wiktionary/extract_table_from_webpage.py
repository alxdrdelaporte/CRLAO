#!/usr/lib/python3.7
# -*-coding:utf-8 -*

"""
Alexander DELAPORTE - CRLAO
https://tekipaki.hypotheses.org/
https://github.com/alxdrdelaporte/CRLAO

Scraping a table from a Wiktionary Appendix web page

INPUT
https://en.wiktionary.org/wiki/Appendix:Pa-Hng_comparative_vocabulary_list
(last edited on 17 March 2020, at 06:10)
Wiktionary contents are available under the Creative Commons Attribution-ShareAlike License
https://creativecommons.org/licenses/by-sa/3.0/

OUTPUT
CSV file (separator = tab) with full data from the first table of the page
"""

# HTML parsing
from bs4 import BeautifulSoup as soup
# Web client
from urllib.request import urlopen as uReq
import urllib.request


def url_ok(url):
    """Function testing if URL can be accessed, parameter = URl string"""
    request = urllib.request.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        urllib.request.urlopen(request)
        return True
    except urllib.request.HTTPError:
        return False


def find_all_tables(url):
    """Function extracting all tables from a given webpage, parameter = URL string"""
    if url_ok(url):
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        tables = page_soup.find_all("table")
        return tables


def table_to_csv(table, output_file, delimiter="\t"):
    """
    Function extracting textual data from a HTML table, with tab as default delimiter,
    parameters = table as a BS4 object, output file path, delimiter (optional)
    """
    with open(output_file, "w") as output_file:
        # Table header from <th> cells
        header = ""
        th_set = table.find_all("th")
        for i in range(len(th_set)):
            th_data = th_set[i].text.rstrip('\n')
            if i == len(th_set) - 1:
                header += f"{th_data}\n"
            else:
                header += f"{th_data}{delimiter}"
        output_file.write(header)
        # Table data from <td> cells for each <tr> row
        tr_set = table.find_all("tr")
        for tr in tr_set:
            line = ""
            td_set = tr.find_all("td")
            for i in range(len(td_set)):
                td_data = td_set[i].text.rstrip('\n')
                if i == len(td_set) - 1:
                    line += f"{td_data}\n"
                else:
                    line += f"{td_data}{delimiter}"
            output_file.write(line)


page_url = 'https://en.wiktionary.org/wiki/Appendix:Pa-Hng_comparative_vocabulary_list'
# Extracting tables from the page
all_tables = find_all_tables(page_url)
# In this case, I only want data from the first table
table_to_extract = all_tables[0]
print(type(table_to_extract))
# Creating CSV file
csv_file = 'Pa-Hng_and_Hm_Nai_dialects.csv'
table_to_csv(table_to_extract, csv_file)
