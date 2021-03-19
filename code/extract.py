# création de requête
import requests

# manipulation du XML
import xmltodict

# création d'expression réguliaire
import re

# manipulation des dates
from datetime import datetime

# manipulation du HTLM et CSS
from bs4 import BeautifulSoup

# manipulation de dataframe
import pandas as pd

# manipulation du Json
import json
from bson import json_util

#
from utile import uniqueName, saveRawData

envPath = ""

# fonction de nettoyage pour les dates avec datetime
def cleaningDate(dateRaw):
    """
    >>> cleaningDate("Fri, 04 Dec 2020 08:22:51 +0100")
    datetime.datetime(2020, 12, 4, 8, 22, 51)
    >>> cleaningDate("bonjour")
    'bonjour'
    """

    try:
        dateClean = datetime.strptime(dateRaw[:-6], "%a, %d %b %Y %H:%M:%S")
        return dateClean
    except ValueError:

        return dateRaw


# fonction de nettoyage pour le titre du manga et le numéro du chapitre avec des regex
def cleanTitreAndNumber(titleNumberChapiterRaw):
    """
    >>> cleanTitreAndNumber('Scan - Jujutsu Kaisen Chapitre 132')
    ('Jujutsu Kaisen', 132)
    """
    if titleNumberChapiterRaw:
        number = re.findall("\d{3,}", titleNumberChapiterRaw)[-1]
        title = titleNumberChapiterRaw.replace("Scan - ", "").replace(
            f" Chapitre {number}", ""
        )
        return title, int(number)


# Function to clean the title
def cleaningChapiterTitle(chapiterTitleRaw):
    """
    return the chapiter's title
    """
    soup = BeautifulSoup(chapiterTitleRaw, "html.parser")
    title = soup.findAll("a")[-1].string

    return title


def myextract():
    # request to retrieve raw data
    url = "https://scantrad.net/rss/"
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    # save raw data
    saveRawData(data)

    # extract
    mangasRawList = data["rss"]["channel"]["item"]

    dataCleanJson = []
    for mangaRow in mangasRawList:
        # cleanning
        mangaTitle, chapiterNumber = cleanTitreAndNumber(mangaRow["title"])
        link = mangaRow["link"]
        chapTitle = cleaningChapiterTitle(mangaRow["description"])
        chapDate = cleaningDate(mangaRow["pubDate"])

        # add
        dataCleanJson.append(
            {
                "mangaTitle": mangaTitle,
                "chapiterNumber": chapiterNumber,
                "chapTitle": chapTitle,
                "link": link,
                "chapDate": chapDate,
            }
        )

    # sauvegarde des données au format JSON
    with open(f"{envPath}data/json/{uniqueName('json')}", "w") as f:
        json.dump(dataCleanJson, f, default=json_util.default)


if __name__ == "__main__":
    myextract()
