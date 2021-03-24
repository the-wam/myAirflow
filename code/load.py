import os

import json

import pymongo
from pymongo import MongoClient

import glob
import traceback

from utile import load_json

env_path = ""
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client.test_database
    collection = db.test_collection
    collection.find_one()
    manga = db.manga
    print("connection OK")
except Exception:
    print("vérifier si le server mongoDB est lancé")


def create_manga(manga_title):
    """
    add a new manga

    return id manga inserted
    """
    res = manga.insert_one({"mangaTitle": manga_title, "chapiters": []})

    return res.inserted_id


def read_manga(manga_title):
    """
    return :  a dict with the manga id or None if the manga title don't exist
    """

    return manga.find_one({"mangaTitle": manga_title})


def read_manga_with_chapiters_number(manga_reading):
    """
    return : list of chapitersNumbers
    """

    res = manga_reading["chapiters"]

    return [row["number"] for row in res]


def update_chapiter(manga_title, chap_num, chap_title, chap_date, chap_url):

    return manga.update_one(
        {"mangaTitle": manga_title},
        {
            "$push": {
                "chapiters": {
                    "number": chap_num,
                    "title": chap_title,
                    "date": chap_date,
                    "url": chap_url,
                }
            }
        },
    ).matched_count


def controle_update_chapiter(manga_title, chap_num, chap_title, chap_date, chap_url):
    """

    """
    current_manga = read_manga(manga_title)

    if not current_manga:
        create_manga(manga_title)
        print(f"We had a new manga : {manga_title}")
        current_manga = read_manga(manga_title)

    if chap_num in read_manga_with_chapiters_number(current_manga):
        print(f"Chapiter n°{chap_num} of {manga_title} already exist")
        return 0
    else:
        update_chapiter(manga_title, chap_num, chap_title, chap_date, chap_url)
        print(f"{manga_title} had a new chapiter {chap_num}")
        return 1


def delete_manga_id(manga_id):
    """

    """
    try:
        return manga.delete_one(manga_id).deleted_count
    except Exception:

        traceback.print_exc()


def get_all_manga_title():
    """
        return list of titles of all manga
    """
    liste_manga = manga.aggregate(
        [
            {"$project": {"_id": 0, "mangaTitle": 1}},
            {"$match": {"mangaTitle": {"$exists": True}}},
        ]
    )

    return sorted([x["mangaTitle"] for x in list(liste_manga)])


def my_load():

    # load path
    list_json = sorted(glob.glob(f"{env_path}data/json/*.json"), reverse=True)

    if not list_json:
        print("pas de fichier")
        return 0

    data = load_json(list_json[0])

    for row in data:
        controle_update_chapiter(
            row["mangaTitle"],
            row["chapiterNumber"],
            row["chapTitle"],
            row["chapDate"]["$date"],
            row["link"],
        )


if __name__ == "__main__":
    my_load()
