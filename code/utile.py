# manipulation du Json
import json
from bson import json_util
import glob

# manipulation des dates
from datetime import datetime

env_path = ""


def unique_name(extention="csv"):
    """
    return a name unqiue for a csv file
    with a timestamp
    unqiue por seconde
    """
    name_ending = f"manga.{extention}"
    now = datetime.now()
    timestamp = int(datetime.timestamp(now))
    name = str(timestamp) + "_" + name_ending
    return name


def save_raw_data(data):
    """
        Dump a dictionary to json file
    """
    with open(f'{env_path}data/raw/{unique_name("json")}', "w") as f:
        json.dump(data, f)


def dump_json(path, my_data):
    """
        Dump a dictionary

        parametter : path of folder, list of dictionary

        return : Nothing
    """

    with open(path, "w") as f:
        json.dump(my_data, f)


def load_json(path):
    """
        Load a json file

        parametter : path of folder

        return : dictionary
    """
    with open(path, "r") as read_file:
        loaded_dictionaries = json.load(read_file)

    return loaded_dictionaries


def load_last_json(path, number):
    """
        load last json file

        parametter : path of folder, number of files

        return : list of dictionary
    """

    list_path_json_file = sorted(glob.glob(f"{path}/*.json"), reverse=True)

    data = []

    for one_path in list_path_json_file[:number]:
        data.append(load_json(one_path))
