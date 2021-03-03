import glob

from utile import loadJson, dumpJson, uniqueName

envPath = ""

def mytransforme():

    # load path 
    listJson = sorted(glob.glob(f"{envPath}data/json/*.json"), reverse=True)
    data = {}

    # select two most recent files
    for one_path in listJson[:2]:
        data[one_path] = loadJson(one_path)

    # transforme data 

    if data[listJson[0]] == data[listJson[1]]:
        print("nothing new")
        return "stop"
    else:
        newData = []
        for i, manga in enumerate(data[listJson[0]]):
            if data[listJson[1]][0] == manga:
                newData = data[listJson[0]][:i]
                break
        
        if not newData:
            print("all is new !")
            print("log: search if data is missing")
            dumpJson(f"{envPath}data/toAdd/{uniqueName('json')}",newData)
            return "continue"
        else:
            print(f"log : return Newdata {len(newData)}")
            dumpJson(f"{envPath}data/toAdd/{uniqueName('json')}",newData)
            return "continue"
    
if __name__ == "__main__":
    mytransforme()