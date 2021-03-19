# manipulation du Json
import json
from bson import json_util
import glob

# manipulation des dates
from datetime import datetime

envPath = ""


def uniqueName(extention="csv"):
    """
    return a name unqiue for a csv file
    with a timestamp
    unqiue por seconde
    """
    nameEnding = f"manga.{extention}"
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    name = str(timestamp) + "_" + nameEnding
    return name


def saveRawData(data):
    """
        Dump a dictionary to json file
    """
    with open(f'{envPath}data/raw/{uniqueName("json")}', "w") as f:
        json.dump(data, f)


def dumpJson(path, myData):
    """
        Dump a dictionary
    """

    with open(path, "w") as f:
        json.dump(myData, f)


def loadJson(path):
    """
        Load a json file

        return : dictionary
    """
    with open(path, "r") as read_file:
        loaded_dictionaries = json.load(read_file)

    return loaded_dictionaries


def loadLastJson(path, number):
    """
        load last json file

        parametter : path of folder, number of files

        return : list of dictionary
    """

    listPathJsonFile = sorted(glob.glob(f"{path}/*.json"), reverse=True)

    data = []

    for one_path in listPathJsonFile[:number]:
        data.append(loadJson(one_path))
