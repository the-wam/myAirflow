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
from utile import unique_name, save_raw_data

envPath = ""

# fonction de nettoyage pour les dates avec datetime
def cleaning_date(date_raw):
    """
    >>> cleaningDate("Fri, 04 Dec 2020 08:22:51 +0100")
    datetime.datetime(2020, 12, 4, 8, 22, 51)
    >>> cleaningDate("bonjour")
    'bonjour'
    """

    try:
        date_clean = datetime.strptime(date_raw[:-6], "%a, %d %b %Y %H:%M:%S")
        return date_clean
    except ValueError:

        return date_raw


# fonction de nettoyage pour le titre du manga et le numéro du chapitre avec des regex
def clean_titre_and_number(titlen_number_chapiter_raw):
    """
    >>> cleanTitreAndNumber('Scan - Jujutsu Kaisen Chapitre 132')
    ('Jujutsu Kaisen', 132)
    """
    if titlen_number_chapiter_raw:
        number = re.findall("\d{3,}", titlen_number_chapiter_raw)[-1]
        title = titlen_number_chapiter_raw.replace("Scan - ", "").replace(
            f" Chapitre {number}", ""
        )
        return title, int(number)


# Function to clean the title
def cleaning_chapiter_title(chapiter_title_raw):
    """
    return the chapiter's title
    """
    soup = BeautifulSoup(chapiter_title_raw, "html.parser")
    title = soup.findAll("a")[-1].string

    return title


def my_extract():
    # request to retrieve raw data
    url = "https://scantrad.net/rss/"
    response = requests.get(url)
    data = xmltodict.parse(response.content)

    # save raw data
    save_raw_data(data)

    # extract
    mangas_raw_list = data["rss"]["channel"]["item"]

    data_clean_json = []
    for manga_row in mangas_raw_list:
        # cleanning
        manga_title, chapiter_number = clean_titre_and_number(manga_row["title"])
        link = manga_row["link"]
        chap_title = cleaning_chapiter_title(manga_row["description"])
        chap_date = cleaning_date(manga_row["pubDate"])

        # add
        data_clean_json.append(
            {
                "mangaTitle": manga_title,
                "chapiterNumber": chapiter_number,
                "chapTitle": chap_title,
                "link": link,
                "chapDate": chap_date,
            }
        )

    # sauvegarde des données au format JSON
    with open(f"{envPath}data/json/{unique_name('json')}", "w") as f:
        json.dump(data_clean_json, f, default=json_util.default)


if __name__ == "__main__":
    my_extract()
