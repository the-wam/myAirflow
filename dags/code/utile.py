# manipulation du Json
import json
from bson import json_util

# manipulation des dates
from datetime import datetime

envPath = "dags/code/"

def uniqueName(extention="csv"):
    """
    return a name unqiue for a csv file 
    with a timestamp 
    unqiue por seconde 
    """
    nameEnding = f"manga.{extention}"
    now = datetime.now()
    timestamp  = int(datetime.timestamp(now))
    name = str(timestamp) + "_" + nameEnding
    return name

def saveRawData(data):
    with open(f'{envPath}data/raw/{uniqueName("json")}', 'w') as f:
        json.dump(data, f)

def dumpJson(path, myData):
    with open(path, 'w') as f:
        json.dump(myData, f)
    
def loadJson(path):
    with open(path, 'r') as read_file:
        loaded_dictionaries = json.load(read_file)

    return loaded_dictionaries
