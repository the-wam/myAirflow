import os

import json

import pymongo
from pymongo import MongoClient

import glob

from code.uttil import loadJson

envPath = "dags/code/"

client = MongoClient('mongodb://localhost:27017/')
db = client.test_database
collection = db.test_collection
collection.find_one()
manga = db.manga

def createManga(mangaTitle):
    """
    add a new manga
    
    return id manga inserted
    """
    res = manga.insert_one({"mangaTitle": mangaTitle, "chapiters": []})
    

    return res.inserted_id

def readManga(mangaTitle):
    """
    return :  a dict with the manga id or None if the manga title don't exist
    """
    
    return manga.find_one({"mangaTitle": mangaTitle})

def readMangaWithChapitersNumber(mangaReading):
    """
    return : list of chapitersNumbers
    """
    
    res = mangaReading["chapiters"]

    return [row["number"] for row in res]

def updateChapiter(mangaTitle, chapNum, chapTitle, chapDate, chapURL):

    return manga.update_one({"mangaTitle": mangaTitle},
            {'$push':{"chapiters": {
                "number": chapNum,
                "title": chapTitle, 
                "date": chapDate,
                "url": chapURL}}}).matched_count

def ControleUpdateChapiter(mangaTitle, chapNum, chapTitle, chapDate, chapURL):
    """
        return 0 if 
    """
    currentManga = readManga(mangaTitle)
    
    if not currentManga:
        createManga(mangaTitle)
        print(f"We had a new manga : {mangaTitle}")
        currentManga = readManga(mangaTitle)

    if chapNum in readMangaWithChapitersNumber(currentManga):
        print(f"Chapiter n°{chapNum} of {mangaTitle} already exist")
        return 0
    else:
        updateChapiter(mangaTitle, chapNum, chapTitle, chapDate, chapURL)
        print(f"{mangaTitle} had a new chapiter {chapNum}")
        return 1

def deleteMangaId(mangaId):
    """
    
    """
    try:
        return manga.delete_one(mangaId).deleted_count
    except Exception as e :
        print(e)

def getAllMangaTitle():
    """
        return list of titles of all manga 
    """
    listeManga = manga.aggregate([{'$project': {'_id':0, 'mangaTitle':1}},
                                  {'$match': {'mangaTitle': {'$exists': True}}}])
    
    
    return sorted([x['mangaTitle'] for x in list(listeManga)])



def myload():

    # load path 
    listJson = sorted(glob.glob(f"{envPath}data/toAdd/*.json"), reverse=True)

    data = loadJson(listJson[0])

    for row in data:
        ControleUpdateChapiter(
            row["mangaTitle"],
            row["chapiterNumber"],
            row["chapTitle"],
            row["chapDate"]["$date"],
            row["link"])
    
    if os.path.exists(listJson[0]):
        os.remove(listJson[0])
        print(f"{listJson[0]} : is deaded")


if __name__ == "__main__":
    myload()